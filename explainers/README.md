# Animated explainers

An explainer is a short narrated animation built from a lesson's existing narration. It is real motion graphics rather than slide screenshots held under audio. The first is `error-budget/`, from Part 3's "Error Budgets & SLOs" (narratives 01, 03 and 04, about 95 seconds).

Explainers are standalone. They are not yet part of the course player, the SCORM package or the textbook.

## How it works

`error-budget/scene.js` exposes `render(t)`, which draws the frame for narration time `t` in seconds. In a browser the page plays `narration.mp3` and draws the frame for the audio's current time. For video, `scripts/render_explainer.cjs` steps `t` one frame at a time in headless Chromium and joins the frames to the same audio with ffmpeg.

| Path | Purpose |
|---|---|
| `error-budget/index.html`, `scene.css`, `scene.js` | The page and the scene. No libraries. |
| `error-budget/script.json` | Which narratives are voiced, the model, and any per-line pronunciation hints. |
| `error-budget/narration.mp3`, `narration.json`, `narration.js` | The recorded take, its word timings, and the compact copy the page loads. |
| `scripts/explainer_narration.py` | Voices the lines with ElevenLabs and writes the three narration files. |
| `scripts/render_explainer.cjs` | Stills and MP4. Requires Playwright and ffmpeg. |

## Commands

```sh
python3 -m http.server -d explainers/error-budget 8000        # then open http://localhost:8000/
node scripts/render_explainer.cjs --stills 4.2,8.6,21.8,43.6,53,79.6,87.6
node scripts/render_explainer.cjs                              # output/explainers/error-budget.mp4
```

The MP4 and its frames go to `output/`, which git ignores.

## Re-voicing

The narration audio is committed here, unlike lesson audio, because the beat times in `scene.js` belong to this exact take. `python3 scripts/explainer_narration.py error-budget` rebuilds the narration from cached line takes in `output/explainers/error-budget-takes/`. Without that cache it records new takes, which costs credits and changes every timing, so the scene then needs re-timing against the word times in `narration.json`.

Line 8 is voiced with a comma after "SLO" (see `script.json`). Without it the model ran "SLO if" together and a transcription check heard "SNLO". The displayed text is the authored narration.

## What is real and what is illustrative

- 99.9% availability allows 8.76 hours of downtime in a 365-day year and 43.2 minutes in a 30-day month. The film shows "about 9 hours" and "43 minutes", matching the narration's "roughly nine hours" and "about forty minutes".
- The month of incidents, the second month's burn (33 of 43 minutes used in 8 of 30 days, about 2.9 times the even rate) and the lever projections are illustrative. The closing credit says so.
- Moving the SLO from 99.9% to 99.5% raises a 30-day budget from 43.2 to 216 minutes.
- The closing line is the lesson's own slide text.

## Fonts

The scene asks for Inter, which this repository does not bundle. A machine without Inter falls back to Avenir or the system sans-serif, and labels may shift slightly.
