---
marp: true
title: Scaling Support Processes
---

# Scaling Support Processes
*Evolving from founder-led fixes to a scalable service desk*

---

## When ad-hoc support stops working
- Slack pings overwhelm the one IT generalist and create invisible queues
- Context lives in heads; onboarding a new hire takes days of oral history
- Regulators and auditors ask for incident logs you can't produce
- Customer-facing teams feel the pain first—every outage escalates straight to engineering

---

## Design the first help desk intentionally
- Launch a single intake (portal + email) with auto-triage by request type
- Publish lightweight SLAs: critical 2h, high 4h, normal 1 business day
- Create macros for the top 20 requests; everything else routes to a backlog
- Implement daily standups and a weekly ops review to surface blockers

---

## Knowledge base as force multiplier
- Pair every resolved ticket with an article draft before closure
- Use "seed, grow, prune" cycles: SMEs review monthly, archive stale pages quarterly
- Embed short Loom walkthroughs—startups learn visually faster than reading PDFs
- Track self-service deflection rate and article helpfulness to justify more authors

---

## Tooling choices: ServiceNow vs Jira Service Management
- **ServiceNow**: enterprise-grade workflows, deep CMDB, strong audit trails; higher cost and implementation lift
- **Jira Service Management**: native with Atlassian stack, faster to deploy, rich automation rules; needs add-ons for mature CMDB
- Decision guardrails: regulatory obligations, dev tool alignment, in-house admin skills, and 3-year TCO
- Bridge gaps with integrations (e.g., Slack virtual agent, asset DB sync) before committing to a rip-and-replace

---

## Layer automation and integrations early
- Connect Slack or Teams to create tickets with structured forms and context capture
- Enforce change approvals and incident postmortems via workflow gates
- Sync asset inventory (Intune, Kandji, Jamf) to the ITSM CMDB nightly
- Automate onboarding/offboarding tasks with workflow engine + IDP events

---

## Staffing for maturity
- Stage 1 (≤50 staff): one ops lead covering L1 + process design; rotate engineers for escalation duty
- Stage 2 (50–150): dedicated L1 agents, part-time knowledge manager, on-call matrix with product squads
- Stage 3 (150+): L2 specialists for infra/security/apps, service owner, tooling admin, CSAT analyst
- Invest in career ladders and certification paths to retain institutional knowledge

---

## Process milestones to hit
- Month 1: catalog services, define categories, publish runbooks for top incidents
- Month 2: launch knowledge base, implement change calendar, start ticket QA program
- Month 3: introduce problem management reviews, automate joiner/mover/leaver flows
- Month 4+: quarterly service reviews with finance/product, refresh tooling roadmap

---

## Metrics that prove maturity
- Ticket intake mix: aim for ≥30% self-service deflection within six months
- Responsiveness: 90th percentile response under SLA, backlog <1.5× weekly throughput
- Quality: CSAT ≥4.5/5 and knowledge article helpfulness ≥80%
- Business impact: downtime minutes prevented, engineering time saved, audit findings closed

---

## Action checklist
- [ ] Pick pilot team, map top 10 request types and pain points
- [ ] Stand up intake, SLAs and runbook templates before announcing new process
- [ ] Select tooling with a weighted scorecard and run a two-week sandbox bake-off
- [ ] Review metrics weekly; adapt staffing and knowledge strategy every quarter
