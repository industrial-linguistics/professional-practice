# Media and Diagram Plan

Last checked: 2026-04-25.

## Current media state

- Slide decks found: 81.
- Slide count across decks: 773.
- Narrative files found: 614.
- Current generated audio/video: only `content/part-01/overview` has checked-in `audio.wav` and `final.mp4`.
- Source images currently committed:
  - `content/part-01/value-chain/images/service-value-chain-continual-improvement.png`
  - `content/part-02/change-vs-release/images/itil-minor-change.png`
- Topics with matching slide and narrative counts: 17.

The largest immediate blocker for audio and video is not imagery. It is slide/narrative alignment: most topics have more slides than narrative files, and two Part 5 topics have no narratives at all.

## QR code decision

The Claude Code course embeds tiny QR codes in the Beamer slides through a `\slideid{...}` macro. The e-learning extractor scans the rendered PDF at high DPI, reads each QR code, and uses that stable ID to associate page images and text with audio directories. That is valuable when the PDF is the extraction source and slide order can drift.

This repository has a different source of truth: Marp markdown lives next to per-topic narrative files. The renderer already knows the topic path and slide order before PDF extraction. For the core audio/video pipeline, QR codes are not needed.

Recommended decision:

1. Do not add QR codes as a prerequisite for audio generation.
2. Add stable slide IDs to an audio manifest first, using a path-derived form such as `part-03-dora-metrics-004`.
3. Add tiny QR overlays only in exported run sheets, PDFs or e-book pages once there is a public URL pattern for per-slide audio or per-topic lesson pages.
4. If QR is added later, make it a generated overlay in the export layer, not hand-authored markup in every slide.

## Priority diagrams and images

The structured production queue is maintained in [image-production-backlog.md](image-production-backlog.md).

Use diagrams where the concept is process, dependency, decision, or role ownership. Use screenshots or realistic mockups where the concept is tool literacy.

