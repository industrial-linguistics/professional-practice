---
marp: true
title: Business Continuity for Small Teams
---

# Business Continuity for Small Teams
*Keeping work alive when you're running lean*

---

## Why continuity matters
- A single outage can erase customer trust overnight
- Smaller teams rarely have 24/7 coverage or redundant staff
- Continuity plans protect revenue, compliance obligations and morale
- Treat it as operational insurance, not a "big company" luxury

---

## Sarah's MongoDB crash night
- 1:07am: production MongoDB cluster filled the disk and locked reads
- No on-call rotation meant Slack pings went unanswered for 40 minutes
- Backups existed, but restore runbooks were outdated and slow
- Customers tweeted screenshots of 500 errors by sunrise
- Lesson: improv chaos costs more than writing a plan on a good day

---

## Core continuity building blocks
- **Impact analysis** – which services fail first and who feels it?
- **Recovery objectives** – set realistic RTO/RPO for each system
- **Runbooks** – step-by-step for outages, restores and communications
- **Testing cadence** – tabletop every quarter, restore drills twice a year

---

## Backup and data recovery essentials
- Automate daily snapshots plus point-in-time recovery for databases
- Store backups off-site and test restores in a staging environment
- Track retention and legal hold requirements in your inventory
- Tag owners so a single engineer vacation does not stall a restore

---

## Incident communication templates
- Draft status page, customer email and investor update templates now
- Define who triggers updates, approves language and closes the loop
- Provide plain-language summaries plus technical timelines
- Keep a DM list for stakeholders who need SMS/phone escalation

---

## Vendor and tooling redundancy
- Document critical SaaS dependencies and their failover options
- Pre-negotiate emergency credits or burst capacity with cloud vendors
- Keep offline copies of contracts, API keys and contact trees
- Identify manual workarounds if integrations or single sign-on fail

---

## Lightweight continuity checklist
1. Inventory critical services, data stores and owners
2. Capture RTO/RPO targets and validated backup evidence
3. Update contact trees and communication templates quarterly
4. Schedule restore tests and tabletop drills on the team calendar
5. Log lessons learned and refresh the plan after every incident

---

## Roles, traits and progression
- Roles: fractional CTOs, ops generalists and compliance leads (1 per 20–30 staff)
- Entry: support engineers, founders doubling as IT, MSP partners on retainer
- Traits: calm under pressure, documentation-first, empathetic communicators
- Growth: ops generalist → continuity lead → head of resilience / risk

---

## Key takeaway
Preparedness beats heroics—documented backups, contacts and scripts keep customers confident when things break at 2am.

---
