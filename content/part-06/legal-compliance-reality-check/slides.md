---
marp: true
title: Legal and Compliance Reality Check
---

# Legal and Compliance Reality Check
*Keeping founders honest about the rules even when the roadmap is sprinting*

---

## Why this matters before Series A
- Contracts, audits and enterprise pilots die quickly if you cannot evidence basic compliance hygiene.
- Regulators and investors expect intent documented early, even if your stack is still duct tape and shared logins.
- Getting ahead of obligations keeps trust intact with customers sharing sensitive data and engineers shipping fast.

---

## Milestones on a lean compliance roadmap
| Milestone | What "good" looks like | Typical timeline |
| --- | --- | --- |
| **Founding (0-3 months)** | Policies drafted, access reviews tracked in a spreadsheet, vendor DPIAs noted. | 2-4 working days of concentrated effort |
| **SOC 2 Type I** | Controls designed and evidenced for a point-in-time audit; readiness assessment signed off. | 3-4 months with external coach |
| **SOC 2 Type II** | Control operation proven over 3-6 months, automation in place for logs and reviews. | 9-12 months from kickoff |
| **ISO 27001 cert** | Risk register, Statement of Applicability, internal audits and management review documented. | 12-15 months with staged scope |

---

## Making audits survivable for small teams
- Start with a single owner (often COO, security lead or fractional CISO) plus one project manager or chief of staff.
- Use lightweight tooling: ticket queue for control tasks, password manager exports, MDM screenshots and change logs.
- Rehearse evidence pulls monthly so nothing lives only in someone's inbox or head.
- Automate what you can early—cloud security posture tools, HRIS-to-IdP sync, log retention policies—before the audit gap list grows.

---

## Open source licence obligations in production
- Maintain a software bill of materials (SBOM) and record licence types for each dependency.
- For copyleft (GPL) components, document how you provide source and any network interaction obligations.
- Apache and MIT libraries still require attribution—ship a NOTICE file in your repo and product help centre.
- Track obligations during vendor assessments: security questionnaires often probe licence posture.
- Assign an owner to approve new libraries and keep dependency updates tied to security patch cycles.

---

## Privacy by design when you're shipping fast
- Map personal data flows for each new feature, noting storage, processors and retention choices.
- Run quick DPIA templates before launch—15 minutes to log risks, mitigations and approvals beats retrofitting controls later.
- Default to data minimisation: drop optional fields, anonymise analytics and isolate test data from production.
- Build consent and deletion journeys as reusable components so every squad does not reinvent them under pressure.
- Keep legal counsel or an external advisor in the loop for cross-border data moves and sector-specific rules.

---

## Roles, traits and progression
- **Key roles:** fractional CISOs, security program managers, privacy counsels and compliance-minded ops leads.
- **Entry pathways:** support engineers who wrangle audits, paralegals moving into tech, security analysts stepping into governance.
- **Traits:** meticulous note-taking, calm stakeholder management, ability to translate legal clauses for engineers.
- **Progression:** from compliance coordinator to trust & safety lead, then head of security governance or VP of risk as the company scales.

---

## Quick-start checklist for founders
1. Appoint a single compliance captain with a documented backup.
2. Centralise policies, risk registers, DPIAs and SBOMs in a shared drive or GRC tool with version control.
3. Schedule quarterly control walkthroughs with engineering, product and legal stakeholders.
4. Budget for at least one external audit readiness review per year.
5. Celebrate small wins—closing a policy gap or automating an access review—so the culture sees compliance as momentum, not drag.

---
