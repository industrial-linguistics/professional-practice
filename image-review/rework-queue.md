# Image rework queue

Rejected and commented image candidates are appended here by the raksasa review processor.

## 2026-06-22-dora-current-target-radar

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-03/dora-metrics/images/dora-current-target-radar.png`
- Slide: slide 1
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: replaced by an HTML current-vs-target comparison in content/part-03/dora-metrics/slides.html slide 2. A radar is the wrong form when two axes are lower-is-better; the polygons contradict the legend, and the MTTR axis label was truncated to MTT. Do not regenerate.

Original prompt/spec:

```text
Create a slide-friendly DORA metrics comparison visual. Compare current state versus target state across deployment frequency, lead time for changes, change failure rate, and mean time to recovery. Use a clear radar or quadrant style with the direction of improvement labeled, avoid fake decimal precision, and ensure it still makes sense in greyscale. Keep the style clean, instructional, and easy to read from a lecture slide.
```

## 2026-06-22-incident-request-decision

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-01/incident-vs-request/images/incident-request-decision.png`
- Slide: slide 4
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: decision guide now implemented as an HTML diagram in content/part-01/incident-vs-request/slides.html slide 4. Do not regenerate this raster. Candidate defects for the record: duplicated yes/no labels on the first branch and a yes label colliding with box text.

Original prompt/spec:

```text
Create a clean educational decision tree for an IT professional practice slide. Start with 'Work arrives'. Branch first on 'Is service degraded or unavailable?'. If yes, go to 'Incident' with notes 'restore service fast' and 'track MTTR'. If no, branch on 'Is it a standard pre-approved ask?'. If yes, go to 'Service request' with notes 'catalog item' and 'workflow + approvals'. If no, branch on 'Is the root cause under investigation?'. If yes, go to 'Problem' with notes 'find cause' and 'prevent recurrence'. Otherwise go to 'Change' with notes 'planned risk review' and 'implementation window'. Use a neutral light background, bold readable labels, subtle color coding, and no vendor branding.
```

## 2026-06-22-support-tier-swimlane

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-01/escalation-tiers/images/support-tier-swimlane.png`
- Slide: slide 1
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: escalation swimlane now an HTML diagram in content/part-01/escalation-tiers/slides.html slide 4. Do not regenerate. Candidate defects: dangling connectors from Triage, Known fix? and Deep diagnostics boxes; feedback arrow overlapped the Close ticket box.

Original prompt/spec:

```text
Create a clean support-escalation swimlane diagram for a university IT operations slide. Show four horizontal lanes: User, Tier 1, Tier 2, Tier 3 or Vendor. Flow left to right from issue reported, triage, known-fix attempt, deeper diagnostics, engineering or vendor escalation, fix delivered, and knowledge article updated. Include the feedback loop from Tier 3 back to Tier 1 knowledge base. Use simple labels, gentle color accents, and a light editorial diagram style rather than corporate clip art.
```

## 2026-06-29-error-budget-burn

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-03/sre-error-budgets/images/error-budget-burn.png`
- Slide: slide 4
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: burn-down chart now an inline SVG in content/part-03/sre-error-budgets/slides.html slide 4. Do not regenerate. Candidate defects: four burn lines drawn instead of two, Caution zone label overdrawn by a line, zone bands misaligned with y-axis ticks.

Original prompt/spec:

```text
Diagram spec: create a 16:9 error-budget burn chart with time on the x-axis and budget remaining on the y-axis.
Include healthy, caution, and release-freeze zones plus two example burn lines that show why teams sometimes slow releases.
Add a compact decision-cues panel that explains what each zone means in plain language.
Keep labels clear for classroom projection and emphasize directional decisions rather than fake precision.
```

## 2026-07-06-cicd-flow

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-03/cicd-pipeline-design/images/cicd-flow.png`
- Slide: slide 4
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: pipeline flow now an HTML diagram in content/part-03/cicd-pipeline-design/slides.html slide 4. Do not regenerate. Candidate defects: stage arrows drawn through stage subtitles, Fast feedback and Build once badges overlapping caption text, rollback arrow floating without a path back to Deploy.

Original prompt/spec:

```text
Diagram spec: create a 16:9 CI/CD flow that shows commit, build, test, security checks, deploy and observe in order. Include a rollback path from production signals back to deploy, keep labels readable on a lecture slide, and emphasize fast feedback over tool-brand detail.
```

## 2026-07-06-cmdb-service-map

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-02/cmdb/images/cmdb-service-map.png`
- Slide: slide 2
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Retry as an image with fixes: concept and layout are right, but the Service Owner box collides with the Why it matters caption, the caption first word hides under the badge, and the Postgres DB side text overflows its box. Regenerate with text fitted inside shapes and more bottom margin; consider a distinct link style for the Service Owner record since it is ownership metadata, not a runtime dependency.

Original prompt/spec:

```text
Diagram spec: create a 16:9 CMDB service map linking one business service to application, database, network, vendor, and service-owner records. Use fictional but plausible labels, show dependencies clearly, and keep the emphasis on change and incident analysis rather than decorative infrastructure art.
```

## 2026-07-06-due-diligence-evidence-map

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-06/investor-due-diligence-prep/images/due-diligence-evidence-map.png`
- Slide: slide 1
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Retry as an image with fixes: concept approved, but the Data Room box text overflows its border (evidence spills outside), the Policies box text touches its bottom edge, and the Investor lens badge crowds the caption. Regenerate with text fitted inside shapes and clear badge-to-caption spacing.

Original prompt/spec:

```text
Diagram spec: create a 16:9 evidence map for startup investor diligence with a central data room linked to policies, control evidence, customer or vendor proof, and governance artifacts. Make it feel executive-ready, use no brand logos, and keep labels readable enough for classroom projection.
```

## 2026-07-06-review-agenda-timeline

- Requeued: 2026-07-06T12:46:25+00:00
- Status: rejected
- Target: `content/part-04/post-mortem-agenda/images/review-agenda-timeline.png`
- Slide: slide 2
- Reviewer: claude at 2026-07-06 12:46:15
- Comment: Superseded: post-incident timeline now an HTML diagram in content/part-04/post-mortem-agenda/slides.html slide 2. Do not regenerate. Candidate was close, but the Blameless rule badge overlapped the caption and hid its first word.

Original prompt/spec:

```text
Diagram spec: create a 16:9 post-incident review timeline showing alert, acknowledge, restore, impact review, root cause discussion, action ownership, and follow-up verification. Make the order unmistakable, include plain-language labels, and keep the tone blameless and operational.
```

## 2026-07-06-due-diligence-evidence-map

- Requeued: 2026-07-12T23:02:38+00:00
- Status: commented
- Target: `content/part-06/investor-due-diligence-prep/images/due-diligence-evidence-map.png`
- Slide: slide 1
- Reviewer: codex-image-review at 2026-07-06 11:35:22
- Comment: Codex public HTTPS POST smoke after CGI fix

Original prompt/spec:

```text
Diagram spec: create a 16:9 evidence map for startup investor diligence with a central data room linked to policies, control evidence, customer or vendor proof, and governance artifacts. Make it feel executive-ready, use no brand logos, and keep labels readable enough for classroom projection.
```

