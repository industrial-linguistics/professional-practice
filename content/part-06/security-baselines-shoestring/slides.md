---
marp: true
title: Security Baselines on a Shoestring
---

# Security Baselines on a Shoestring
*Keep founders secure without burning the runway*

---

## Why baselines still matter when cash is tight
- Opportunistic attackers do not care about your burn rate or headcount
- Core customers and investors expect proof of disciplined hygiene
- Founders sleep better knowing incidents will be containable, not existential
- A written baseline lets contractors and MSPs align to the same guardrails

---

## Essential controls triage
- Multi-factor authentication everywhere with hardware keys for admins
- Team-wide password manager, vaulting shared secrets and automations
- Patch cadence locked to auto-update; log drift and skipped versions
- 3-2-1 backup pattern for production data and critical SaaS exports
- Typical spend: $15–25 per user per month for MFA, password manager and backup tooling combined

---

## Identity and access on a lean budget
- Use Google Workspace or Entra ID as the identity backbone with zero-trust defaults
- Enforce conditional access: block legacy auth, require device health for admin roles
- Automate joiner/mover/leaver via scripts or low-code HRIS connectors
- Maintain least privilege through quarterly access reviews with board visibility

---

## Device security without a full IT team
- Lightweight MDM: Kandji, JumpCloud or Intune Business Premium for <$10/user/month
- Baseline policies: disk encryption, firewall on, biometric unlock, screen-lock timers
- Auto-roll patches via managed update rings; track stragglers in a single dashboard
- Ship loaner kits with pre-registered hardware keys and step-by-step recovery guides

---

## SaaS and network hygiene
- Centralise SaaS discovery with browser plug-ins and finance exports to catch shadow IT
- Force SSO or at least MFA on critical apps; disable email/password logins where possible
- DNS filtering (NextDNS, Cloudflare Teams) as a "virtual firewall" for remote staff
- Document vendor data locations and default retention so customers hear a confident answer

---

## Outsourced detection and monitoring options
- Virtual SOC subscriptions (Arctic Wolf, Huntress, Defendify) from ~$1,000/month for <50 seats
- MSSP bundles that include SIEM-lite dashboards and monthly threat briefings
- Contract clauses: 24/7 alerting, 1-hour critical escalation, playbook alignment workshops
- Treat MSSPs as staff augmentation—keep an internal owner accountable for outcomes

---

## Lightweight telemetry stack
- Centralise logs with open source (Wazuh, Elastic Agent) or affordable SaaS (Tines, Panther community)
- Prioritise identity, endpoint and cloud audit trails; skip noisy firewall logs at first
- Establish retention tiers: 30 days hot, 180 days cold for regulator-friendly storytelling
- Use automation to enrich alerts with asset owner, business criticality and runbooks

---

## Everyday hygiene culture
- Embed "turn it off and on again" humour into ops hours to reinforce prompt patching
- Celebrate zero-click fixes: revoked access, password resets, updates before board meetings
- Publish a monthly hygiene scoreboard with MFA coverage, patch compliance and phishing stats
- Rotate mini-drills so every team experiences a simulated reset, wipe or account recovery

---

## Incident readiness without big spend
- Write two-page runbooks for ransomware, account takeover and lost device scenarios
- Pre-stage crisis comms templates and external counsel contacts
- Leverage free tabletop guides from CISA and insurance partners for quarterly exercises
- Align evidence collection with legal hold obligations before an investigation hits

---

## 30/60/90-day implementation roadmap
- **Day 0–30:** Baseline MFA, password manager rollout, inventory of devices and SaaS apps
- **Day 31–60:** Deploy MDM, DNS filtering, backup automation and outsourced SOC contract
- **Day 61–90:** Fine-tune telemetry, run first tabletop, complete access review with board readout
- Record lessons learned each sprint to iterate controls without adding headcount

---

## Metrics the board will back
- MFA coverage %, device compliance %, mean time to patch critical updates
- Logged incidents resolved internally vs escalated to MSSP in under 4 hours
- Cost per secure seat relative to revenue and industry benchmarks
- Evidence of continuous improvement: updated baseline doc, training completion, audit trails

---
