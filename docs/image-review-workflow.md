# Protected image review workflow

The image-generation workflow uses private S3 for cloud input and output. The live review SQLite database stays on merah; cloud workers cannot replace it.

1. A five-minute raksasa bridge exports a consistent SQLite backup and candidate previews to the private, versioned S3 exchange.
2. A Codex Cloud run fetches the snapshot, makes a small batch, preserves the instructional content, and checks rendered geometry. The repository skill and `.codex/cloud-task.md` contain its run instructions.
3. New image candidates are registered locally, then submitted as immutable bundles. The bridge validates hashes and imports new pending records in a transaction, preserving all existing reviews. An accepted receipt confirms registration and protected preview publication.
4. The protected Go CGI records reviewer decisions. The daily raksasa processor installs approved assets and appends rework notes, then acknowledges only decisions that still match the processed snapshot.

Source-level HTML reworks keep semantic text in the course source and archive their QA evidence in S3. GitHub Actions continues to build and deploy course changes after a push to main.

## Private exchange and cloud setup

- Exchange: `s3://professional-practice-image-review-141101760219/exchange`
- Region: `ap-southeast-2`
- Cloud runtime setup: `.codex/cloud-setup.sh`; requirements: `.codex/cloud-requirements.txt`
- Durable task instructions: `.codex/cloud-task.md`
- Repository skill: `.agents/skills/professional-practice-images/SKILL.md`
- Server deployment: `/home/professionalpractice/image-review-exchange/` on raksasa and merah.
- Server bridge credentials: `/home/professionalpractice/.config/professional-practice/image-review-bridge.env`, mode 0600. Cloud reuses the existing shared `AWS_*` vault variables or tested AWS OIDC; do not add job-specific secret variable names.

The cloud identity needs the permissions returned by `policy('cloud')` in `scripts/provision_image_review_exchange.py`: read snapshots and receipts; write submissions and source-rework evidence. Grant those permissions to the existing shared AWS identity. Cross-account access also needs an allow for that exact principal in the bucket policy. Verify the shared identity after Cloud connectivity works; never copy a replacement secret over the shared vault bindings. The provisioner's separate cloud identity is retained for the isolated transport smoke test, and does not need to be configured in document-handling.

The bucket explicitly denies changes to authoritative snapshots and receipts by every identity except the server bridge. Review decisions stay on merah. Bucket public access is blocked, TLS is required, default encryption is enabled, and versioning is enabled. The provisioner configures these controls without printing credentials.

Cloud setup and storage transport are separate from scheduling. Verify a published environment and an end-to-end hosted run before retiring the desktop schedule. A queued legacy task does not confirm a hosted run. Do not reuse local desktop sign-in credentials on a server.

The selected environment is **document-handling**. On 27 October 2026 its setup
could validate the cached course source and offered image generation, but its
managed HTTPS proxy returned 503 for GitHub fetch and API requests. Current-main
exchange tests, shared AWS access, browser geometry, publication and schedule
cutover remain pending until connectivity is repaired. The desktop schedule stays
active during this transition.

## Review app

- CGI source: `cmd/image-review-cgi/main.go`
- Local database path: `state/image-review/image-review.sqlite`
- Merah database path inside the OpenBSD chroot: `/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite`
- Merah filesystem path: `/var/www/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite`
- Protected static candidate previews: `/image-review/candidates/...`
- Protected CGI URL: `https://professional-practice.industrial-linguistics.com/cgi-bin/image-review.cgi`

The CGI uses HTTP Basic Auth supplied by OpenBSD `httpd` and records `REMOTE_USER` in the review database.
Keep the vhost `db/` directory group-writable and keep `image-review.sqlite` mode `0664`, so SQLite journal writes still work when the CGI runs as `www`. On OpenBSD, new files inherit the containing directory's group; the publish and sync scripts enforce the writable modes after copying the database.

## Cloud candidate registration

Put `.venv/bin` first in PATH. Start every run by fetching current authoritative state; a stale or failed fetch must stop production:

```bash
python scripts/image_review_exchange.py fetch --max-age-hours 1
```

