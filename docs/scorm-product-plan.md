# SCORM Product Plan

Last checked: 2026-07-27.

## Product decision

The first paid release is **IT Professional Practice — Incident Triage Lab**, not
the whole eight-part course.

By the end, graduates and junior technologists should be able to classify
incoming work, assign a defensible initial priority, choose the next owner and
write a useful first customer update because professional service work starts
with judgement, not ticket vocabulary.

The release uses Part 1 because it is a coherent, narrated unit with a practical
artefact. It avoids marketing Parts 2–8 as a finished paid library while Part 8,
course-wide assessment, accessibility evidence, audio coverage and specialist
review remain incomplete.

## Included in version 1.0

- Seven Part 1 lessons in a deliberate learning order.
- 34 learner-visible slides and seven existing narration tracks.
- Slide transcripts and plain-text transcripts.
- Five workplace ticket scenarios with 20 scored decisions:
  - record classification;
  - initial priority;
  - next owner or escalation;
  - first customer-facing update.
- A printable intake and escalation worksheet.
- An individual and team facilitator guide.
- SCORM 1.2 launch, bookmark, suspend/resume, raw score and status reporting.
- A 70% pass mark. Completion requires reaching the end of all seven lessons and
  completing the lab.
- Standalone browser fallback when the LMS API is absent.

The package deliberately does not claim to be ITIL certification preparation,
does not include an exam voucher and does not depend on a ServiceNow account.

## Commercial offer

Store price: **A$490 including Australian GST** for one legal organisation.

The organisation licence should cover unlimited employees and LMS enrolments,
perpetual use of the purchased version and 12 months of package fixes and
updates. It should exclude resale, sublicensing, redistribution, public hosting,
client delivery, bespoke LMS integration and customisation.

This price is aligned with the store's existing organisation-licence model and
with current public single-module SCORM pricing. The product earns the price
through the assessed simulation, reporting, facilitator material and practical
worksheet rather than through slide count.

## Release gates

Repository-complete means:

1. `scripts/build_scorm.py` builds the package from the canonical HTML,
   narratives and media.
2. `scripts/validate_scorm_package.py` verifies the manifest, declared files,
   lesson/slide/audio counts, scenario structure and runtime reporting calls.
3. The package passes the local SCORM API browser harness for launch, bookmark,
   score, completion and resume.
4. Desktop and narrow-width visual checks pass for the module home, lessons,
   lab, result and worksheet.
5. The protected store bundle is staged outside the public web root and the
   shopfront's paid-download checks pass.

External release means:

1. Import the inner ZIP into Moodle, the reference LMS for this release.
2. Verify a learner can launch, leave, resume, complete, fail, retry and pass.
3. Confirm the LMS report shows the latest raw score and final status.
4. Create live and test Stripe prices for A$490 and install the matching
   shopfront environment variables.
5. Deploy the protected bundle and shopfront, then complete a paid-download smoke
   purchase.

Moodle 5.2.1 verification is complete for package version 1.0.2. A disposable
Moodle instance imported the ZIP as SCORM 1.2 with one launchable SCO. It
recorded an initial `incomplete` state without a premature score, lesson
bookmark `part-01/overview/index.html#4`, all seven lesson-completion records,
exit and resume, a 25-point failed assessment, and a successful retry with
`passed`, raw score 100 and grade 100. The test also confirmed that every
package-local lesson link names an explicit HTML file, which Moodle's
`pluginfile.php` delivery requires.

Moodle is the accepted reference-LMS gate for this release; a second SCORM Cloud
run is not required.

Narration transcription QA is also complete for all seven included lessons. A
durable CPU job on `raksasa` screened the audio with Whisper `large-v3`; five
lessons passed immediately at 0.0%–4.9% word error rate. The two apparent
outliers were rerun with `medium.en`, voice-activity detection and
previous-text conditioning disabled. They passed at 1.9% and 2.7%, confirming
that the first run's low-confidence trailing text was silence-driven ASR
hallucination rather than a narration defect. The reports are retained under
`output/transcribe/raksasa-20260726-large-v3/` and
`output/transcribe/raksasa-20260727-medium-en-vad/`.

Checkout can open after the protected bundle, live Stripe price and production
shopfront deployment have passed their smoke checks.

## Full-course roadmap

The later product should be a modular library rather than one enormous SCO:

1. Part 1: Incident Triage Lab.
2. Part 2: Change, SLA and CMDB decisions.
3. Part 3: DORA Metrics Lab.
4. Part 4: Postmortem Builder.
5. Part 5: Vendor/CRM Handoff Mapper.
6. Part 6: Startup IT Cost and Risk Lab.
7. Part 7: Data Stewardship Memo Tool, only after paid Indigenous review.
8. Part 8: Capstone evidence and defence, after the authored unit exists.

Each module should remain independently assignable, report its own score and
completion, and use structured scenario data so buyer-specific examples do not
fork the course source.

## Current primary references

- Moodle 5.2 SCORM activity documentation:
  <https://docs.moodle.org/502/en/SCORM>
- Moodle SCORM package requirements:
  <https://docs.moodle.org/502/en/SCORM_FAQ>
- W3C Web Content Accessibility Guidelines 2.2:
  <https://www.w3.org/TR/WCAG22/>
- PeopleCert marks usage policy:
  <https://www.peoplecert.org/-/media/folders-reorganized/legal-documents/qmepo13-marks-usage-policy.pdf>
