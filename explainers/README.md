# Animated explainers

An explainer is a short narrated animation built from a lesson's existing narration. It is real motion graphics rather than slide screenshots held under audio. The first is `error-budget/`, from Part 3's "Error Budgets & SLOs" (narratives 01, 03 and 04, about 90 seconds). The second is `p1-outage/`, a trailer for the Incident Triage Lab.

Explainers are standalone. They are not yet part of the course player, the SCORM package or the textbook.

## How it works

`error-budget/scene.js` exposes `render(t)`, which draws the frame for narration time `t` in seconds. In a browser the page plays `narration.mp3` and draws the frame for the audio's current time. For video, `scripts/render_explainer.cjs` steps `t` one frame at a time in headless Chromium and joins the frames to the same audio with ffmpeg.

| Path | Purpose |
|---|---|
| `error-budget/index.html`, `scene.css`, `scene.js` | The page and the scene. No libraries. |
| `error-budget/script.json` | Which narratives are voiced, the model for each speaker, and per-line pronunciation hints. |
| `error-budget/narration.mp3`, `narration.json`, `narration.js`, `captions.vtt` | The current take, its word timings, the compact copy the page loads, and captions. |
| `error-budget/authored.json` | Word timings of the first take, which the scene's beat times were written against. |
| `error-budget/release.json` | The tracking record for the rendered film: hash, size, duration, source hash, storage. |
| `scripts/explainer_narration.py` | Voices the lines with ElevenLabs and writes the narration files. |
| `scripts/render_explainer.cjs` | Stills and MP4. Requires Playwright and ffmpeg. |
| `scripts/publish_explainer.py` | Writes `release.json` and stores the film in S3. |

## Commands

```sh
python3 -m http.server -d explainers/error-budget 8000        # then open http://localhost:8000/
node scripts/render_explainer.cjs --stills 4.2,8.6,18.6,40.6,47.5,74.6,81.5
node scripts/render_explainer.cjs                              # output/explainers/error-budget.mp4
python3 scripts/publish_explainer.py error-budget              # update release.json and show the storage plan
python3 scripts/publish_explainer.py error-budget --upload     # store the master; add --create-bucket the first time
python3 scripts/publish_explainer.py error-budget --fetch      # get the recorded film back, hash-checked
```

The MP4 and its frames go to `output/`, which git ignores. The master belongs in S3 under a name that contains its hash; `release.json` in git says which file that is.

## Re-voicing needs no re-timing

The beat times in `scene.js` are in authored time, the timeline of the first take. Every later take carries a `warp` table in `narration.js` that maps its word times back to the authored ones, and the scene looks up authored time before it draws. Changing a model or a voice setting therefore needs only:

```sh
python3 scripts/explainer_narration.py error-budget
node scripts/render_explainer.cjs
```

This holds while the words are unchanged. If a line's wording changes, that line falls back to matching its start and end only, and its beats may need adjusting.

The narration audio is committed here, unlike lesson audio, so the page and the render always have the take the timings describe. Line takes are cached in `output/explainers/error-budget-takes/` and stored in S3 by the publish script; with them, one line can be re-recorded without paying for the rest.

## Voices

Anna is voiced on `eleven_v4`. Greg is voiced on `eleven_multilingual_v2`, because v4 at its defaults renders his voice clone about three semitones high (median pitch about 120 Hz against 88 to 101 Hz on v2). The alternative is v4 with `"voice_settings": {"Greg": {"clone_strength": 1.0}}` in `script.json`, which measured 101 Hz. The API has no pitch control; `clone_strength` is v4-only and is rejected on v2.

Line 8 is voiced with a comma after "SLO" (see `script.json`). Without it v4 ran "SLO if" together and a transcription check heard "SNLO". The displayed text is the authored narration.

## What is real and what is illustrative

- 99.9% availability allows 8.76 hours of downtime in a 365-day year and 43.2 minutes in a 30-day month. The film shows "about 9 hours" and "43 minutes", matching the narration's "roughly nine hours" and "about forty minutes".
- The month of incidents, the second month's burn (33 of 43 minutes used in 8 of 30 days, about 2.9 times the even rate) and the lever projections are illustrative. The closing credit says so.
- Moving the SLO from 99.9% to 99.5% raises a 30-day budget from 43.2 to 216 minutes.
- The closing line is the lesson's own slide text.

## P1 outage trailer (`p1-outage/`)

An 80-second trailer for the Incident Triage Lab, the Part 1 package. It follows the same pattern as `error-budget/`; pass `--name p1-outage` to the render script and `p1-outage` to the narration and publish scripts.

- The script is `p1-outage/script.md`, a new two-speaker script written for the trailer. It draws on the lesson "Major Incident Management Drill" (narratives 03, 06 and 07) and keeps several of its sentences word for word or nearly so.
- Product claims come from `CURRENT_STATUS.md` and `scripts/build_scorm.py`: seven narrated lessons, a five-ticket assessed simulation, SCORM completion, score and resume reporting, a 70% pass mark, a worksheet and a facilitator guide. The seven lesson titles follow `TOPIC_ORDER`.
- The five ticket titles, their queue times and the four worked answers for the first ticket are taken from `scorm/incident-triage/scenarios.json`. The "Next owner" answer is shortened on screen.
- The outage itself is an illustrative scenario: the clock times, order and alert counts, region names, alert names, pressure messages and incident-record entries are invented for the film. A label says so during those scenes and the closing credit repeats it.
- Anna is on `eleven_v4` and Greg on `eleven_multilingual_v2`. All nine lines passed a transcription check on the first take.

## Fonts

The scene asks for Inter, which this repository does not bundle. A machine without Inter falls back to Avenir or the system sans-serif, and labels may shift slightly.
