# Protected image review workflow

The image-generation workflow has three stages:

1. A weekly Codex run selects a small batch from `docs/image-production-backlog.md`, generates draft images and renders two slide previews for each candidate: the current slide and the proposed slide with the image inserted.
2. The run registers each candidate in `image-review.sqlite`, writes a batch list under `image-review/batches/YYYY-MM-DD.md`, and syncs the candidate images/previews to merah.
3. A password-protected Go CGI on merah records approvals, rejections and comments. A daily raksasa cron pulls the SQLite database and candidate files back, installs approved images into `content/.../images/...`, and appends rejected/commented items to `image-review/rework-queue.md`.

## Review app

- CGI source: `cmd/image-review-cgi/main.go`
- Local database path: `state/image-review/image-review.sqlite`
- Merah database path inside the OpenBSD chroot: `/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite`
- Merah filesystem path: `/var/www/vhosts/professional-practice.industrial-linguistics.com/db/image-review.sqlite`
- Protected static candidate previews: `/image-review/candidates/...`
- Protected CGI URL: `https://professional-practice.industrial-linguistics.com/cgi-bin/image-review.cgi`

The CGI uses HTTP Basic Auth supplied by OpenBSD `httpd` and records `REMOTE_USER` in the review database.
Keep the vhost `db/` directory group-writable and keep `image-review.sqlite` mode `0664`, so SQLite journal writes still work when the CGI runs as `www`. On OpenBSD, new files inherit the containing directory's group; the publish and sync scripts enforce the writable modes after copying the database.

## Candidate registration

Use `scripts/image_review_register.py` after generating the candidate image and slide previews:

```bash
python3 scripts/image_review_register.py \
  --batch-id "$(date +%F)" \
  --target-path content/part-01/incident-vs-request/images/incident-request-decision.png \
  --topic-path content/part-01/incident-vs-request \
  --slide-ref "slide 3" \
  --brief "Incident/request/problem/change decision tree" \
  --prompt-file state/image-review/candidates/<candidate-id>/prompt.txt
```

By default this writes or updates `state/image-review/image-review.sqlite` and appends the item to `image-review/batches/<batch-id>.md`.

After registering a batch, publish the database and candidate previews:

```bash
scripts/image_review_publish_candidates.sh
```

The publish script assumes the local database is the current review database. If a review session has already started on merah, run the daily sync first before adding more candidates so reviewer actions are not overwritten.

## Daily raksasa processing

Install this crontab for `professionalpractice@raksasa`:

```cron
17 3 * * * cd /home/professionalpractice/devel/professional-practice && scripts/image_review_sync_process.sh >> logs/image-review-sync.log 2>&1
```

The sync script:

- creates a consistent SQLite backup on merah with `.backup`,
- copies candidate previews from merah,
- copies approved candidate images into their final repo path,
- appends rejected/commented candidates to `image-review/rework-queue.md`,
- copies the updated SQLite database back to merah so the web UI stops showing already processed actions.

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
