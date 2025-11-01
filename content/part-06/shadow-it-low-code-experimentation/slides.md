---
marp: true
title: Shadow IT and Low-Code Experimentation
---

# Shadow IT and Low-Code Experimentation
*Empower creativity without losing control*

---

## Why shadow IT happens
- Teams need quick wins while official backlogs stretch for quarters.
- Low-code tools advertise drag-and-drop miracles and free tiers that bypass procurement.
- Vendors bundle "starter" admin roles that feel harmless until production data lands inside.
- People default to whatever solves their immediate customer pain, governance slide deck or not.

---

## Upside of sanctioned tinkering
- Rapid prototypes surface requirements before engineering commits sprints.
- Business teams build dashboards, forms and automations that unblock frontline work.
- Low-code playbooks cultivate citizen developers who speak both process and platform.
- Early experiments become evidence for future budget and hiring conversations.

---

## Risk: access sprawl and data leakage
- Over-permissioned connectors replicate sensitive data into personal accounts.
- Shadow integrations create blind spots for incident response and continuity plans.
- Untracked API keys or webhook secrets violate customer contracts and regional laws.
- Support teams inherit break/fix duties for stacks they have never seen before.

---

## Cautionary tale: the Slack admin summer
- An enthusiastic intern spun up a workflow app and, "to save time," granted Workspace Admin to every channel lead.
- A week later a contractor accidentally deleted finance archives while exploring new buttons.
- Recovery required Slack support, legal notifications and a surprise weekend sprint to rebuild audit logs.
- The lesson: enthusiasm without guardrails equals overtime and apology tours.

---

## Access guardrails that scale
- Default to least-privilege roles mapped to personas (builder, reviewer, auditor).
- Automate provisioning via SSO groups so revoking access is one click, not 19 emails.
- Enforce data classification tags that block exports of regulated information.
- Log every elevated permission grant and require manager sign-off within 24 hours.

---

## Safe sandboxes for experimentation
- Offer dedicated dev tenants with scrubbed datasets and disposable connectors.
- Provide golden templates that bake in audit logging, alerts and naming conventions.
- Use API gateways or service accounts with scoped tokens instead of personal credentials.
- Schedule quarterly "citizen dev" hack nights with platform engineers coaching in real time.

---

## Lightweight governance rituals
- Publish an intake form capturing purpose, data types, integrations and owners.
- Run fortnightly review huddles to bless launches, flag risks and share learnings.
- Maintain a living catalogue of approved tools with support tiers and renewal dates.
- Tie shadow IT discoveries into risk registers so executives see trends, not surprises.

---

## Observability and assurance
- Instrument low-code platforms with central logging and anomaly alerts.
- Track metrics: number of sanctioned apps, orphaned flows, escalations per quarter.
- Conduct tabletop exercises simulating connector breaches and revoked tokens.
- Feed findings into onboarding so new hires learn "how we experiment here" on day one.

---

## Roles, traits and career pathways
- Platform engineers and automation leads curate guardrails while enabling new builders.
- Business technologists or ops analysts translate problems into safe low-code patterns.
- Governance analysts grow into risk leads by shaping policy with pragmatic empathy.
- Curious tinkerers progress from citizen devs to official solution architects who mentor others.

---
