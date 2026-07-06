# E-learning Roadmap

Last checked: 2026-07-06.

The current Professional Practice output is not yet an e-learning course. It is
mostly a content repository plus a simple public run-script index. The sibling
repos show two mature patterns worth importing:

- `../decision-grade` has a separate self-paced delivery tree, transcript
  controls, course-wide Q&A context, SCORM packaging, MP4 export and production
  smoke tests.
- `../claude-code-course` has per-slide courseware pages, audio controls,
  transcript cards, progress UI, course/locale/theme variants, SCORM packages,
  EPUB/ebook output and transcript validation.

## Current State

- Source content lives in `content/part-XX/topic/slides.html` and
  `narratives/`.
- The e-learning pipeline builds `output/elearning/` and `output/site/` from
  HTML slide source.
- The textbook pipeline builds a LaTeX project under `textbook/`, with
  `main.pdf` for A4 student printing and `main-amazon.pdf` for 6x9 inch
  print-on-demand checks.
- The video pipeline can render HTML slides to PNG, VTT subtitles, narration
  audio and topic MP4s.
- `website/index.html` is a plain list of run-script links.
- `scripts/generate_run_sheets_html.sh` converts PDFs to basic HTML.
- `output/elearning/` includes transcript pages, transcript overlay controls,
  progress controls and a course-wide `course-corpus.json`.
- SCORM packaging and quiz export are still future work.

## Target Shape

Professional Practice should build three delivery surfaces from the same source
content:

- `output/web/`: instructor-facing deck/run-sheet material.
- `output/elearning/`: self-paced learner pages with slide preview, audio,
  transcript, progress, resources and topic navigation.
- `textbook/`: LaTeX textbook source plus A4 and print-on-demand PDFs.
- `output/scorm/`: LMS-ready SCORM packages assembled from the e-learning tree.

Generated output should then be assembled into `output/site/` and deployed from
there. The existing `website/` tree can become either a generated compatibility
copy or be retired once the new output tree is stable.

## Imported Capabilities

| Capability | Source pattern | Professional Practice version |
| --- | --- | --- |
| Separate presentation and self-paced output | `decision-grade/build/build_variants.py --delivery elearning` | `scripts/build_elearning.py` emits `output/elearning/part/topic/`. |
| Learner runtime | `decision-grade/shared/deck.js` and `deck.css` | Shared CSS/JS supports topic navigation, progress, audio, transcript overlay and local-model Q&A gating. |
| Transcript pages | `decision-grade/build/build_transcripts.py` | `transcript.html` and `transcript.txt` are generated from each topic's narratives and slide text. |
| Course corpus | `decision-grade/build/build_course_corpus.py` | `course-corpus.json` is generated from all topic slide text and narratives. |
| Per-slide courseware | `claude-code-course/e-learning/generate_web_version.py` | Produce one topic landing page plus per-slide pages for long topics if needed. |
| Exercises and commands | Claude Code course `commands.yaml` panels | Add optional per-topic `resources.yaml` for commands, links, worksheets and activity instructions. |
| SCORM packaging | both sibling repos | Package each part and selected topic bundles from `output/elearning/`. |
| MP4 export | `decision-grade/build/render_video.py` plus current `build_videos.sh` | Keep as an optional manual output; do not make MP4s part of the default learner-facing course surface. |
| Validation | Decision Grade node/python tests and Claude transcript checks | Add smoke tests for generated transcript links, audio presence, SCORM manifest and malformed HTML. |

## Phased Work

### Phase 1: Make the public output look like courseware

- Create `scripts/build_elearning.py`.
- Generate `output/elearning/index.html` with part cards, topic cards, status
  markers and links to audio, transcripts and run sheets.
- Generate one learner page per topic using HTML slide source and narratives.
- Add a shared `output/elearning/assets/course.css` and `course.js`.
- Replace the current plain `website/index.html` generation with an
  `output/site/` assembly step.

This is the highest-return first step because it changes the visible product
without requiring new narration spend.

### Phase 2: Transcript and audio learner controls

- Generate `transcript.html` and `transcript.txt` per topic from
  `narratives/` and `subtitles.vtt`.
- Add transcript-as-subtitle controls to topic pages.
- Add a durable progress marker using local storage.
- Publish existing `audio.wav` and `subtitles.vtt` when present.

### Phase 3: LMS packaging

- Add `scripts/build_scorm.py` using the e-learning tree as the source.
- Package each part as a SCORM 1.2 module.
- Include `imsmanifest.xml`, topic HTML, shared assets, transcripts, subtitles,
  audio, subtitles and quizzes.
- Add local package validation that checks manifest entries exist in the zip.

### Phase 4: Practice surfaces

- Add small browser exercises for high-value topics:
  - incident triage and escalation
  - change request/CAB simulation
  - DORA metric interpretation
  - post-incident action tracking
  - vendor/CRM lifecycle mapping
- Store scenarios as data files so the exercises are editable course content,
  not one-off pages.

### Phase 5: Course-wide context and quality gates

- Generate `course-corpus.json` from slide text, narratives, quiz questions and
  activity instructions.
- Add optional local-model Q&A in browsers that support it.
- Add tests that verify e-learning pages expose transcript links, no missing
  assets, usable keyboard navigation, SCORM packages and video links.
- Add narration round-trip validation for new or changed audio.

## Implementation Notes

- Prefer generated HTML from structured repo content over PDF-to-HTML output.
  PDF conversion is useful for compatibility, but it produces weak courseware.
- Keep images in the existing review workflow. Approved images should appear in
  e-learning pages only after the daily processor installs them into
  `content/.../images/...`.
- Keep `content/` as the source of truth. `output/` and `website/` should remain
  generated surfaces.
- Do not copy Decision Grade's token/variant system until there is a concrete
  Professional Practice customer variant. The immediate need is delivery
  quality, not industry substitution.
