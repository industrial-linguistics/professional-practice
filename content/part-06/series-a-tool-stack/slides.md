---
marp: true
title: Series A Tool Stack Example
---

# Series A Tool Stack Example
*Scaling discipline without enterprise bloat*

---

## Series A reality check
- 40–60 person team, first enterprise deals on the horizon.
- Board asks for proof of internal controls before approving new spend.
- Customers now require SOC 2 reports, SSO and incident response evidence.
- Guardrail: keep the SaaS core near **$2K/month** while funding product growth.

---

## Budget snapshot (~$2.1K/month)
| Category | Tools & assumptions | Monthly cost | Investor proof point |
| --- | --- | --- | --- |
| Identity & access | Okta Workforce Identity for 45 seats @ $12 | **$540** | SSO + central audit logs |
| Collaboration & meetings | Slack Business+ (30 seats) + Zoom Business (18 hosts) | **$735** | Secure global coordination |
| Product delivery & on-call | Atlassian Cloud (Jira, Confluence, Opsgenie) for 40 seats | **$320** | Traceable change history |
| Trust & compliance | Vanta Growth plan (discounted with startup credits) | **$250** | Automated SOC 2 evidence |
| Data & RevOps | Snowflake starter + Fivetran Lite + dbt Cloud Team | **$250** | Revenue metrics on tap |
| **Total** | | **$2,095** | Within Series A burn model |

---

## Identity & access: Okta as the spine
- Deploy Okta Workforce Identity or Auth0 Workforce for workforce SSO.
- Enforce SAML for Slack, Zoom, Atlassian and HRIS in one dashboard.
- Automate joiner/mover/leaver with HR triggers (Rippling, Deel, HiBob).
- Capture MFA posture reports for diligence rooms.
- Budget buffer: +$120/month for adaptive policies or Advanced Server Access if engineers need SSH brokering.

---

## Communication & meeting layer
- **Slack Business+** unlocks SSO, retention policies and eDiscovery exports.
- **Zoom Business** covers 18 global hosts plus 2 executive webinar add-ons.
- Provision guest accounts for agencies via Okta to keep audit trails clean.
- Record renewal dates and owners in a finance ledger so nothing auto-renews unnoticed.
- Shared etiquette: move post-mortems and decision logs into Confluence within 24 hours to keep Slack from becoming your memory.

---

## Product delivery & incident response
- **Jira Software** for backlog + sprint rituals; restrict admin rights to engineering leadership.
- **Confluence** houses runbooks, architecture ADRs and policy packs linked from Jira epics.
- **Opsgenie** standard plan wires alerts to on-call, with post-incident templates exported for compliance.
- Integrate Jira tickets with GitHub or GitLab so release notes and change approvals are auditable.
- Expect cost to rise ~15% once you cross 50 technical seats—document the trigger in your forecast.

---

## Trust, risk & compliance automation
- **Vanta Growth** (or Drata equivalent) pulls evidence from Okta, Jira, AWS and GitHub automatically.
- Map controls to SOC 2, ISO 27001 and Essential Eight requirements for Australian clients.
- Use policy packs to train teams quarterly; store attestations in Confluence.
- Pair with **Tugboat Logic questionnaires** or **Thoropass** if customer security reviews ramp up.
- Justify the spend: single security hire would cost >$12K/month—this tool simulates the headcount.

---

## Data, finance & RevOps instrumentation
- **Fivetran Lite** syncs SaaS sources (Stripe, HubSpot) into Snowflake nightly.
- **Snowflake** on-demand compute stays <$50/month if you suspend warehouses off-hours.
- **dbt Cloud Team** lets analytics and RevOps co-own models with approvals tied to Jira.
- Layer **Census** or **Hightouch** later for reverse ETL once CS teams need 360° health scores.
- Cost hygiene: monitor daily credit burn in Snowflake and set a $80/month alert with automatic warehouse suspension.

---

## Serverless vs container run costs (monthly)
| Item | Serverless baseline | Container baseline |
| --- | --- | --- |
| Compute | AWS Lambda & API Gateway (~60M requests) = $220 | EKS w/ 3 × m5.large nodes = $340 |
| Data | DynamoDB on-demand & S3 = $90 | RDS Postgres + EFS backups = $160 |
| Operations | Observability (CloudWatch + Lumigo) = $70 | Observability (Datadog APM + Logs) = $180 |
| Staffing | 0.5 platform engineer (shared) | 1 FTE platform/SRE for cluster upkeep |
| **Total** | **$380 + shared headcount** | **$680 + dedicated headcount** |
- Serverless stays cheaper until workloads exceed 100M requests/month or need long-running compute.
- Containers make sense when you require custom networking, GPU jobs or predictable workloads.

---

## Decision triggers for architecture shifts
- Switch to containers when cold starts hurt SLAs or per-request cost exceeds $0.60 per 1K invocations.
- Budget for Terraform/Terragrunt and cluster hardening audits before migrating.
- Pilot with managed Fargate/ECS to avoid Kubernetes overhead unless you already have deep ops talent.
- Document the total cost of ownership—tools, observability, people—in the board pack.

---

## Framing spend for skeptical investors
- Tie each tool to a risk removed: SSO stops account sprawl, Vanta prevents $200K SOC 2 consulting.
- Show savings vs headcount: one security hire + in-house ETL exceeds $25K/month fully loaded.
- Present a time-to-value chart: Okta deployed in 3 weeks, Vanta audit ready in 90 days, Atlassian reporting in 1 sprint.
- Highlight scalability: all contracts scale to 100 seats without renegotiation.
- Build an exit plan slide noting downgrade paths if growth slows.

---

## Workshop prompt for learners
- Map your current stack against the five categories and highlight gaps.
- Draft a $2K/month budget, including assumptions and credits you are counting on.
- Identify the metric or risk that justifies each line item for the board memo.
- Debate whether your workloads justify serverless, containers or a hybrid, citing cost data.
- Capture the action plan in Confluence with owners and review dates.

---
