---
marp: true
title: Day-Zero Startup IT Assessment
---

# Day-Zero Startup IT Assessment
*Make the first 48 hours intentional*

---

## Why a day-zero checklist?
- Founders are wiring payroll, domains and devices while investors expect security by default.
- Early missteps compound: a shared admin login today becomes a breach notification tomorrow.
- A structured checklist turns tribal knowledge into a repeatable onboarding ritual for every new hire and contractor.
- It also creates a baseline for MSP handovers, cyber insurance applications and due diligence conversations.

---

## Facilitating the workshop
- Schedule a 90-minute working session with the founding team, operations lead and any fractional IT partner.
- Start with a current-state mural or whiteboard of systems before diving into controls—people grasp context first.
- Assign a scribe who updates the checklist live so decisions turn into action items instead of hallway promises.
- Close each section by capturing blockers, owners and due dates to feed your task tracker that same afternoon.

---

## Checklist structure at a glance
- **Identity** – who has access, how accounts are created, and where MFA is enforced.
- **Endpoints** – device inventory, hardening steps and remote wipe readiness.
- **Backups & Continuity** – what data is protected, tested restores and manual fallbacks.
- **Security & Governance** – logging, password policies, vendor reviews and incident contacts.
- Each block should score readiness (green/amber/red) to signal where to focus limited time and budget.

---

## Identity foundations
- Map every system to an identity source: HR roster, Google Workspace, Microsoft 365, or a password manager.
- Require MFA on admin, finance and customer data tools before inviting the next hire.
- Document joiner/mover/leaver steps, including who revokes access when someone exits suddenly.
- Capture shared secrets in a vault with rotation dates rather than in spreadsheets or chat threads.
- Flag gaps like personal email accounts on vendor contracts so legal can renegotiate early.

---

## Endpoint readiness
- Build an asset list with owner, device type, OS version, and last patch date—spreadsheets beat wishful thinking.
- Standardise baseline builds: disk encryption, auto-lock timers, and approved software images.
- Enable remote wipe or MDM for laptops and mobile phones before a travel-heavy sales push.
- Confirm antivirus/EDR coverage and define how alerts route to whoever is on-call.
- Note loaner device processes so day-one hires are not waiting on procurement.

---

## Backups and data protection
- Identify critical data stores: source code, CRM, finance, shared drives and product telemetry.
- Verify at least one automated backup exists with retention that meets contractual promises.
- Test a sample restore quarterly and document who validated it, how long it took and what broke.
- Outline manual fallback workflows—exporting CSVs, printing key documents, or switching to a secondary tool.
- Track compliance drivers (tax, privacy, contracts) that dictate how long data must stay recoverable.

---

## Security controls and monitoring
- Review password policies, SSO coverage and whether default admin accounts have been renamed or disabled.
- Confirm logging is enabled for auth events, financial transactions and production infrastructure.
- Establish an incident contact tree with who calls legal, PR, investors and affected customers.
- Set expectations for vulnerability scanning cadence and patch response windows.
- Capture third-party vendor attestations (SOC 2, ISO 27001) and note renewals on the calendar.

---

## Workshop outputs
- A scored checklist PDF or Notion page with red/amber/green status and named owners.
- A 30/60/90-day roadmap of remediation tasks aligned to risk and business milestones.
- Updated runbooks: account lifecycle, device setup, backup testing and escalation paths.
- A shared folder with evidence—screenshots, policy links, vendor contracts—for future audits or funding rounds.
- A follow-up session booked to review progress before the next hire or investor meeting.

---

## Roles, traits and progression
- Day-zero assessments are often led by fractional CTOs, security-minded operations managers or MSP onboarding leads.
- Junior security analysts and IT generalists can shadow to learn stakeholder facilitation and control baselining.
- Success hinges on curiosity, diplomacy and the ability to translate checkboxes into founder-friendly language.
- As the company scales, these practitioners grow into heads of IT, risk leaders or customer trust advocates with board visibility.
- Encourage cross-functional allies—finance, HR, product—to own portions of the checklist so accountability is shared.

---

## Key takeaway
A living day-zero checklist is your startup's safety net. It keeps identity, devices, backups and security posture honest from the outset, making future audits and incidents far less dramatic.
Treat the artefact as a shared playbook: iterate after every hire, vendor change or funding round so resilience matures alongside revenue.
---
