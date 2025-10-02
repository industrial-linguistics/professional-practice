---
marp: true
title: Day-Zero Core Services Setup
---

# Day-Zero Core Services Setup
*Launch the company without losing the first week*

---

## What "day zero" covers
- Incorporation paperwork, domains, devices and baseline tooling
- Mapping who owns which setup tasks during the first 5 business days
- Getting identity, communication and knowledge systems online together
- Capturing decisions so MSPs, investors and auditors see a coherent plan

---

## Incorporation & registrations
- Lodge the legal entity, appoint directors and open a business bank account
- Secure tax IDs and payroll registration before the first contractor invoice lands
- Document ownership structure and sign founder agreements to prevent later disputes
- Create a data room folder for incorporation artefacts and board resolutions

---

## Domains, DNS and website plumbing
- Register primary domains plus defensives (.com, .co, relevant country codes)
- Use registrar accounts tied to shared ops email, not a founder's personal inbox
- Set up DNS hosting with templated records for MX, SPF, DKIM and verification tokens
- Configure uptime monitoring so a silent DNS change does not break email launches

---

## Productivity suite and identity backbone
- Choose Google Workspace or Microsoft 365 based on customer expectations and toolchain fit
- Example: a B2B SaaS startup picked Google Workspace because enterprise buyers expected Google SSO integration
- Compare costs early—Google Workspace Business Standard at $12/user/month vs Microsoft 365 Business Premium at $22/user/month
- Establish a primary identity provider and enforce MFA on admin roles from day one
- Create shared mailboxes (hello@, finance@) and delegated calendar access for founders
- Sync HR roster or interim spreadsheet to drive joiner/mover/leaver workflows

---

## Communication and knowledge hubs
- Stand up chat (Slack/Teams) with channels for founders, delivery, customers and incidents
- Launch a lightweight knowledge base (Notion, Confluence, Google Sites) for policies and SOPs
- Decide where meeting notes, board decks and investor updates live to avoid scattered history
- Pre-create announcement, incident and customer escalation templates for fast reuse

---

## Device procurement and setup
- Order a buffer of laptops with baseline images, asset tags and shipping templates
- Plan inventory—for a two-person team, order three laptops so a backup is ready for demos or travel hiccups
- Budget $1,500–2,000 per laptop including warranty, MDM licensing and shipping
- Pre-stage admin accounts in MDM or Autopilot/Zero Touch before boxes leave the supplier
- Document loaner process plus travel kits (power adapters, privacy filters, LTE dongles)
- Track serial numbers, warranty dates and assigned owners in the asset register

---

## Security guardrails on hour one
- Enable password manager, phishing reporting button and security awareness bite-size modules
- Turn on default logging, backup policies and conditional access before inviting new users
- Generate break-glass accounts with hardware keys stored off-site under dual control
- Recommend starter tooling: 1Password for teams ($8/user/month), Microsoft Defender for Business or Google Workspace security center
- Add founders to incident bridge, legal counsel and cyber insurer contact lists

---

## Budgeting for day-zero services
- Reserve $200–500/month for productivity suite licensing, domain registration and DNS hosting
- Allow 2–3 weeks for hardware procurement, imaging and inevitable shipping delays
- Line up $1,000–3,000 for incorporation legal fees plus trademark searches
- Pre-approve founder credit cards so vendor sign-ups are not stalled at payment screens

---

## Early compliance and data residency
- Confirm whether early contracts mandate specific data locations or certifications
- Document which services store data in which regions (e.g. Slack US, email EU) to avoid surprises
- Draft a lightweight privacy policy before collecting any customer information
- Flag GDPR, CCPA or industry rules that influence vendor shortlists and architecture choices

---

## When day-zero planning goes wrong
Real examples teach better than theoretical checklists.
Let's see how a simple DNS mistake nearly derailed a promising startup.

---

## Sarah's DNS cautionary tale
- Sarah, the CEO, registered the domain under her personal email and "learned DNS" at 1 a.m.
- She deleted the wildcard record while experimenting, taking product demos offline for 6 hours
- Sales woke up to bounced customer emails and a frantic investor asking about the outage
- The fix: shared registrar access, documented records and change windows even for tiny teams

---

## First-week runbook
- Create a simple Kanban board with day-zero tasks, owners and completion evidence links
- Schedule daily 15-minute stand-ups to clear blockers and surface vendor delays
- Record walkthrough videos for critical systems so future hires ramp without live hand-holding
- Note dependencies on lawyers, accountants or MSPs and pre-book escalation contacts

---

## Key takeaway
A disciplined day-zero setup makes incorporation, domains, devices and security feel intentional.
Treat the checklist as a living runbook that survives founder vacations, vendor turnover and the first due-diligence call.
Your assignment: craft a day-zero checklist for a hypothetical startup, noting where outside experts are required.

---
