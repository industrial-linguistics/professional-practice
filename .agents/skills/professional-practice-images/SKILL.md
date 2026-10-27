---
name: professional-practice-images
description: Produce a small Professional Practice image or semantic-slide batch in Codex Cloud using the private S3 review exchange, full content preservation and rendered geometry QA.
---

# Professional Practice images in Codex Cloud

Use the checked-in `.codex/cloud-task.md` as the run instructions. The environment
must run `.codex/cloud-setup.sh` when prepared and put `.venv/bin` first in `PATH`.

The live review SQLite and review decisions belong to merah. Fetch a current S3
snapshot at the start. Cloud may add new pending candidates and upload immutable
bundles. The server registers them without replacing reviewer records. Existing
reviewer actions never belong in a cloud writeback.

Required access: repository read/write, GitHub Actions status, and exchange access
through the environment's existing shared `AWS_*` variables or tested AWS OIDC.
Use the default S3 URI in the run instructions. Do not introduce job-specific
credential variables or print secret values. No SSH key is needed.

A submitted S3 bundle is awaiting import. Only an accepted server receipt confirms
registration and protected preview publication. Source-level reworks stay in
semantic HTML and do not require a candidate submission.
