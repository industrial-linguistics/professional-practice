# Image Production Backlog

Last checked: 2026-07-06.

This is the working queue for reviewed image batches. Weekly automation may generate candidates, but it must publish them through the protected image review workflow before any asset is installed into course content.

## Status Values

- `backlog`: identified, but not ready for a batch.
- `ready`: enough context exists to draft a prompt or diagram spec.
- `prompt-drafted`: prompt/spec exists and is ready for review.
- `candidate-generated`: image candidates exist but have not been accepted.
- `accepted`: final asset is in the repo and referenced from slides.
- `blocked`: needs content, tool access, copyright/licensing clarity or a design decision.
- `superseded-html`: the need is now met by an HTML/CSS or inline-SVG diagram in the topic's `slides.html`; do not generate a raster for it.

## Weekly Review Protocol

1. Pull latest repo state and check whether slides/narratives changed near the queued assets.
2. Select 3-5 `ready` items, preferring assets that support validated or near-validated audio topics.
3. For each item, choose `diagram`, `mockup`, or `raster-illustration`.
4. Draft prompts/specs in the batch notes before generating any raster images.
5. Generate or draw candidates and render both the current slide and the proposed slide with the image inserted.
6. Register candidates with `scripts/image_review_register.py` and sync them to the protected merah review site.
7. Approve, reject or comment through the review site.
8. Let the daily raksasa processor install approved assets and append rejected/commented candidates to `image-review/rework-queue.md`.

## Next Batch Candidate Set

These are the best first candidates because they either support early course concepts or usable commercial previews.

| Batch | Status | Target | Type | Brief | Acceptance checks |
| --- | --- | --- | --- | --- | --- |
| 1 | superseded-html | `content/part-01/incident-vs-request/images/incident-request-decision.png` | diagram | Branch on service degradation, standard request path and urgency to separate incidents, requests, problems and changes. | Labels readable in 16:9 slide; no ITIL trademark-heavy wording; referenced from relevant slide. |
| 1 | superseded-html | `content/part-01/escalation-tiers/images/support-tier-swimlane.png` | diagram | Swimlane for L1 triage, L2 specialist support, L3 engineering/vendor escalation and feedback to knowledge base. | Shows handoffs and closure loop; not a generic org chart. |
| 1 | superseded-html | `content/part-03/dora-metrics/images/dora-current-target-radar.png` | diagram | Radar or quadrant showing deployment frequency, lead time, change failure rate and MTTR for current vs target state. | Uses directional labels clearly; avoids fake precision; works in greyscale. |
| 1 | superseded-html | `content/part-04/post-mortem-agenda/images/review-agenda-timeline.png` | diagram | Timeline of alert, acknowledge, restore, review, action ownership and follow-up verification. | Makes blameless review sequence obvious; includes business impact and action tracking. |
| 1 | ready | `content/part-06/day-zero-core-services/images/startup-day-zero-architecture.png` | diagram | Startup day-zero map covering domain, DNS, identity, email, chat, docs, devices, backups and support owner. | Uses Sarah/startup framing without decorative clutter; suitable as commercial preview. |

## Backlog

