Two rounds ago, Sarah's tooling decisions were about stretching $200 a month across six seats. Now the company is pushing 200 people, it sells to banks and hospitals whose procurement teams read every appendix of the MSA, and the board expects spend forecast eighteen months out. The tooling budget has grown to roughly **$20,000 a month** — a hundred times the pre-seed figure — and the character of the decisions has changed with it. The question is no longer "can we afford this tool?" but "can we prove, to an auditor or a customer's CISO, that our tools enforce what our contracts promise?"

That's what Series B does to a stack. Regulated enterprise customers expect SOC 2 Type II evidence, 24/7 support coverage and contractual uptime remedies. Investors expect every SKU to carry a forecast line and a justification against an 18-month runway plan. Internally, the tooling now underpins pipeline audits, co-selling and customer onboarding. It has stopped being a patchwork of founder credit-card subscriptions and become the company's nervous system.

## Three layers, glued together by automation

The reference architecture is easiest to hold in your head as three layers — revenue, service and trust — connected by automation rather than by people re-keying data.

- **Revenue.** Salesforce Enterprise with CPQ anchors accounts, entitlements and renewals. When pricing changes, downstream systems inherit it instantly instead of waiting for someone to update a spreadsheet.
- **Service.** ServiceNow ITSM and CSM own operational truth: incidents, changes and customer support cases, with audited hand-offs between them.
- **Trust and data.** A Snowflake lakehouse with dbt models joins the two worlds for finance dashboards and customer health scores; contract lifecycle management (CLM) orchestrates legal, finance and sales; and a SIEM/EDR pairing captures audit-grade logs so that every action in the other layers leaves a trace.

None of these choices is exotic. What's distinctive at Series B is that they are chosen *as a system*: each platform is judged on what it feeds and what it consumes, not on its feature list in isolation.

## Where the $20K goes

The monthly snapshot breaks into eight categories. Salesforce Enterprise for 60 seats plus CPQ and its Slack and MuleSoft connectors takes the lion's share at **$7,200**, because tying ARR, usage and renewals to a single source of truth is what makes every other number in the company trustworthy. ServiceNow ITSM and CSM for 30 agents, including the Virtual Agent, adds **$3,900** — expensive, but it is what keeps regulated customers out of the founders' inboxes and inside audited 24/7 workflows. Security and observability (Panther SIEM, SentinelOne Complete, Cribl for log ingestion) run **$2,400**; the integration fabric (Workato Enterprise with eight recipes, plus Segment) **$1,200**; contract lifecycle (Ironclad plus DocuSign CLM) **$1,600**; data and RevOps (Snowflake, Fivetran, Hightouch, Mode) **$1,150**; and compliance and risk (Drata Enterprise plus Whistic for vendor assessments) **$950**. The final **$1,600** — ten per cent — is a deliberate buffer for add-on SKUs, seat growth and implementation partners.

That buffer deserves a comment, because founders instinctively delete it. At this scale something *will* change mid-quarter — a new geography, a compliance-heavy customer, a surprise seat true-up — and a plan with no slack converts every change into an emergency budget request to the board. The buffer is not waste; it's the price of never having to say "we didn't model that".

## Integration is where the value lives

A $20K stack of unconnected platforms is just an expensive way to have the same argument in five different consoles. The integrations are what make the architecture real:

- Salesforce accounts and ServiceNow customer-service records stay synchronised, so support agents and account executives are describing the same customer.
- When a monitored service breaches an uptime SLA, ServiceNow auto-creates an incident, pages the on-call engineer through PagerDuty, and mirrors the escalation inside Salesforce so the account team isn't blindsided on the renewal call.
- Change approvals in ServiceNow write back to the Salesforce opportunity, keeping renewals co-termed with what's actually running in production.
- ServiceNow audit logs stream into Panther, so the security team sees who touched what without logging into three consoles.
- Okta's SCIM feeds provision and deprovision users in both platforms, keeping least privilege enforceable rather than aspirational.

When you assess a Series B stack — yours or someone else's — start here. Missing integrations show up later as reconciliation spreadsheets, missed escalations and audit findings.

## Contracts stop being email attachments

CLM is the unsung addition at this stage. Once legal reviews start stacking up, a platform like Ironclad or LinkSquares hosts the standard templates, clause playbooks and approval routes, so sales reps stop emailing legal for every redline: the playbook already knows which clauses are pre-approved for which industry and region. ServiceNow's Vendor Risk module attaches due-diligence artefacts, NetSuite consumes the executed contract to trigger revenue recognition, and Snowflake picks up contract events to drive renewal forecasts. With DocuSign CLM in the loop you get an audit-grade history of every version, approver and obligation — which matters enormously the first time a customer disputes what was agreed. A simple dashboard tracks cycle time, clause deviations and upcoming renewals, turning legal from a queue into a measurable process.

## Security posture an auditor can actually read

Security spend is no longer optional judgement — enterprise CISOs and auditors are reading your runbooks. SentinelOne endpoint telemetry ships into Panther with retention aligned to PCI and Essential Eight requirements, so you're not buying log storage à la carte in a panic. Drata pulls control evidence continuously from Okta, AWS, ServiceNow and Jira, which turns SOC 2 renewal from an annual heroic effort into a background process. Whistic's shared questionnaire library deflects roughly 40% of bespoke customer security reviews. Quarterly purple-team exercise results land in Confluence and ServiceNow Knowledge, where the next audit can find them.

> Budget 80 hours of specialist partner time for SIEM tuning and response playbooks. Nobody gets detection rules right alone on the first pass, and an untuned SIEM is a very expensive way to generate alerts nobody reads.

## The worksheet that keeps everyone honest

The cost model for all of this lives in a five-tab worksheet that finance, IT and go-to-market leadership share. **Inventory** lists every system with its contract owner, renewal date and SKUs — nothing auto-renews in the shadows. **Seats and tiers** records current counts and, critically, the trigger that forces an upgrade: headcount, a compliance requirement, a product launch. **Projects** tracks implementation partners and statements of work so spend can be capitalised or amortised properly. **Scenario levers** and **risk offsets** close the loop, connecting investments to the penalties they avoid and the hires they defer.

The levers tab is where the plan lives or dies, so it's built on concrete unit economics: 25 new go-to-market seats adds about $1,800 a month of Salesforce uplift; a new SOC 2-demanding customer adds roughly $600 for SIEM storage and two more ServiceNow agents; expanding into EMEA switches on extra Workato recipes and DocuSign's eIDAS compliance pack; shedding 10% of low-touch customers cuts $400 of ServiceNow digital channels. Savings get documented with the same discipline — retiring a legacy ETL job frees $700 a month, which funds CLM workflow bots instead of silently disappearing. When the board asks "what happens to spend if we grow 40% instead of 20%?", the answer comes from formulas, not vibes.

## Making it yours

The workshop for this topic asks you to do what a platform owner or head of IT does in the first month of a Series B role: map the current stack against the reference architecture and mark the gaps, populate the worksheet with real owners, renewal dates and seat counts, then stress-test spend against best- and worst-case ARR with a 15% contingency. Identify the top three integration risks and the mitigation each buffer dollar funds. Close with a two-slide executive summary — one slide of spend, one of risk posture — because that, in the end, is the deliverable: a stack the board can read as easily as the engineers can run it.
