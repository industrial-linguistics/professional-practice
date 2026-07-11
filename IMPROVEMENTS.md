# IMPROVEMENTS.md

*Analysis date: 2026-07-11.*

This repository is the "IT Professional Practice" course: an 8-part
university-style curriculum (ITIL, DevOps/SRE, CRM/sales, startups, OSS and
Indigenous data sovereignty) plus a substantial build pipeline (Go tools in
`cmd/`, Python/shell in `scripts/`) that renders HTML slides into an
e-learning site, a textbook (A4 and 6x9 PDFs), run sheets, ElevenLabs audio
and FFmpeg video. Per `CURRENT_STATUS.md` (2026-07-08), the content phase is
essentially done — 81 topics complete across Parts 1-7 with a clean narrative
audit — and the bottleneck has moved to packaging, assessment delivery, and
commercial validation. The working tree is clean; recent commits are all
polish (textbook pass, MP3 audio, deploy tweaks).

## Highest Priority: Ship the Package, Not More Prose

`CURRENT_STATUS.md` already diagnoses this correctly; these items convert
that diagnosis into repo work:

1. **LICENSE/TERMS file** — there is none at the repo root, which is both a
   commercial blocker and embarrassing for a course that teaches OSS
   licensing (Part 7). One file, ten minutes. Do this first.
2. **Deploy the quiz layer.** Quiz source exists for Parts 1-7 as markdown
   with inline answers; it is not a learner-facing engine. Generate quiz
   runtime output from source (as the status notes recommend) rather than
   hand-maintaining LMS pages. Assessment is the sellable layer.
3. **SCORM 1.2 pilot for Part 1** with quiz interactions, validated in
   Moodle. No `imsmanifest.xml` exists under `output/` today.
4. **Part 8 is a stub** (`outline.md`, `practice-artifact.md`,
   `textbook-intro.md`, no topics). Either build it as a thin capstone
   scaffold or explicitly mark the product as Parts 1-7 + facilitated
   capstone; don't let it silently block "course complete" claims.
5. **Landing page + three polished sample lessons** (Part 3 DORA, Part 4
   RCA, Part 6 startup IT were already identified as candidates). Audio
   coverage is only 14 files and there is exactly one MP4
   (`content/part-01/overview/final.mp4`) — concentrate media effort on the
   three samples instead of trying to cover 81 topics.

## Bugs & Fixes

- **Stale CLAUDE.md**: it still says the repo "is in early development
  stages" and lists finished README cleanup tasks as pending. Rewrite it to
  reflect the actual architecture (Go cmds, scripts pipeline, content/,
  output/, textbook/) so agents don't re-plan solved problems.
- **README drift**: README still describes the course as a plan and points
  to `raw-notes.txt`, but the file on disk is `raw-notes.md`. Fix the link
  and update the "raw material" framing now that content is complete.
- **`scripts/__pycache__/` is present in the tree** — confirm it is
  gitignored; if committed, remove it and add to `.gitignore`. Same review
  for `logs/`, `output/`, and `state/` (build artefacts and mutable state
  living beside source invites accidental commits).

## Testing

- Only visible automated check is the audio S3 cache smoke test
  (`scripts/check_audio_s3_cache.sh`). Add:
  - a CI job (GitHub Actions is already the planned stack) that runs
    `build_elearning.py`, `build_textbook.py` and the narrative mismatch
    audit on every push — the audit is the project's de facto integration
    test and should be enforced, not run ad hoc;
  - `go test`/`go vet` for `cmd/` and `pkg/` (voicer, vtt-generator,
    render-slides currently have no test signal);
  - a link checker over the generated site in `output/elearning/`.
- Add the accessibility checks the status doc lists (keyboard nav,
  transcripts, alt text, contrast) as a scriptable gate, not a wish.

## Housekeeping / Modernization

- **Python tooling**: the scripts in `scripts/` (build_elearning.py,
  build_textbook.py, audio_generation_worker.py, etc.) appear to run as
  loose scripts. Adopt `uv`: create a `pyproject.toml`, add deps with
  `uv add`, and run via `uv run scripts/build_textbook.py`. Do not
  introduce a requirements.txt. This pins the headless-Chrome/screenshot
  dependencies that are currently only implied by `envsetup.sh`.
- Consolidate the shell/Python split: several `*.sh` scripts
  (build_audio.sh, build_videos.sh, generate_run_sheets*.sh) wrap logic
  that would be more testable in the Python layer; at minimum, add
  `set -euo pipefail` consistently and a single `make`-style entry point so
  the "step-by-step checklist in TODO.md" becomes one command.
- `TODO.md` is now almost entirely checked boxes — archive the completed
  content checklist and replace it with the packaging backlog from
  `CURRENT_STATUS.md` (SCORM, quiz engine, landing page, certificates),
  so the live TODO matches the live bottleneck.

## Security

- No committed secrets found: ElevenLabs and AWS credentials are read from
  the environment (`ELEVENLABS_API_KEY` in build_audio.sh,
  audio_generation_cron.sh). Keep it that way; consider a `.env.example`
  documenting required vars.
- The image-review CGI (`cmd/image-review-cgi`, deployed to merah) is a
  write-capable web endpoint — confirm it validates/authenticates review
  submissions before the site gets commercial traffic.

## Documentation

- Add a top-level BUILD.md (or fold into README) giving the one-command
  path from clean checkout to rendered site/textbook; today the knowledge
  is spread across README, TODO.md, envsetup.sh and
  docs/directory-structure.md.
- Add `last-verified` metadata to volatile topics (pricing, market claims,
  tool versions) as the status doc suggests — DORA/ServiceNow/Salesforce
  details date quickly.

## Quick Wins

- LICENSE + terms page (see above).
- Fix `raw-notes.txt` → `raw-notes.md` in README.
- Rewrite CLAUDE.md to current reality.
- `.gitignore` audit for `__pycache__/`, `logs/`, `output/`, `state/`.
- Commission the Indigenous review of Part 7 before using it in marketing —
  it is a stated precondition and has a long lead time, so start now.
