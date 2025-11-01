---
marp: true
title: Budgeting and FinOps for Start-ups
---

# Budgeting and FinOps for Start-ups
*Stretch every credit while protecting runway*

---

## Session objectives
- Understand FinOps principles tailored to sub-50 person teams.
- Translate infrastructure and tooling spend into runway scenarios.
- Build a cadence for monitoring usage and renegotiating credits.

---

## FinOps mindset in the first 24 months
- Cash is the constraint; design guardrails before scaling automation.
- Align product, finance and engineering on a single cost taxonomy.
- Document who owns pricing decisions for each platform or vendor.
- Treat forecasts as living artefacts reviewed with investor updates.

---

## Mapping cash runway with tooling
- Start with burn formula: `(opening cash - committed spend) ÷ monthly burn`.
- Categorise costs into keep-the-lights-on vs. experiment budgets.
- Highlight contractual cliffs: annual renewals, seat minimums, auto-renewals.
- Use a shared dashboard to show spend per customer or feature flag.

---

## Making cloud credits last
- Catalogue every provider credit, expiry date and eligible workloads.
- Deploy credits to low-risk environments first (sandbox, QA).
- Set budget alerts at 60/80/100% of expected usage to course-correct.
- Pair credits with optimisation tactics: rightsizing, scheduling shutdowns, spot usage.

---

## Tooling usage monitoring toolkit
- Centralise billing exports in a warehouse or spreadsheet.
- Instrument services with tags/labels for team, feature and environment.
- Automate weekly cost digests to Slack/email for accountable owners.
- Trigger lightweight reviews when variances exceed 15% week-on-week.

---

## Monthly stack spend drill
| Tool / Service | Seat or usage assumption | Monthly cost (AUD) |
| --- | --- | --- |
| Google Workspace Business Standard | 12 seats @ $11 | $132 |
| AWS compute & storage | Forecast 450 credits, 70% burn | $0 (credit drawdown) |
| Datadog monitoring | 3 engineer seats @ $27 | $81 |
| Customer support platform | 6 agents @ $20 | $120 |
| Contingency / experiment buffer | 10% of baseline | $33 |
| **Total cash outlay** |  | **$366 (credits cover $150 value)** |

---

## Workshop instructions
1. Duplicate the drill with your own stack and contract terms.
2. Adjust assumptions until your cash outlay stays within guardrails.
3. Identify one optimisation lever per tool (renegotiate, downgrade, automate).

---

## Guardrails & red flags
- Vendor pushes multi-year deal before product-market fit—counter with quarterly.
- Usage spikes without revenue signal? Pause automation rollouts immediately.
- Silent auto-renewals: set calendar holds 60 days prior to renewal dates.
- Founders ignoring chargeback data erodes trust with finance and investors.

---

## Linking to investor conversations
- Share FinOps scorecard in monthly updates: spend vs. forecast, credits remaining.
- Demonstrate how optimisations extended runway (e.g., +2 months from rightsizing).
- Use variance explanations to reinforce control over GTM and product strategy.
- Invite observers to quarterly FinOps reviews to build confidence pre-Series A.

---

## Action plan for Sarah
- Stand up a weekly cost review ritual with engineering and finance partners.
- Build a central ledger for credits, renewals and owner accountability.
- Pilot the monthly spend drill with leadership, then cascade to team leads.
- Revisit guardrails each funding milestone to stay aligned with growth.

---
