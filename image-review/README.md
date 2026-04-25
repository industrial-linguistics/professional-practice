# Image Review Queue

This directory stores human-readable review artifacts for generated course images.

- Weekly batches are listed in `batches/YYYY-MM-DD.md`.
- Rejected or commented candidates are appended to `rework-queue.md` by the raksasa processor.
- Draft candidate images and rendered previews are not committed here; they live under `state/image-review/` on raksasa and `/htdocs/image-review/candidates/` on merah until approved.

Approved images are copied into their final `content/.../images/...` paths by `scripts/image_review_process_reviews.py`.
