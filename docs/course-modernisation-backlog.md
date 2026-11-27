# Course modernisation backlog

The initial inventory on 27 November 2026 found 81 topics and 735 slides, two standalone animated explainers, and the assessed Incident Triage Lab in the Part 1 SCORM package. Part 8 has an outline, a practice artefact and a textbook introduction. The checks below seed the queue. The complete freshness and production audit is open.

For each run, record the source revision, topics and surfaces checked, primary sources and check dates, and the next topics to inspect. Keep work unchecked until its specified result is verified. Track a film or exercise that spans runs by its next milestone.

## Content to refresh

- [ ] **F01 ITIL edition and transition.** The Part 1 overview [textbook](../content/part-01/overview/textbook.md) calls ITIL 4 the current edition. Narrative 02 also implies it is the current form. Explain the phased introduction of ITIL (Version 5) while keeping the lesson's explicit ITIL 4 scope. Check adjacent certification references and narration provenance. Verified 27 November 2026 against the [PeopleCert transition FAQ](https://www.peoplecert.org/help-and-support/faq-itil).
- [ ] **F02 DORA measures.** [Part 3 slide 2](../content/part-03/dora-metrics/slides.html) and its [narratives](../content/part-03/dora-metrics/narratives) teach four measures and use broad MTTR terminology. Bring them into line with the [textbook](../content/part-03/dora-metrics/textbook.md), which explains five measures and the historical terms. Check the quiz and nearby references, keep the trend comparison, and use worked rates or explicitly fictional examples. Verified 27 November 2026 against [DORA's definitions](https://dora.dev/guides/dora-metrics/).
- [ ] **F03 Complete the first freshness audit.** Inspect the rest of Parts 1–8 for dated claims, broken instructions or links, and disagreements among slides, narrations, the textbook and exercises. Prioritise vendor and browser behaviour, cloud pricing, credentials, and time sensitive policy or legal references. Record exact source evidence before making a change.

## Explainers and interactive tools

- [ ] **M01 Embed the existing Error Budgets & SLOs explainer.** Integrate the [existing explainer](../explainers/error-budget/index.html) in its [Part 3 lesson](../content/part-03/sre-error-budgets/slides.html). Use its existing timed scene, narration and captions. Verify play, pause, captions and the transcript on the generated site. Keep the private master private. This establishes the delivery path for subsequent videos.
- [ ] **M02 Build a DORA metrics lab.** After F02, add an HTML exercise to [DORA Metrics](../content/part-03/dora-metrics/slides.html). Give learners a small fictional deployment log with commits, failures, recovery and unplanned fixes. Ask them to calculate and interpret metrics, then choose one improvement and compare it with a worked answer. Verify arithmetic and the retry path.
- [ ] **M03 Animate Sarah's market day outage.** Storyboard a short Blender explainer from [Business Continuity for Small Teams](../content/part-06/business-continuity-small-teams/slides.html), slides 3–5. Show where the connection fails, why payments and recipes are affected together, and what changes when the shop has a rehearsed fallback. Use a realistic fictional shop layout and generic devices. First milestone is a timed storyboard and rough frames for both operating states. See B01 for a possible establishing shot.
- [ ] **M04 Practise a change decision.** Build an HTML change advisory scenario for [Change Enablement vs Release Management](../content/part-02/change-vs-release/slides.html). Ask learners to approve, defer or request evidence for a change, and show how dependencies, timing and rollback readiness affect each answer.
- [ ] **M05 Reconstruct an incident.** Turn [Alert Correlation](../content/part-04/alert-correlation/slides.html) into an exercise in ordering evidence, spotting a timestamp discrepancy and marking which causal claims are still uncertain.
- [ ] **M06 Rehearse a discovery call.** Use the [Part 5 discovery call lesson](../content/part-05/discovery-call-techniques/slides.html) for a fictional stakeholder conversation with a rubric. Start with typing and scripted branches. Add browser model replies and optional speech when they improve the rehearsal.
- [ ] **M07 Complete the first production audit.** Consider every topic and part-level activity. Record opportunities with distinct learner outcomes. Keep specialist clearance for Part 7 and use the authored Part 8 sources when they are ready.

## B-roll requests

Use one entry per shot. Include its ID, film and storyboard beat or timecode, why the insert is useful, target duration and aspect ratio, action and camera instructions, continuity constraints, a copy-ready Gemini prompt, expected return filename, and status. Use `proposed`, `ready for Gemini`, `needs Greg`, `received` and `used` or `dropped`. Send the ready prompt and filename in ChatGPT when the operator marks `needs Greg`. Keep returned media in the film's working directory until verified, then record the accepted clip's provenance and storage in the film's release evidence. [Gemini video instructions](https://support.google.com/gemini/answer/16126339).

### B01 Market day opening

- **Status:** proposed. Confirm against the M03 storyboard before requesting generation.
- **Beat and purpose:** opening, roughly 00:00–00:04. Establish the stall before the film moves inside to show the payment and recipe dependencies in Blender.
- **Delivery:** 16:9 landscape, about six usable seconds with time to trim, MP4 `market-day-B01.mp4`. Crop or trim to fit. The explainer provides the audio.
- **Gemini prompt:** A realistic documentary establishing shot of a fictional Australian weekend farmers market before opening. Early morning overcast light. A small meal-prep stall under a cream canopy with muted blue table coverings, closed food containers and a plain card terminal near the right edge. The camera moves slowly forward from the public walkway, and a worker out of focus arranges containers. One continuous landscape shot for about six seconds, with steady exposure and natural movement. Keep faces indistinct. Use no legible text, shop names, logos, dialogue or music. Match the final Blender storyboard's canopy, table position and colours if a reference frame is supplied.