| Priority | Location | Asset | Purpose |
| --- | --- | --- | --- |
| 1 | `content/part-01/incident-vs-request/images/incident-request-decision.png` | Decision tree | Show when work is an incident, service request, problem or change. |
| 1 | `content/part-01/escalation-tiers/images/support-tier-swimlane.png` | L1/L2/L3 handoff swimlane | Make escalation paths and ownership visible. |
| 1 | `content/part-01/major-incident-drill/images/p1-incident-timeline.png` | Major incident timeline | Anchor commander, comms, resolver and scribe roles. |
| 1 | `content/part-01/servicenow-visual-guide/images/servicenow-ticket-lifecycle.png` | ServiceNow ticket mockup | Show states from logging to closure without relying on live sandbox screenshots. |
| 1 | `content/part-02/slas-olas-kpis/images/sla-ola-kpi-stack.png` | SLA/OLA/KPI hierarchy | Explain contract, internal commitment and measurement layers. |
| 1 | `content/part-02/cmdb/images/cmdb-service-map.png` | CMDB service dependency map | Show app, database, network, vendor, owner and affected service links. |
| 1 | `content/part-02/metrics-reporting-dashboards/images/itil-dashboard-mockup.png` | Dashboard mockup | Turn reporting from abstract KPIs into operational decisions. |
| 1 | `content/part-03/dora-metrics/images/dora-current-target-radar.png` | DORA radar or quadrant | Compare current and target delivery performance. |
| 1 | `content/part-03/cicd-pipeline-design/images/cicd-flow.png` | Commit-to-production pipeline | Show build, test, package, deploy, observe and rollback. |
| 1 | `content/part-03/github-actions-workflows/images/workflow-dag.png` | GitHub Actions job graph | Explain triggers, jobs, matrix builds and approval gates. |
| 1 | `content/part-04/post-mortem-agenda/images/review-agenda-timeline.png` | Post-incident review timeline | Show the order of facts, impact, causes, actions and comms. |
| 1 | `content/part-04/rca-frameworks/images/five-whys-fishbone.png` | RCA comparison | Show when to use five whys versus fishbone analysis. |
| 1 | `content/part-05/vendor-engagement-funnel/images/vendor-funnel-swimlanes.png` | Funnel with IT/legal/finance/MSP swimlanes | Make the vendor lifecycle cross-functional. |
| 1 | `content/part-05/salesforce-opportunity-walkthrough/images/salesforce-opportunity-map.png` | Salesforce object/process mockup | Show lead, account, contact, opportunity, quote and renewal links. |
| 1 | `content/part-05/contract-negotiation-basics/images/sla-clause-anatomy.png` | Contract clause anatomy | Show uptime, exclusions, credits, reporting and exit terms. |
| 1 | `content/part-06/day-zero-core-services/images/startup-day-zero-architecture.png` | Day-zero startup IT map | Show domain, identity, devices, comms, docs, backups and support. |
| 1 | `content/part-06/security-baselines-shoestring/images/security-baseline-grid.png` | Low-cost control grid | Prioritise MFA, password manager, MDM-lite, backups, logging and incident comms. |
| 1 | `content/part-06/startup-budgeting-finops/images/tool-stack-cost-chart.png` | SaaS/cloud spend chart | Show pre-seed, Series A and Series B cost step-ups. |
| 1 | `content/part-06/capstone-remediation-roadmap/images/roadmap-30-60-90.png` | 30/60/90 remediation roadmap | Give the capstone an executive-ready output shape. |
| 1 | `content/part-07/maori-case-study/images/te-hiku-data-governance-map.png` | Data governance and access map | Show community control, consent, vendors, storage and audit loops. |
| 2 | `content/part-02/continual-improvement/images/pdca-csi-loop.png` | PDCA/continual improvement loop | Reinforce improvement as a cycle, not a one-off. |
| 2 | `content/part-03/sre-error-budgets/images/error-budget-burn.png` | Error-budget burn chart | Connect SLOs to release decisions. |
| 2 | `content/part-03/trunk-vs-feature-branching/images/branching-comparison.png` | Branching comparison | Show integration delay and merge risk visually. |
| 2 | `content/part-04/alert-correlation/images/alert-correlation-timeline.png` | Alert-to-incident timeline | Show how duplicate alerts become one incident story. |
| 2 | `content/part-04/communicating-outcomes/images/stakeholder-update-template.png` | Outcome report mockup | Model executive, customer and technical update sections. |
| 2 | `content/part-05/multi-stakeholder-buying-committees/images/buying-committee-map.png` | Stakeholder map | Show champion, blocker, economic buyer, security and legal. |
| 2 | `content/part-05/lead-scoring-opportunity-progression-renewal-alerts/images/lead-renewal-timeline.png` | CRM lifecycle timeline | Connect lead scoring, stage movement, health score and renewal alert. |
| 2 | `content/part-05/proof-of-concept-management/images/poc-scorecard.png` | POC success scorecard | Make acceptance criteria concrete. |
| 2 | `content/part-06/remote-first-reality-check/images/remote-onboarding-flow.png` | Remote onboarding/offboarding flow | Show HRIS, device logistics, IAM, payroll and access review. |
| 2 | `content/part-06/vendor-management-rhythms/images/vendor-scorecard-calendar.png` | Cadence and scorecard diagram | Show weekly, monthly and quarterly vendor management rhythms. |
| 2 | `content/part-06/investor-due-diligence-prep/images/due-diligence-evidence-map.png` | Evidence map | Link policy, logs, access reviews, backups and board reporting. |
| 2 | `content/part-06/capstone-red-team-exercise/images/startup-maturity-radar.png` | Maturity radar | Give red-team findings a simple visual structure. |
| 2 | `content/part-07/foss-licensing-options/images/license-decision-tree.png` | License decision tree | Guide MIT/Apache/GPL/dual-license decisions. |
| 2 | `content/part-07/community-governance-structures/images/oss-governance-spectrum.png` | Governance spectrum | Show maintainer, core team, foundation and commercial steward models. |
| 2 | `content/part-07/balancing-openness-cultural-safety/images/cultural-safety-access-matrix.png` | Access matrix | Show open, restricted, community-approved and embargoed data states. |
| 3 | `content/part-08/studio/images/capstone-evidence-pack.png` | Capstone evidence pack diagram | Help teams organise final pitch evidence across the course outcomes. |

## Production notes

- Prefer SVG or Mermaid for abstract process diagrams that need labels and revision.
- Prefer PNG screenshots or realistic UI mockups for ServiceNow, Salesforce, GitHub Actions and dashboards.
- Avoid using real vendor screenshots if licensing or login state is unclear; clean mockups are usually safer and easier to localise.
- Store per-topic images under `content/part-XX/topic-name/images/` and reference them with relative Markdown links from `slides.md`.
