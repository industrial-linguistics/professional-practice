# Operations Setup

Last checked: 2026-04-25.

## Host roles

- `professionalpractice@merah` is the publication and light hosting account.
- `professionalpractice@raksasa` is the build and orchestration account for video, audio, cache-aware rendering and any future scheduled work.
- The canonical source remains GitHub: `industrial-linguistics/professional-practice`.

This follows the usual `merah`/`raksasa` split: keep static/public output on `merah`, and keep heavier generation work on `raksasa`.

## Current state

### `professionalpractice@merah`

- The account already existed on `merah`.
- Local SSH access from this machine has been installed and verified with `ssh professionalpractice@merah`.
- The account also accepts the dedicated `professionalpractice@raksasa` SSH key, so the build account can publish to `merah` without going through `gregb`.

### `professionalpractice@raksasa`

- The account has been created with home directory `/home/professionalpractice`.
- The repository is checked out at `/home/professionalpractice/devel/professional-practice`.
- The remote checkout uses SSH: `git@github.com:industrial-linguistics/professional-practice.git`.
- A dedicated GitHub SSH key exists at `/home/professionalpractice/.ssh/id_ed25519_github`. SSH authentication to GitHub has been verified from the service account.
- A dedicated `merah` SSH key exists at `/home/professionalpractice/.ssh/id_ed25519_merah` and has been installed into `professionalpractice@merah`.
- `~/.ssh/config` maps `github.com` to the GitHub key and `merah` to the `merah` key.

### Secrets and environment

- The ElevenLabs key has been installed as `/home/professionalpractice/.elevenlabs.io`.
- AWS credentials have been installed under `/home/professionalpractice/.aws/` from the local `audio-fragements` profile.
- `/home/professionalpractice/.config/professional-practice.env` sets:
  - `VOICER_S3_BUCKET=audio-fragments`
  - `AWS_DEFAULT_REGION=ap-southeast-2`
  - `AWS_REGION=ap-southeast-2`
- The file is sourced from `.profile`.

Do not commit these files. They live only in the service account home directory.

## Verified commands

The following checks were run successfully:

```bash
ssh professionalpractice@merah 'id; hostname'
ssh professionalpractice@raksasa 'ssh -o BatchMode=yes merah "id; hostname"'
ssh professionalpractice@raksasa 'cd ~/devel/professional-practice && go build -o bin/voicer ./cmd/voicer'
ssh professionalpractice@raksasa 'cd ~/devel/professional-practice && go build -o bin/vtt-generator ./cmd/vtt-generator'
ssh professionalpractice@raksasa 'cd ~/devel/professional-practice && ./bin/vtt-generator content/part-01/overview'
ssh professionalpractice@raksasa 'cd ~/devel/professional-practice && . ~/.config/professional-practice.env && ./bin/voicer -v content/part-01/overview/subtitles.vtt -o /tmp/profpractice-dryrun.wav --dry-run'
ssh professionalpractice@raksasa 'ssh -T github.com'
ssh professionalpractice@raksasa 'cd ~/devel/professional-practice && git ls-remote --heads origin main'
```

S3 cache access was also checked from `professionalpractice@raksasa` using the Go AWS SDK against the `audio-fragments` bucket.

## Remaining decisions

- If the GitHub key should be narrowed later, move it to a repository deploy key once repository settings allow deploy keys again.
- If scheduled jobs need AWS CLI diagnostics, install `awscli` on `raksasa`; the current Go renderer does not need it.
- Audio generation is run from `professionalpractice@raksasa` with `scripts/audio_generation_cron.sh`. The wrapper takes a lock, pulls the latest `main`, sources `/home/professionalpractice/.config/professional-practice.env`, and invokes `scripts/audio_generation_worker.py` for a bounded number of valid topics per run.