| Priority | Status | Target | Type | Brief | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | superseded-html | `content/part-01/incident-vs-request/images/incident-request-decision.png` | diagram | Incident/request/problem/change decision tree. | Implemented as HTML decision guide on slide 4 (2026-07-06). |
| 1 | superseded-html | `content/part-01/escalation-tiers/images/support-tier-swimlane.png` | diagram | L1/L2/L3 support handoff swimlane. | Implemented as HTML lane diagram on slide 4 (2026-07-06). |
| 1 | ready | `content/part-01/major-incident-drill/images/p1-incident-timeline.png` | diagram | P1 incident timeline with commander, comms, resolver and scribe. | Good second batch candidate. |
| 1 | ready | `content/part-01/servicenow-visual-guide/images/servicenow-ticket-lifecycle.png` | mockup | Clean ServiceNow-style ticket lifecycle mockup. | Avoid live screenshot dependency. |
| 1 | accepted | `content/part-02/slas-olas-kpis/images/sla-ola-kpi-stack.png` | diagram | Contract SLA, internal OLA and operational KPI stack. | Approved 2026-07-06; referenced from slide 2. |
| 1 | candidate-generated | `content/part-02/cmdb/images/cmdb-service-map.png` | diagram | CMDB dependency map across app, database, network, vendor, owner and service. | 2026-07-06 candidate rejected with fixes (text overflow, caption collision); see rework queue. |
| 1 | ready | `content/part-02/metrics-reporting-dashboards/images/itil-dashboard-mockup.png` | mockup | Operational dashboard mockup for ITIL metrics. | Use realistic but fictional numbers. |
| 1 | superseded-html | `content/part-03/dora-metrics/images/dora-current-target-radar.png` | diagram | DORA current vs target performance visual. | Implemented as HTML shift table on slide 2 (2026-07-06); radar form rejected. |
| 1 | superseded-html | `content/part-03/cicd-pipeline-design/images/cicd-flow.png` | diagram | Commit, build, test, package, deploy, observe, rollback. | Implemented as HTML flow on slide 4 (2026-07-06). |
| 1 | ready | `content/part-03/github-actions-workflows/images/workflow-dag.png` | diagram | GitHub Actions jobs, matrix, artifacts and approval gate. | Could derive from simple YAML example. |
| 1 | superseded-html | `content/part-04/post-mortem-agenda/images/review-agenda-timeline.png` | diagram | Post-incident review timeline. | Implemented as HTML timeline on slide 2 (2026-07-06). |
| 1 | ready | `content/part-04/rca-frameworks/images/five-whys-fishbone.png` | diagram | Five whys versus fishbone comparison. | Needs compact labels. |
| 1 | ready | `content/part-05/vendor-engagement-funnel/images/vendor-funnel-swimlanes.png` | diagram | Vendor lifecycle funnel with IT, finance, legal and MSP swimlanes. | Strong commercial asset. |
| 1 | ready | `content/part-05/salesforce-opportunity-walkthrough/images/salesforce-opportunity-map.png` | mockup | Salesforce-style object/process map. | Avoid copying Salesforce UI too closely. |
| 1 | ready | `content/part-05/contract-negotiation-basics/images/sla-clause-anatomy.png` | diagram | Anatomy of SLA clause: uptime, exclusions, credits, reporting, exit. | Topic currently lacks narratives. |
| 1 | ready | `content/part-06/day-zero-core-services/images/startup-day-zero-architecture.png` | diagram | Day-zero startup IT architecture. | First batch. |
| 1 | ready | `content/part-06/security-baselines-shoestring/images/security-baseline-grid.png` | diagram | Low-cost controls grid for MFA, password manager, MDM-lite, backups and logging. | Good for worksheet reuse. |
| 1 | ready | `content/part-06/startup-budgeting-finops/images/tool-stack-cost-chart.png` | diagram | Pre-seed, Series A and Series B stack cost step-up chart. | Use illustrative, labelled ranges. |
| 1 | ready | `content/part-06/capstone-remediation-roadmap/images/roadmap-30-60-90.png` | diagram | 30/60/90 remediation roadmap. | Supports validated topic. |
| 1 | ready | `content/part-07/maori-case-study/images/te-hiku-data-governance-map.png` | diagram | Community control, consent, vendors, storage and audit loops. | Needs cultural review sensitivity. |
| 2 | backlog | `content/part-02/continual-improvement/images/pdca-csi-loop.png` | diagram | PDCA/continual-service-improvement loop. | Lower priority because existing value-chain image covers adjacent idea. |
| 2 | superseded-html | `content/part-03/sre-error-budgets/images/error-budget-burn.png` | diagram | Error-budget burn chart linked to release freeze decision. | Implemented as inline SVG on slide 4 (2026-07-06). |
| 2 | ready | `content/part-03/trunk-vs-feature-branching/images/branching-comparison.png` | diagram | Trunk versus feature branch integration delay. | Supports validated topic. |
| 2 | backlog | `content/part-04/alert-correlation/images/alert-correlation-timeline.png` | diagram | Alert correlation timeline. | Needs topic slide alignment check. |
| 2 | backlog | `content/part-04/communicating-outcomes/images/stakeholder-update-template.png` | mockup | Outcome report sections for executives, customers and technical teams. | Could become worksheet. |
| 2 | backlog | `content/part-05/multi-stakeholder-buying-committees/images/buying-committee-map.png` | diagram | Buying committee map. | Hold until Part 5 narrative alignment improves. |
| 2 | backlog | `content/part-05/lead-scoring-opportunity-progression-renewal-alerts/images/lead-renewal-timeline.png` | diagram | CRM lifecycle timeline. | Hold until Part 5 narrative alignment improves. |
| 2 | backlog | `content/part-05/proof-of-concept-management/images/poc-scorecard.png` | mockup | POC scorecard. | Potential worksheet asset. |
| 2 | ready | `content/part-06/remote-first-reality-check/images/remote-onboarding-flow.png` | diagram | Remote onboarding/offboarding flow. | Strong operations asset. |
| 2 | accepted | `content/part-06/vendor-management-rhythms/images/vendor-scorecard-calendar.png` | diagram | Weekly/monthly/quarterly vendor cadence and scorecard. | Approved 2026-07-06; referenced from slide 7. |
| 2 | candidate-generated | `content/part-06/investor-due-diligence-prep/images/due-diligence-evidence-map.png` | diagram | Evidence map for policy, logs, access reviews, backups and board reporting. | 2026-07-06 candidate rejected with fixes (Data Room text overflow, badge spacing); see rework queue. |
| 2 | ready | `content/part-06/capstone-red-team-exercise/images/startup-maturity-radar.png` | diagram | Startup maturity radar. | Good visual for group exercise. |
| 2 | backlog | `content/part-07/foss-licensing-options/images/license-decision-tree.png` | diagram | License choice decision tree. | Needs legal wording caution. |
| 2 | backlog | `content/part-07/community-governance-structures/images/oss-governance-spectrum.png` | diagram | Maintainer to foundation governance spectrum. | Useful after Part 7 polish pass. |
| 2 | backlog | `content/part-07/balancing-openness-cultural-safety/images/cultural-safety-access-matrix.png` | diagram | Open/restricted/community-approved/embargoed data states. | Needs cultural review sensitivity. |
| 3 | backlog | `content/part-08/studio/images/capstone-evidence-pack.png` | diagram | Capstone evidence pack diagram. | Wait until Part 8 content exists. |

## Batch Notes

Add a dated subsection here after each weekly review.

### 2026-07-06 review sweep

All ten pending candidates (batches 2026-06-22, 2026-06-29 and 2026-07-06) were reviewed and dispositioned:

- **Approved and wired into slides:** `sla-ola-kpi-stack` (part-02/slas-olas-kpis slide 2), `vendor-scorecard-calendar` (part-06/vendor-management-rhythms slide 7 — moved from the text-dense slide 8).
- **Superseded by HTML/SVG diagrams in `slides.html`** (these had failed raster generation repeatedly since April with label collisions, dangling arrows or truncated text): `incident-request-decision`, `support-tier-swimlane`, `dora-current-target-radar`, `error-budget-burn`, `cicd-flow`, `review-agenda-timeline`. Shared diagram CSS lives in `COURSE_CSS` in `scripts/build_elearning.py`. Do not re-queue rasters for these.
- **Rejected, retry as images with fixes:** `cmdb-service-map`, `due-diligence-evidence-map` — right concept, but text overflowed boxes and badges collided with captions. Details in `image-review/rework-queue.md`.
- Stale candidate directories from superseded weekly batches (2026-04-27 through 2026-06-15) were removed from `state/image-review/candidates/`.