After the content-preservation and geometry gates pass, use a new candidate ID and the existing local registration tool:

```bash
python scripts/image_review_register.py \
  --id <candidate-id> --batch-id <date> \
  --target-path content/part-XX/topic/images/name.png \
  --topic-path content/part-XX/topic --slide-ref "slide N" \
  --brief "Description" \
  --prompt-file state/image-review/candidates/<candidate-id>/prompt.txt
python scripts/image_review_exchange.py submit \
  --candidate <candidate-id> --format html --qa-passed
```

A bundle contains `candidate.png`, `current-slide.png`, `proposed-slide.png`, `prompt.txt`, and editable source. The prompt must include Composition decision, Content preservation, and Layout QA. Choose the actual `html`, `graphviz`, `mermaid`, `chart`, `tikz` or `raster` format. The importer verifies file hashes, PNG dimensions, path boundaries, QA headings, candidate-ID uniqueness, and any active candidate for the same target. All imported records start pending. Reusing an accepted run ID is harmless; it never resets later reviewer decisions.

Record the returned run ID and check its receipt:

```bash
python scripts/image_review_exchange.py receipt <run-id>
```

Pending exits 3, rejected exits 1, and accepted exits 0. Allow up to five minutes for the bridge. An S3 upload alone is not publication. Rejected bundles require correction and a new run ID. Never upload an edited SQLite snapshot to the authoritative database. The old `scripts/image_review_publish_candidates.sh` now forwards explicit candidate submissions to S3 rather than overwriting the live database.

For a semantic source rework, archive the complete evidence directory instead:

```bash
python scripts/image_review_exchange.py archive-evidence <directory> --run-id <source-rework-id>
```

Record the S3 key and checksum in the dated batch note. This archives evidence without creating a review candidate or acceptance record.

## Daily raksasa processing

The bridge runs independently of the Mac every five minutes:

```cron
MAILTO=professionalpractice
*/5 * * * * /home/professionalpractice/image-review-exchange/scripts/image_review_bridge_cron.sh
```

The daily processor retains its 03:17 server schedule. Its synchronizer uses a consistent SQLite backup for reading, processes decisions in its checkout, and sends conditional acknowledgements back to merah. A newer review is preserved rather than overwritten. The stale processor checkout's unrelated rework notes and previously delivered images are preserved; the historical `delivery-pending` entries remain separate delivery work.

The bridge has its own runtime, clean checkout and process lock. It fetches main with fast-forward-only merges, publishes the authority helper atomically, and keeps the protected review stylesheet current. Routine successful checks are retained in `logs/image-review-bridge.log`; changes, imports, rejections and failures produce cron mail. Complete submissions have a final ready marker; partial uploads are ignored. Imports are idempotent and use an `image_review_imports` ledger in the live database. The server stages verified preview files before inserting pending candidates. An interrupted import can be retried without resetting reviews. Snapshot files use content-derived immutable names and `latest.json` is published last.

Validation:

```bash
python -m unittest discover -s tests -v
python scripts/smoke_image_review_exchange.py
```

The live smoke test needs the two scoped environment files locally. It tests real S3 transfer and an isolated remote SQLite import, verifies repeat delivery and preserved decisions, and checks that the production review database is byte-unchanged. Synthetic test candidates are never added to the live review app.

## Required `httpd.conf` stanza

The existing `professional-practice.industrial-linguistics.com` vhost is static-only. Add the protected locations below inside that server block and then run `doas rcctl reload httpd`.

```httpd
location "/image-review/*" {
    authenticate "Professional Practice Image Review" with "/vhosts/professional-practice.industrial-linguistics.com/etc/htpasswd"
}

location "/cgi-bin/image-review.cgi" {
    fastcgi
    root "/vhosts/professional-practice.industrial-linguistics.com"
    authenticate "Professional Practice Image Review" with "/vhosts/professional-practice.industrial-linguistics.com/etc/htpasswd"
}

location "/db/*" {
    block
}
```

Do not expose `/cgi-bin/image-review.cgi` or `/image-review/*` without the authentication rules. The candidate previews are review artifacts, not public course assets.
