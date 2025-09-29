---
marp: true
title: Capstone: Red Team Your Friend's Startup
---

# Capstone: Red Team Your Friend's Startup
*Group exercise structure and maturity mapping*

---

## Capstone objectives
- Stress-test a 15-person startup's toolchain, culture and vendor choices without breaking production.
- Practice red-team thinking, blue-team response and facilitation skills in a psychologically safe setting.
- Map findings to an actionable maturity model so leaders leave with a prioritized remediation backlog.
- Showcase cross-functional roles—from fractional CTO to customer success—needed to sustain improvements.

---

## Scenario setup
- Sarah's marketplace startup: 15 staff, a mix of contractors and founders shipping weekly product updates.
- Stack: managed Kubernetes cluster, GitHub Actions CI/CD, Google Workspace, Notion, HubSpot and Stripe.
- Third parties: fractional SOC provider, MSP handling endpoints, offshore data labeling partner.
- Known pain points: ad-hoc onboarding, shadow SaaS, limited incident rehearsal and compliance debt.

---

## Team structure & logistics
- Participants form pods of 5–6: red-team analysts, blue-team responders, a business stakeholder and a scribe.
- 90-minute block: 20-minute recon, 30-minute incident drill, 25-minute debrief, 15-minute report-out prep.
- Facilitator provides injects, timeboxes discussions and keeps the tone curious rather than accusatory.
- Shared workspace includes architecture diagram, SaaS inventory, contract excerpts and customer personas.

---

## Phase 1 — Recon & hypothesis building
- Red team maps the startup's assets, data flows, trust boundaries and third-party dependencies.
- Identify top three attack vectors (credential reuse, misconfigured S3, vendor breach) with supporting evidence.
- Draft "assume breach" scenarios that articulate the business impact for sales, support and engineering leaders.
- Scribe captures questions for the facilitator to answer or park for later research.

---

## Phase 2 — Simulated incident drill
- Facilitator triggers a chosen scenario: e.g., compromised GitHub token leading to tampered container images.
- Blue team walks through detection sources, containment steps, communication cadences and legal escalations.
- Injects add twists: incident overlaps with product launch, MSP lead is on leave, or SOC ticket queue is full.
- Encourage practicing customer updates, board briefs and postmortem draft outlines in real time.

---

## Phase 3 — Debrief & maturity mapping
- Teams grade the startup across people, process, technology and governance dimensions using 1–5 scale.
- Tie observations to evidence: outdated runbooks, missing tabletop cadence, single approver for releases.
- Prioritize remediation backlog: quick wins (MFA gaps), medium-term (vendor contract reviews), strategic plays (platform observability).
- Capture leadership asks: budget, headcount or policy changes needed to support improvements.

---

## Maturity model cheat sheet
- **Level 1 — Ad hoc:** hero-driven fixes, no defined playbooks, limited logging or third-party oversight.
- **Level 2 — Emerging:** basic runbooks, partial MFA rollout, informal retros but inconsistent follow-through.
- **Level 3 — Scaling:** quarterly tabletop drills, defined SLAs, vendor scorecards, baseline observability.
- **Level 4 — Measured:** automated controls, resilience OKRs, integrated risk dashboards, dedicated budget.
- **Level 5 — Optimized:** continuous assurance, proactive purple teaming, shared outcomes with partners.

---

## Deliverables & facilitation cues
- Pod outputs: risk map, attack narrative, maturity scores, top-five remediation backlog with owners and timelines.
- Encourage visual artifacts—journey maps, swimlanes, heat maps—to anchor executive conversations.
- Debrief using "start, stop, continue" format to surface culture shifts alongside technical fixes.
- Close with commitment round: each role states the next concrete action they will champion post-session.

---

## Roles, traits & progression
- Roles represented: fractional CTO, security lead, product manager, customer success manager, operations analyst.
- Entry pathways include support engineers stepping into incident command, consultants pivoting into vCISO roles and ops generalists leading vendor management.
- Standout traits: facilitation under pressure, systems thinking, empathy for non-technical stakeholders and curiosity about adversary tradecraft.
- Career progression: red-team exercise leads can grow into security program managers, heads of resilience or platform engineering directors.

---

## Key takeaway
A well-structured capstone turns abstract resilience talk into muscle memory.
By stress-testing Sarah's startup collaboratively, teams leave with evidence-backed maturity scores, a sequenced roadmap and renewed respect for cross-functional partnership.
Treat the exercise as a rehearsal for the next funding round diligence meeting—and an invitation to invest in shared accountability before the real incident hits.

---
