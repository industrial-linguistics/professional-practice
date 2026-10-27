#!/usr/bin/env python3
"""Exchange review snapshots and immutable candidate bundles through private S3.

The live SQLite database stays on merah. Only authority-import writes to it;
cloud workers submit new pending candidates, never a replacement database.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shlex
import sqlite3
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path, PurePosixPath
from uuid import uuid4

DEFAULT_S3_URI = "s3://professional-practice-image-review-141101760219/exchange"
DEFAULT_DB = "/var/www/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite"
DEFAULT_CANDIDATES = "/var/www/vhosts/professional-practice.industrial-linguistics.com/htdocs/image-review/candidates"
DEFAULT_REMOTE_SCRIPT = "/home/professionalpractice/image-review-exchange/scripts/image_review_exchange.py"
MAX_FILE = 25 * 1024 * 1024
MAX_BUNDLE = 100 * 1024 * 1024
MAX_FILES = 2000
ID_RE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,119}\Z")
TOPIC_RE = re.compile(r"content/part-[0-9]{2}/[a-z0-9][a-z0-9-]*\Z")
FIELDS = ("id", "batch_id", "target_path", "topic_path", "slide_ref", "brief", "prompt")
FORMATS = ("html", "graphviz", "mermaid", "chart", "tikz", "raster")
REQUIRED = ("candidate.png", "current-slide.png", "proposed-slide.png", "prompt.txt")
IMPORT_SCHEMA = """CREATE TABLE IF NOT EXISTS image_review_imports (
    run_id TEXT PRIMARY KEY, manifest_sha256 TEXT NOT NULL,
    candidate_ids TEXT NOT NULL, imported_at INTEGER NOT NULL
)"""


class InvalidBundle(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def checked_id(value: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise InvalidBundle(f"Invalid ID: {value!r}")
    return value


def relative(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(p in ("", ".", "..") for p in value.split("/")) or "\\" in value:
        raise InvalidBundle(f"Unsafe relative path: {value!r}")
    return value


def read_zip(data: bytes) -> dict[str, bytes]:
    if len(data) > MAX_BUNDLE:
        raise InvalidBundle("Archive exceeds bundle size limit")
    result = {}
    total = 0
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if len(archive.infolist()) > MAX_FILES:
                raise InvalidBundle("Too many files in archive")
            for item in archive.infolist():
                name = relative(item.filename)
                if name in result or item.is_dir() or item.file_size > MAX_FILE:
                    raise InvalidBundle(f"Invalid or duplicate archive member: {name}")
                if (item.external_attr >> 16) & 0o170000 == 0o120000:
                    raise InvalidBundle(f"Symlink in archive: {name}")
                total += item.file_size
                if total > MAX_BUNDLE:
                    raise InvalidBundle("Expanded archive exceeds bundle size limit")
                result[name] = archive.read(item)
    except (zipfile.BadZipFile, RuntimeError) as exc:
        raise InvalidBundle(f"Invalid ZIP archive: {exc}") from exc
    return result


def make_zip(files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in sorted(files.items()):
            info = zipfile.ZipInfo(relative(name), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content)
    return output.getvalue()


def tree_files(root: Path) -> dict[str, bytes]:
    result = {}
    if root.exists():
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise InvalidBundle(f"Symlink in bundle source: {path}")
            if path.is_file():
                if path.stat().st_size > MAX_FILE:
                    raise InvalidBundle(f"File too large: {path}")
                result[path.relative_to(root).as_posix()] = path.read_bytes()
    return result


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
    try:
        temporary.chmod(0o644)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def check_db(path: Path) -> dict:
    with sqlite3.connect(f"file:{path.resolve()}?mode=ro", uri=True) as conn:
        if conn.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise InvalidBundle("SQLite snapshot failed integrity check")
        statuses = dict(conn.execute("SELECT status,count(*) FROM candidates GROUP BY status"))
        return {"candidates": sum(statuses.values()), "statuses": statuses,
                "review_events": conn.execute("SELECT count(*) FROM review_events").fetchone()[0],
                "last_event_id": conn.execute("SELECT coalesce(max(id),0) FROM review_events").fetchone()[0]}


def authority_export(db: Path, candidates_dir: Path, output: Path) -> dict:
    if not db.is_file():
        raise InvalidBundle("Authoritative database is missing")
    output.mkdir(parents=True, exist_ok=True)
    dest = output / "image-review.sqlite"
    with sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True) as source:
        with sqlite3.connect(dest) as target:
            source.backup(target)
    stats = check_db(dest)
    atomic_write(output / "candidates.zip", make_zip(tree_files(candidates_dir)))
    metadata = {"schema_version": 1, "source": "merah", "checked_at": int(time.time()), **stats}
    atomic_write(output / "snapshot.json", json_bytes(metadata))
    return metadata


class S3Store:
    def __init__(self, uri: str, profile: str | None = None):
        import boto3
        from botocore.config import Config
        match = re.fullmatch(r"s3://([^/]+)(?:/(.*))?", uri.rstrip("/"))
        if not match:
            raise ValueError("Expected s3://bucket/prefix")
        self.bucket, self.prefix = match[1], (match[2] or "").strip("/")
        self.client = boto3.Session(profile_name=profile).client(
            "s3", region_name=os.environ.get("AWS_DEFAULT_REGION", "ap-southeast-2"),
            config=Config(connect_timeout=15, read_timeout=60, retries={"max_attempts": 3}))
        if "IfNoneMatch" not in self.client.meta.service_model.operation_model("PutObject").input_shape.members:
            raise RuntimeError("Install .codex/cloud-requirements.txt: this boto3 is too old for conditional S3 writes")

    def key(self, key: str) -> str:
        return "/".join(filter(None, (self.prefix, relative(key))))

    def get(self, key: str) -> bytes:
        response = self.client.get_object(Bucket=self.bucket, Key=self.key(key))
        try:
            if response.get("ContentLength", 0) > MAX_BUNDLE:
                raise InvalidBundle("S3 object too large")
            data = response["Body"].read(MAX_BUNDLE + 1)
            if len(data) > MAX_BUNDLE:
                raise InvalidBundle("S3 object too large")
            return data
        finally:
            response["Body"].close()

    def maybe_get(self, key: str) -> bytes | None:
        from botocore.exceptions import ClientError
        try:
            return self.get(key)
        except ClientError as exc:
            if exc.response["Error"]["Code"] in ("NoSuchKey", "NotFound", "404"):
                return None
            if exc.response["Error"]["Code"] in ("AccessDenied", "403"):
                # With prefix-scoped ListBucket, S3 can hide missing objects as 403.
                exact = self.key(key)
                page = self.client.list_objects_v2(Bucket=self.bucket, Prefix=exact, MaxKeys=1)
                if not any(obj["Key"] == exact for obj in page.get("Contents", [])):
                    return None
            raise

    def put(self, key: str, content: bytes, immutable: bool = True) -> None:
        from botocore.exceptions import ClientError
        if len(content) > MAX_BUNDLE:
            raise InvalidBundle("S3 object too large")
        if immutable:
            try:
                head = self.client.head_object(Bucket=self.bucket, Key=self.key(key))
                if head.get("Metadata", {}).get("sha256") == digest(content) and head.get("ContentLength") == len(content):
                    return
            except ClientError as exc:
                if exc.response["Error"]["Code"] not in ("NoSuchKey", "NotFound", "404", "AccessDenied", "403"):
                    raise
        try:
            self.client.put_object(Bucket=self.bucket, Key=self.key(key), Body=content,
                                   Metadata={"sha256": digest(content)},
                                   **({"IfNoneMatch": "*"} if immutable else {}))
        except ClientError as exc:
            if not immutable or exc.response["Error"]["Code"] not in ("PreconditionFailed", "412"):
                raise
            if self.get(key) != content:
                raise InvalidBundle(f"Immutable object already has different content: {key}") from exc

    def keys(self, prefix: str):
        base = self.key(prefix.rstrip("/")) + ("/" if prefix.endswith("/") else "")
        for page in self.client.get_paginator("list_objects_v2").paginate(Bucket=self.bucket, Prefix=base):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                yield key[len(self.prefix) + 1:] if self.prefix else key


def publish_snapshot(store, source: Path) -> dict:
    db, assets = (source / "image-review.sqlite").read_bytes(), (source / "candidates.zip").read_bytes()
    meta = json.loads((source / "snapshot.json").read_bytes())
    version = digest(db)[:20] + "-" + digest(assets)[:20]
    meta.update({"version": version, "database_sha256": digest(db), "assets_sha256": digest(assets)})
    store.put(f"snapshots/{version}/image-review.sqlite", db)
    store.put(f"snapshots/{version}/candidates.zip", assets)
    store.put("latest.json", json_bytes(meta), immutable=False)
    return meta


def fetch_snapshot(store, state: Path, max_age: int = 86400) -> dict:
    meta = json.loads(store.get("latest.json"))
    if meta.get("schema_version") != 1 or meta.get("source") != "merah":
        raise InvalidBundle("Unrecognised snapshot manifest")
    age = time.time() - int(meta["checked_at"])
    if age > max_age or age < -300:
        raise InvalidBundle(f"Review snapshot is stale or from the future ({age:.0f} seconds)")
    version = checked_id(meta["version"])
    db = store.get(f"snapshots/{version}/image-review.sqlite")
    assets = store.get(f"snapshots/{version}/candidates.zip")
    if digest(db) != meta["database_sha256"] or digest(assets) != meta["assets_sha256"]:
        raise InvalidBundle("Snapshot checksum mismatch")
    files = read_zip(assets)
    state.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=state) as scratch:
        scratch = Path(scratch)
        candidate_db = scratch / "image-review.sqlite"
        candidate_db.write_bytes(db)
        stats = check_db(candidate_db)
        if stats["last_event_id"] != meta["last_event_id"] or stats["candidates"] != meta["candidates"]:
            raise InvalidBundle("Snapshot counts do not match its manifest")
        with sqlite3.connect(f"file:{candidate_db.resolve()}?mode=ro", uri=True) as conn:
            incoming_ids = {row[0] for row in conn.execute("SELECT id FROM candidates")}
        existing_db = state / "image-review.sqlite"
        if existing_db.exists():
            with sqlite3.connect(f"file:{existing_db.resolve()}?mode=ro", uri=True) as conn:
                local_ids = {row[0] for row in conn.execute("SELECT id FROM candidates")}
            if local_ids - incoming_ids:
                raise InvalidBundle("Local candidates have not reached the server; preserve them before fetching again")
        # Preserve any local, as-yet-unsubmitted bundles. Existing paths must match.
        for name, content in files.items():
            target = state / "candidates" / name
            if any(parent.is_symlink() for parent in target.parents if parent != state.parent):
                raise InvalidBundle(f"Symlink in local candidate path: {name}")
            if target.exists() and (target.is_symlink() or target.read_bytes() != content):
                raise InvalidBundle(f"Local candidate differs from the authoritative snapshot: {name}")
        for name, content in files.items():
            atomic_write(state / "candidates" / name, content)
        atomic_write(state / "image-review.sqlite", db)
        with sqlite3.connect(f"file:{candidate_db.resolve()}?mode=ro", uri=True) as conn:
            meta["known_candidate_ids"] = [row[0] for row in conn.execute("SELECT id FROM candidates ORDER BY id")]
        atomic_write(state / "snapshot.json", json_bytes(meta))
    return meta


def validate_candidate(row: dict, files: dict[str, bytes], format_name: str) -> None:
    if any(not isinstance(row.get(key), str) for key in FIELDS):
        raise InvalidBundle("Candidate metadata fields must be strings")
    checked_id(row["id"])
    if format_name not in FORMATS or not TOPIC_RE.fullmatch(row["topic_path"]):
        raise InvalidBundle("Invalid composition format or topic path")
    target = relative(row["target_path"])
    if not target.startswith(row["topic_path"] + "/images/") or not target.endswith(".png"):
        raise InvalidBundle("Candidate target must be a PNG under its topic images directory")
    if not row["brief"].strip() or len(row["prompt"]) > 100000:
        raise InvalidBundle("Missing brief or oversized prompt")
    for name in REQUIRED:
        if name not in files:
            raise InvalidBundle(f"Missing required review artifact: {name}")
    if files["prompt.txt"].decode().strip() != row["prompt"].strip():
        raise InvalidBundle("Prompt file differs from registered prompt")
    for heading in ("Composition decision", "Content preservation", "Layout QA"):
        if heading not in row["prompt"]:
            raise InvalidBundle(f"Missing QA heading: {heading}")
    if format_name != "raster" and not any(Path(name).suffix in (".html", ".svg", ".dot", ".mmd", ".py", ".tex") for name in files):
        raise InvalidBundle("Deterministic candidate is missing editable source")
    for name in REQUIRED[:3]:
        data = files[name]
        if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            raise InvalidBundle(f"Not a PNG: {name}")
        width, height = int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
        if width < 800 or height < 450 or width > 8192 or height > 8192:
            raise InvalidBundle(f"Unexpected image dimensions: {name}: {width}x{height}")


def create_submission(state: Path, ids: list[str], run_id: str, format_name: str, qa_passed: bool) -> bytes:
    if not qa_passed:
        raise InvalidBundle("Geometry/content QA must pass before submission")
    checked_id(run_id)
    snapshot = json.loads((state / "snapshot.json").read_bytes())
    if time.time() - int(snapshot["checked_at"]) > 86400:
        raise InvalidBundle("Fetch a fresh review snapshot before submitting")
    rows, members = [], {}
    if len(set(ids)) != len(ids) or not 1 <= len(ids) <= 5:
        raise InvalidBundle("Submit one to five distinct candidates")
    with sqlite3.connect(f"file:{(state / 'image-review.sqlite').resolve()}?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        for cid in ids:
            checked_id(cid)
            if cid in snapshot["known_candidate_ids"]:
                raise InvalidBundle("Use a new ID for reworks; existing review records are immutable")
            row = conn.execute("SELECT * FROM candidates WHERE id=?", (cid,)).fetchone()
            if row is None or row["status"] != "pending":
                raise InvalidBundle(f"Candidate is absent or not pending: {cid}")
            row = {key: row[key] for key in FIELDS}
            files = tree_files(state / "candidates" / cid)
            validate_candidate(row, files, format_name)
            row["format"] = format_name
            row["files"] = {name: {"sha256": digest(data), "size": len(data)} for name, data in files.items()}
            rows.append(row)
            members.update({f"candidates/{cid}/{name}": data for name, data in files.items()})
    manifest = {"schema_version": 1, "run_id": run_id, "snapshot_version": snapshot["version"],
                "qa_passed": True, "candidates": rows}
    members["submission.json"] = json_bytes(manifest)
    return make_zip(members)


def submit(store, content: bytes, run_id: str) -> dict:
    checked_id(run_id)
    ready = {"schema_version": 1, "run_id": run_id, "sha256": digest(content), "size": len(content)}
    store.put(f"submissions/{run_id}/bundle.zip", content)
    store.put(f"submissions/{run_id}/ready.json", json_bytes(ready))
    return ready


def unpack_submission(content: bytes) -> tuple[dict, dict[str, bytes]]:
    members = read_zip(content)
    try:
        manifest = json.loads(members.pop("submission.json"))
        if manifest["schema_version"] != 1 or manifest["qa_passed"] is not True:
            raise InvalidBundle("Unsupported submission or QA has not passed")
        checked_id(manifest["run_id"])
        rows = manifest["candidates"]
        if not 1 <= len(rows) <= 5 or len({row["id"] for row in rows}) != len(rows):
            raise InvalidBundle("Invalid candidate set")
        expected = set()
        for row in rows:
            prefix = f"candidates/{checked_id(row['id'])}/"
            files = {name[len(prefix):]: data for name, data in members.items() if name.startswith(prefix)}
            validate_candidate(row, files, row["format"])
            if set(files) != set(row["files"]):
                raise InvalidBundle("Candidate file manifest does not match archive")
            for name, data in files.items():
                if row["files"][name] != {"sha256": digest(data), "size": len(data)}:
                    raise InvalidBundle(f"Candidate file checksum mismatch: {name}")
                expected.add(prefix + name)
        if set(members) != expected:
            raise InvalidBundle("Unexpected files in submission")
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidBundle(f"Malformed submission: {exc}") from exc
    return manifest, members


def authority_import(db: Path, candidates_dir: Path, content: bytes) -> dict:
    manifest, members = unpack_submission(content)
    run_id, manifest_hash = manifest["run_id"], digest(json_bytes(manifest))
    # No schemas or files change until the entire untrusted bundle validates.
    if not db.is_file():
        raise InvalidBundle("Authoritative database is missing")
    conn = sqlite3.connect(db, timeout=30)
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(IMPORT_SCHEMA)
        previous = conn.execute("SELECT manifest_sha256,candidate_ids FROM image_review_imports WHERE run_id=?", (run_id,)).fetchone()
        if previous:
            if previous[0] != manifest_hash:
                raise InvalidBundle("Run ID already imported with different content")
            conn.rollback()
            return {"run_id": run_id, "status": "accepted", "candidate_ids": json.loads(previous[1]), "already_imported": True}
        for row in manifest["candidates"]:
            existing = conn.execute("SELECT 1 FROM candidates WHERE id=?", (row["id"],)).fetchone()
            if existing:
                raise InvalidBundle(f"Candidate ID already exists; reviewer state preserved: {row['id']}")
            # Avoid replacing a candidate another worker has already submitted.
            active = conn.execute("SELECT id FROM candidates WHERE target_path=? AND (status IN ('pending','approved') OR (status='commented' AND requeued_at IS NULL))", (row["target_path"],)).fetchone()
            if active:
                raise InvalidBundle(f"Target already has an active candidate: {active[0]}")
        for row in manifest["candidates"]:
            cid = row["id"]
            candidate_files = {name[len(f'candidates/{cid}/'):]: data for name, data in members.items() if name.startswith(f"candidates/{cid}/")}
            destination = candidates_dir / cid
            if destination.exists():
                if destination.is_symlink() or tree_files(destination) != candidate_files:
                    raise InvalidBundle(f"Existing candidate files differ: {cid}")
            else:
                candidates_dir.mkdir(parents=True, exist_ok=True)
                with tempfile.TemporaryDirectory(dir=candidates_dir) as stage:
                    staged = Path(stage) / cid
                    staged.mkdir()
                    for name, data in candidate_files.items():
                        atomic_write(staged / relative(name), data)
                    os.rename(staged, destination)
            urls = [f"/image-review/candidates/{cid}/{name}" for name in REQUIRED[:3]]
            conn.execute(f"INSERT INTO candidates ({','.join(FIELDS)},candidate_url,current_slide_url,proposed_slide_url,candidate_rel_path,status) VALUES ({','.join(['?'] * (len(FIELDS)+5))})",
                         [row[k] for k in FIELDS] + urls + [f"{cid}/candidate.png", "pending"])
            conn.execute("INSERT INTO review_events(candidate_id,actor,action,comment) VALUES (?,'s3-image-review-import','registered',?)", (cid, run_id))
        ids = [row["id"] for row in manifest["candidates"]]
        conn.execute("INSERT INTO image_review_imports VALUES (?,?,?,?)", (run_id, manifest_hash, json.dumps(ids), int(time.time())))
        conn.commit()
        return {"run_id": run_id, "status": "accepted", "candidate_ids": ids, "already_imported": False}
    finally:
        conn.close()


def authority_ack(db: Path, processed_db: Path) -> dict:
    """Acknowledge only the exact review decision processed from a snapshot."""
    changed = stale = 0
    with sqlite3.connect(f"file:{processed_db.resolve()}?mode=ro", uri=True) as source:
        source.row_factory = sqlite3.Row
        rows = source.execute("SELECT * FROM candidates WHERE processed_at IS NOT NULL OR requeued_at IS NOT NULL").fetchall()
    with sqlite3.connect(db, timeout=30) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute("BEGIN IMMEDIATE")
        for row in rows:
            live = conn.execute("SELECT * FROM candidates WHERE id=?", (row["id"],)).fetchone()
            if live is None:
                continue
            if any(live[key] != row[key] for key in ("reviewed_at", "reviewed_by", "review_comment")):
                stale += 1
                continue
            if row["status"] == "processed" and live["status"] == "approved" and live["processed_at"] is None:
                conn.execute("UPDATE candidates SET status='processed',processed_at=?,updated_at=CURRENT_TIMESTAMP WHERE id=?", (row["processed_at"], row["id"]))
                action, comment = "processed", f"installed {row['target_path']}"
            elif row["requeued_at"] and live["status"] == row["status"] and live["requeued_at"] is None:
                conn.execute("UPDATE candidates SET requeued_at=?,updated_at=CURRENT_TIMESTAMP WHERE id=?", (row["requeued_at"], row["id"]))
                action, comment = "requeued", row["status"]
            else:
                continue
            conn.execute("INSERT INTO review_events(candidate_id,actor,action,comment) VALUES (?,'image-review-process',?,?)", (row["id"], action, comment))
            changed += 1
    return {"acknowledged": changed, "stale_decisions_preserved": stale}


def remote_run(remote: str, args: list[str]) -> str:
    completed = subprocess.run(["ssh", "-o", "BatchMode=yes", remote, shlex.join(args)], check=True, capture_output=True, text=True)
    return completed.stdout


def bridge(store, remote: str, script: str, work: Path, db: str, candidates: str) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    accepted = rejected = 0
    with tempfile.TemporaryDirectory(dir=work) as scratch:
        scratch = Path(scratch)
        for key in store.keys("submissions/"):
            if not key.endswith("/ready.json"):
                continue
            try:
                run_id = checked_id(key.split("/")[-2])
                if key != f"submissions/{run_id}/ready.json":
                    raise InvalidBundle("Unexpected submission path")
            except InvalidBundle:
                rejected += 1
                continue
            if store.maybe_get(f"receipts/{run_id}.json") is not None:
                continue
            bundle = store.maybe_get(f"submissions/{run_id}/bundle.zip")
            try:
                try:
                    ready = json.loads(store.get(key))
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    raise InvalidBundle("Malformed ready marker") from exc
                if bundle is None:
                    raise InvalidBundle("Ready marker has no bundle")
                if ready != {"schema_version": 1, "run_id": run_id, "sha256": digest(bundle), "size": len(bundle)}:
                    raise InvalidBundle("Ready marker checksum mismatch")
                manifest, _ = unpack_submission(bundle)
                if manifest["run_id"] != run_id:
                    raise InvalidBundle("Submission run ID differs from its key")
                local = scratch / f"{run_id}.zip"
                local.write_bytes(bundle)
                remote_file = f"/home/professionalpractice/image-review-exchange/inbox/{run_id}.zip"
                subprocess.run(["scp", "-q", str(local), f"{remote}:{remote_file}"], check=True)
                output = remote_run(remote, ["python3", script, "authority-import", "--db", db,
                                              "--candidates-dir", candidates, "--bundle", remote_file])
                receipt = json.loads(output)
                receipt["run_id"] = run_id
                remote_run(remote, ["rm", "-f", remote_file])
                if receipt["status"] == "accepted":
                    accepted += 1
                else:
                    rejected += 1
            except InvalidBundle as exc:
                receipt = {"run_id": run_id, "status": "rejected", "error": str(exc)}
                rejected += 1
            receipt["bundle_sha256"] = digest(bundle) if bundle is not None else None
            receipt["recorded_at"] = int(time.time())
            store.put(f"receipts/{run_id}.json", json_bytes(receipt))
        remote_output = "/home/professionalpractice/image-review-exchange/export"
        output = remote_run(remote, ["python3", script, "authority-export", "--db", db,
                                      "--candidates-dir", candidates, "--output-dir", remote_output])
        json.loads(output)
        for name in ("image-review.sqlite", "candidates.zip", "snapshot.json"):
            subprocess.run(["scp", "-q", f"{remote}:{remote_output}/{name}", str(scratch / name)], check=True)
        snapshot = publish_snapshot(store, scratch)
    return {"accepted": accepted, "rejected": rejected, "snapshot": snapshot}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s3-uri", default=os.environ.get("IMAGE_REVIEW_S3_URI", DEFAULT_S3_URI))
    parser.add_argument("--profile", default=os.environ.get("IMAGE_REVIEW_AWS_PROFILE"))
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch")
    fetch.add_argument("--state-dir", type=Path, default=Path("state/image-review"))
    fetch.add_argument("--max-age-hours", type=float, default=24)
    send = commands.add_parser("submit")
    send.add_argument("--state-dir", type=Path, default=Path("state/image-review"))
    send.add_argument("--candidate", action="append", required=True)
    send.add_argument("--run-id", default=None)
    send.add_argument("--format", choices=FORMATS, required=True)
    send.add_argument("--qa-passed", action="store_true")
    receipt = commands.add_parser("receipt")
    receipt.add_argument("run_id")
    evidence = commands.add_parser("archive-evidence")
    evidence.add_argument("directory", type=Path)
    evidence.add_argument("--run-id", required=True)
    run = commands.add_parser("bridge")
    run.add_argument("--remote", default="professionalpractice@merah")
    run.add_argument("--remote-script", default=DEFAULT_REMOTE_SCRIPT)
    run.add_argument("--work-dir", type=Path, default=Path("state/image-review-bridge"))
    for command in (run, commands.add_parser("authority-export"), commands.add_parser("authority-import"), commands.add_parser("authority-ack")):
        command.add_argument("--db", type=Path, default=Path(DEFAULT_DB))
        command.add_argument("--candidates-dir", type=Path, default=Path(DEFAULT_CANDIDATES))
        if command.prog.endswith("authority-export"):
            command.add_argument("--output-dir", type=Path, required=True)
        if command.prog.endswith("authority-import"):
            command.add_argument("--bundle", type=Path, required=True)
        if command.prog.endswith("authority-ack"):
            command.add_argument("--processed-db", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "authority-export":
        result = authority_export(args.db, args.candidates_dir, args.output_dir)
    elif args.command == "authority-import":
        try:
            result = authority_import(args.db, args.candidates_dir, args.bundle.read_bytes())
        except InvalidBundle as exc:
            result = {"status": "rejected", "error": str(exc)}
    elif args.command == "authority-ack":
        result = authority_ack(args.db, args.processed_db)
    else:
        store = S3Store(args.s3_uri, args.profile)
        if args.command == "fetch":
            result = fetch_snapshot(store, args.state_dir, int(args.max_age_hours * 3600))
            result.pop("known_candidate_ids", None)
        elif args.command == "submit":
            run_id = args.run_id or time.strftime("%Y-%m-%d-") + uuid4().hex
            content = create_submission(args.state_dir, args.candidate, run_id, args.format, args.qa_passed)
            result = submit(store, content, run_id)
        elif args.command == "receipt":
            content = store.maybe_get(f"receipts/{checked_id(args.run_id)}.json")
            if content is None:
                print(json.dumps({"run_id": args.run_id, "status": "pending"}))
                return 3
            result = json.loads(content)
            if result["status"] != "accepted":
                print(json.dumps(result))
                return 1
        elif args.command == "archive-evidence":
            checked_id(args.run_id)
            files = tree_files(args.directory)
            if not files or "prompt.txt" not in files:
                raise InvalidBundle("Source rework evidence must include prompt.txt")
            for heading in ("Composition decision", "Content preservation", "Layout QA"):
                if heading not in files["prompt.txt"].decode():
                    raise InvalidBundle(f"Missing evidence heading: {heading}")
            content = make_zip(files)
            key = f"source-reworks/{args.run_id}/evidence.zip"
            result = {"run_id": args.run_id, "key": key, "sha256": digest(content), "size": len(content)}
            store.put(key, content)
            store.put(f"source-reworks/{args.run_id}/manifest.json", json_bytes(result))
        elif args.command == "bridge":
            result = bridge(store, args.remote, args.remote_script, args.work_dir, str(args.db), str(args.candidates_dir))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
