# Voicer Narration Plan

This note captures how to render narration audio with the `voicer` CLI from the Revoicer toolkit. The approach is based on the `voicer(1)` manual page bundled with the package.

## Environment preparation

1. Confirm that the Revoicer tools are installed (the package provides `/usr/bin/voicer`).
2. Ensure the ElevenLabs API key is available at `~/.elevenlabs.io` or pass `--key-file` with an explicit path.
3. Point the cache at Amazon S3 so we reuse synthesized segments between runs: set `VOICER_S3_BUCKET=s3://audio-fragments/` in the shell or supply `--s3-bucket s3://audio-fragments/` on the command line.

## Rendering workflow

1. Start with a WebVTT subtitle file that contains the narration script broken into cues.
2. Choose the desired narrator. The built-in `Greg` voice will be the default; switch to `Nichalia` when a different tone is required by passing `--voice Nichalia`.
3. Run `voicer --vtt narration.vtt --voice Greg --output build/greg-track.wav --format pcm_44100 --s3-bucket s3://audio-fragments/` to render Greg's take. Repeat with `--voice Nichalia` to produce the alternate read, writing to a different output file.
4. If we only need to voice ad-hoc lines, use `--say "Your text" --output snippet.wav --autopad` (implied) instead of supplying a `.vtt` file.
5. For long scripts, consider `--autopad` so that voicer simulates the final mix and adds trailing silence automatically. Use `--padding 5s` when an explicit buffer is needed.
6. Keep `--format` consistent with the target container (e.g., `pcm_44100` for WAV masters). MP3 masters can be produced with `--format mp3_44100`.
7. On re-runs, voicer will read cached segments either from the local temporary directory or from `s3://audio-fragments/`, accelerating subsequent renders.

## Additional tips

- Use `--limit` when iterating on early cues to avoid re-synthesizing the whole script.
- Enable `--autospeed` if any cues overflow their allotted time and need automatic time compression.
- Inspect the dry run plan with `--dry-run` before incurring synthesis costs.
