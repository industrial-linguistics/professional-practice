# Audio Generation Plan

Last checked: 2026-04-25.

## Current audio inventory

The course has enough draft material to make a substantial audio job, but it is not ready for a bulk render.

| Part | Topics | Slides | Narratives | Estimated spoken minutes from existing narratives | Topics with slide/narrative parity |
| --- | ---: | ---: | ---: | ---: | ---: |
| Part 1 | 7 | 39 | 31 | 12.7 | 1 |
| Part 2 | 6 | 39 | 30 | 12.7 | 0 |
| Part 3 | 6 | 33 | 31 | 19.0 | 4 |
| Part 4 | 11 | 75 | 62 | 41.1 | 4 |
| Part 5 | 23 | 228 | 159 | 97.0 | 0 |
| Part 6 | 23 | 304 | 266 | 145.7 | 8 |
| Part 7 | 5 | 55 | 35 | 24.9 | 0 |
| Total | 81 | 773 | 614 | 353.1 | 17 |

Only `content/part-01/overview` currently has generated `audio.wav` and `final.mp4`.

The existing narratives total about 53,000 words. Depending on punctuation, speaker tags and model choice, that is roughly 320,000 to 380,000 text characters before the missing narratives are filled in. The complete course will likely be closer to 450,000 to 550,000 characters.

## Readiness gates

Do not bulk-generate audio until these gates pass:

1. Every topic selected for audio has the same number of Marp slides and narrative files.
2. `scripts/validate_content.py` passes for the topic.
3. `bin/vtt-generator` produces a valid `subtitles.vtt`.
4. `bin/voicer --dry-run` succeeds.
5. A cache lookup confirms whether each segment is already present in S3.

Current topics that pass slide/narrative parity:

- `content/part-01/overview`
- `content/part-03/devops-sre-platform-careers`
- `content/part-03/dora-metrics`
- `content/part-03/sre-error-budgets`
- `content/part-03/trunk-vs-feature-branching`
- `content/part-04/managing-emotions`
- `content/part-04/post-mortem-agenda`
- `content/part-04/post-mortem-culture`
- `content/part-04/rca-frameworks`
- `content/part-06/capstone-remediation-roadmap`
- `content/part-06/guest-speaker-ideas`
- `content/part-06/mock-vendor-evaluation-exercise`
- `content/part-06/pre-seed-tool-stack`
- `content/part-06/remote-talent-logistics-scale`
- `content/part-06/series-b-enterprise-stack`
- `content/part-06/shadow-it-low-code-experimentation`
- `content/part-06/startup-budgeting-finops`

## Throttled generation policy

The policy should protect shared ElevenLabs credits used by other projects, especially `../robopastor`.

Implemented first pass:

1. Generate no more than 10,000 estimated Professional Practice characters per UTC day.
2. Generate no more than 250,000 estimated Professional Practice characters per UTC month.
3. Treat 500,000 shared ElevenLabs characters per account period as the hard spending cap; rollover balance is reserve, not the scheduled-work budget.
4. Run at most one `voicer` process at a time on `professionalpractice@raksasa`.
5. Use a lock file such as `/home/professionalpractice/.cache/professional-practice-audio.lock`.
6. Stop immediately if the ElevenLabs subscription check fails, or if an API response indicates rate limiting, quota exhaustion or billing errors.
7. Never use `--force` for audio unless intentionally invalidating the cache.
8. Always use `VOICER_S3_BUCKET=audio-fragments` so successful segments are reusable.

The worker estimates spend from the topic narrative text before claiming work. This is deliberately conservative: cache hits may mean the actual ElevenLabs charge is lower, but the cron should not keep spending simply because the account has rollover credits.

## Queue design

Status: implemented as `scripts/audio_generation_worker.py`, called by `scripts/audio_generation_cron.sh` from `professionalpractice@raksasa`. The worker records state, estimated per-project usage events and budget-wait topics in `state/audio-worker-state.json`; per-topic logs live in `logs/audio-generation/`. Both paths are intentionally outside source control.

The original proposed queue shape was:

```text
state/audio-queue.tsv
topic_path    segment_index    checksum    chars    status    attempts    updated_at
```

Suggested statuses:

- `blocked-content`: slide/narrative mismatch or validation failure.
- `cache-hit`: available locally or in S3.
- `queued`: ready to synthesize.
- `rendering`: claimed by the active worker.
- `done`: rendered and uploaded to S3.
- `failed`: API, validation or assembly failure; include a short reason.

The worker should:

1. Rebuild Go tools.
2. Generate or refresh `subtitles.vtt`.
3. Run `voicer --dry-run` to list segments and checksums.
4. Mark S3 cache hits without using ElevenLabs.
5. Render queued segments until the daily character budget is exhausted.
6. Assemble topic audio only when all its segments are present.
7. Assemble video only when audio and slide images are present.

## Implementation notes

- The current `voicer` supports `--limit`, `--dry-run`, `--autopad`, `--autospeed`, local temp cache and S3 cache.
- The current `scripts/build_videos.sh` is topic-oriented, not budget-oriented. Add a separate slow worker rather than overloading this script.
- `cmd/voicer` currently checks S3 only during real generation. A dedicated `--cache-status-json` mode would make the slow worker cleaner and avoid synthesizing just to learn cache state.
- Keep generated `audio.wav`, `final.mp4`, slide PNGs and manifest output out of source control unless the distribution policy changes.
- `../inventory` records shared ElevenLabs account usage and documents the project reporting contract. The worker currently enforces a local Professional Practice budget plus a live ElevenLabs subscription cap; a later inventory integration can import `state/audio-worker-state.json` usage events or replace the live subscription check with a central budget service.

## First render order

Use this order to get useful previews with low risk:

1. Re-render `content/part-01/overview` only if needed to verify the full path.
2. Render the four valid Part 3 topics, because they are central to the pipeline/RCA assessment.
3. Render valid Part 4 topics needed for the A2 RCA story.
4. Render the valid Part 6 startup topics as commercial preview material.
5. Hold Part 5 and Part 7 until narrative counts are repaired.
