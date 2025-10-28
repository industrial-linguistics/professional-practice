---
marp: true
title: Series B Enterprise Stack
---

# Series B Enterprise Stack
*Integrations, controls and cost modelling at ~$20K/month*

---

## Why Series B changes the stack
- 180–250 person company supporting regulated enterprise customers.
- Customers expect SOC 2 Type II evidence, 24/7 support and ironclad SLAs.
- Board pressure to forecast spend with 18-month runway discipline.
- Tooling now underpins pipeline audits, co-selling and customer onboarding.

---

## Reference architecture
- **Salesforce Enterprise + CPQ** anchors revenue, entitlements and renewals.
- **ServiceNow ITSM/CSM** runs incidents, change and customer support flows.
- **Central data lakehouse** (Snowflake + dbt) feeds health scores and finance.
- **Contract lifecycle management (CLM)** orchestrates legal, finance and sales.
- **SIEM + EDR** stack captures audit-grade logs for security and compliance.

---

## Monthly spend snapshot (~$20K)
| Category | Tools & assumptions | Monthly cost | Rationale |
| --- | --- | --- | --- |
| Revenue platform | Salesforce Enterprise (60 seats) + CPQ, Slack + MuleSoft connectors | **$7,200** | Ties ARR, usage and renewals to one source of truth |
| Service operations | ServiceNow ITSM & CSM (30 agents) incl. Virtual Agent | **$3,900** | Meets 24/7 support SLAs with audited workflows |
| Security & observability | Panther SIEM + SentinelOne Complete + Cribl ingestion | **$2,400** | Consolidated threat detection and compliance-ready logs |
| Integration fabric | Workato Enterprise (8 recipes) + Segment Connections | **$1,200** | Bridges go-to-market, product and finance data |
| Contract lifecycle | Ironclad CLM (legal + sales users) + DocuSign CLM | **$1,600** | Speeds redlines, tracks obligations and renewal clauses |
| Data & RevOps | Snowflake, Fivetran Growth, Hightouch Pro, Mode | **$1,150** | Gives RevOps near-real-time performance dashboards |
| Compliance & risk | Drata Enterprise + Whistic vendor assessments | **$950** | Automates evidence, centralises security questionnaires |
| Buffer & pilots | 10% reserve for add-on SKUs and implementation partners | **$1,600** | Absorbs seat growth and specialist services |
| **Total** |  | **$20,000** | Within Series B operating plan |

---

## Integration map: Salesforce ↔ ServiceNow ↔ SIEM
- Sync accounts and cases: Salesforce Account ↔ ServiceNow Customer Service.
- Auto-create incidents when uptime SLAs breached via ServiceNow + PagerDuty.
- Feed ServiceNow change approvals to Salesforce opportunities for co-terming.
- Stream ServiceNow audit logs into Panther for unified detection.
- Capture user provisioning via SCIM from Okta into both systems for least privilege.

---

## Contract lifecycle management expansion
- Ironclad or LinkSquares hosts standard templates, playbooks and approval routes.
- Integrate with Salesforce for clause libraries driven by industry/region metadata.
- Connect to ServiceNow Vendor Risk for due diligence artefacts.
- Route signed contracts to NetSuite and Snowflake for revenue recognition triggers.
- Dashboard monitors cycle time, clause deviations and renewal auto-notifications.

---

## Security guardrails and compliance posture
- SentinelOne telemetry shipped to Panther SIEM with retention aligned to PCI/Essential Eight.
- Drata pulls evidence from Okta, AWS, ServiceNow and Jira for continuous monitoring.
- Whistic questionnaire library reduces bespoke customer security reviews by 40%.
- Quarterly purple-team exercise results stored in Confluence + ServiceNow Knowledge.
- Budget 80 hours of partner time for SIEM tuning and playbook development.

---

## Cost modelling worksheet structure
- **Tab 1: Inventory** – list systems, contract owners, renewal dates and SKUs.
- **Tab 2: Seats & tiers** – capture current counts, expansion triggers and unit costs.
- **Tab 3: Projects** – implementation partners, statements of work, depreciation.
- **Tab 4: Scenario levers** – ARR growth, headcount plans, support coverage tiers.
- **Tab 5: Risk offsets** – penalties avoided, staff savings, required compliance controls.

---

## Example worksheet levers
- Headcount growth: +25 GTM seats = +$1,800/month Salesforce uplift.
- New SOC 2 customer: adds $600/month for additional SIEM storage + 2 ServiceNow agents.
- EMEA expansion: Workato adds 2 recipes; DocuSign adds eIDAS compliance pack.
- Churn risk: removing 10% low-touch customers cuts ServiceNow digital channels by $400/month.
- Automation win: retiring legacy ETL saves $700/month, funding CLM workflow bots.

---

## Workshop prompt
- Map your current stack against the reference architecture and highlight gaps.
- Populate the worksheet tabs with your own seat counts and integration owners.
- Stress-test spend with best/worst-case ARR scenarios and 15% contingency.
- Identify the top three integration risks and document mitigation actions.
- Present back a two-slide executive summary for board or investor readouts.

---
