# IT Professional Practice

All the things you need to know to get started in your IT career. This
started as a plan for a university-level subject (which didn't go
ahead for other reasons).

You can browse through everything here for free to see if you like
it. If you are wanting to embed this into your corporate training (for
example, as part of a graduate entry program), I would encourage you
to talk to Greg (gregb@industrial-linguistics.com) about paying to get
a custom build done for your organisation -- this helps pay for the
development work for everyone.

# Learning objectives

| LO# | Outcome (Bloom level unchanged) |
| --- | --- |
| 1 | Map and explain the operational, governance, sales and community roles that keep IT services humming. |
| 2 | Design and run a lightweight continuous-delivery pipeline + blameless post-incident review. |
| 3 | Compare and critique innovation & commercialisation pathways—corporate, open-source, start-up, social-impact. |
| 4 | Evaluate and justify service-management and delivery frameworks (ITIL 4, DevOps/SRE, SaaS, OSS, CRM). |
| 5 | Create an IT proposal that embeds ethics, sustainability and Indigenous data-sovereignty principles end-to-end. |

---
| Part | Topic & Focus | Hands-on / Evidence piece | LOs |
| --- | --- | --- | --- |
| 1 | ITIL 4 Foundations: service value chain, incident vs request, L1/L2/L3 roles, major-incident drill. ServiceNow sandbox introduced purely as a visualiser of ITIL concepts (raise, escalate, close). | Log a P1 incident in the sandbox and annotate each role's action. | 1,4 |
| 2 | ITIL 4 Deep Dive: change, problem, CMDB, SLA/SLO & reporting. Introduce ServiceNow change module + simple CMDB demo. | Draft a change-request & walk it through CAB simulation; match each field to ITIL artefacts. | 1,4 |
| 3 | High-Velocity Delivery: DORA metrics, trunk-based DevOps, SRE error budgets. GitHub Actions 3-step pipeline. | Build "hello-world" pipeline → inject failure → collect lead-time/MTTR baseline. | 2,4 |
| 4 | Blameless RCA & Continuous Improvement: post-mortem culture, five-whys, Kaizen vs corrective actions, linking RCA tickets back into ServiceNow & GitHub. | Run an RCA on the week-3 failure; publish an action item & re-run pipeline to show improvement. | 2,4 |
| 5 | Vendor/MSP & CRM Lifecycle: SDR → AE → CSM roles, Challenger Sales, renewals & churn, SLA hand-off to ITSM. Salesforce Trailhead "CRM fundamentals" badge. | Map a six-month pursuit in Salesforce (dummy org) and show touch-points with ITIL change & incident. | 1,3,4 |
| 6 | Start-ups & Small-Biz IT: shoestring stacks, GenAI helpers, zero-ops hosting, security trade-offs. | Mini-consult: audit a local café's tech stack; recommend one practical change & justify with DORA/ITIL lens. | 3,4 |
| 7 | Open-Source & Indigenous Digital Sovereignty: licensing, governance models, Maori case study, "community tech-lead wearing many hats." | Fork & re-license a tiny OSS repo; draft a data-sharing MoU for a First-Nations NGO. | 3,5 |
| 8 | Project Studio and Presentations: teams finalise capstone; viva with panel of SRE, ServiceNow architect, Salesforce AE, and Indigenous digital-inclusion advocate. | Capstone delivery & defence. | 1-5 |

---

# Assessment


| Task | Weight | Due | Notes |
| --- | --- | --- | --- |
| A1: Role-Mapping Reflection (individual) | 20% | Wk 4 | Analyse a simulated major incident; identify every role you interacted with, what mattered and why. (ULO 1, 5) |
| A2: Tiny Pipeline + RCA (pairs) | 30% | Wk 8 | Build the 3-step GitHub Actions pipeline, trigger a forced failure, run a blameless post-mortem, improve the metric. (ULO 2, 4) |
| A3: Capstone Proposal & Pitch (teams 4-5) | 50% | Report Wk 12, viva Wk 13 | Design an IT service for a real community org (indigenous or social-impact). Must justify framework choices, innovation pathway, long-term ethics & sustainability. Includes 10-min board-style pitch + questioning. (ULO 1-5) |


| Task | Notes |
| --- | --- |
| A1 Role-Mapping Reflection (20%) | Now draws on ITIL weeks 1-2 and CRM week 5. |
| A2 Tiny Pipeline + RCA (30%) | Unchanged (weeks 3-4 feed it). |
| A3 Capstone Proposal & Pitch (50%) | Keep structure; students may optionally integrate Salesforce or ServiceNow elements to strengthen justification under ULO 4-5. |
---

Key Resources

- ITIL 4 Foundation
- Forsgren, Humble & Kim – Accelerate (e-book)
- Salesforce Trailhead modules (CRM) – free
- GitHub Education Pack – CI/CD minutes
- ServiceNow "Student Path" sandbox
- Moodle book of short OSS & Indigenous data-rights readings curated with community partners

# Slide Rendering Pipeline

The repository includes scripts that convert slide decks and narratives into finished video lessons.
Each slide's text is sent to ElevenLabs for narration and cached in S3. Slides are exported to PNG
using Marp, then stitched into a silent video. The cached audio segments are concatenated and merged
with the video to create the final lesson, which can be uploaded along with quiz material and packaged
into SCORM or e-book formats. The step-by-step checklist is maintained in [TODO.md](TODO.md).

# Raw material

- `cmd/voicer/main.go` was pulled in from another project, and shows how to call the ElevenLabs API 

- `raw-notes.txt` some text that I wrote that is relevant to a few topics


## Repository Structure

This repository contains Go source code, course content and automation scripts. A full description of the layout is available in [docs/directory-structure.md](docs/directory-structure.md).

For a list of outstanding tasks and ideas, see [TODO.md](TODO.md).

## Development Environment

Run `./envsetup.sh` to install Node.js, npm, ffmpeg, Go, `jq` and the Marp CLI.
