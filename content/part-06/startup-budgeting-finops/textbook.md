FinOps has a corporate reputation — cost-allocation committees, chargeback models, tagging councils — that makes founders' eyes glaze over. Forget that version. For a company of fewer than fifty people, FinOps is one sentence: know what every tool costs, who decided to buy it, and how many months of payroll it's competing with. Cash is the constraint at this stage, so the guardrails have to exist *before* the team automates every workflow and signs annual commitments, not after.

Three habits make up the mindset. First, a single cost taxonomy shared by product, finance and engineering, so a new tool lands in an agreed bucket instead of triggering a budget turf war. Second, a named owner for pricing decisions on each platform or vendor — "who can say yes to the upgrade?" should never be an open question. Third, forecasts treated as living artefacts, reviewed alongside investor updates rather than rebuilt in a panic before each board meeting. Boring, deliberate, and worth real money.

## Runway maths and cost buckets

Everything anchors on a burn formula simple enough for everyone to recite: `(opening cash - committed spend) ÷ monthly burn` = months of runway. The subtlety is in "committed" — annual renewals, seat minimums and auto-renewing contracts are spend you've already promised, whether or not the invoice has arrived.

From there, split costs into two buckets: keep-the-lights-on (email, hosting for paying customers, payroll systems) and experiments (the growth tool someone wants to trial, the observability upgrade). The split stops product bets from quietly cannibalising payroll, and it makes the kill decision easy when an experiment doesn't earn its line. Flag the contractual cliffs explicitly — the date a seat minimum kicks in, the auto-renewal window — and put spend on a shared dashboard cut by customer or feature where you can, so the conversation is "feature X costs $400 a month to serve" rather than "the AWS bill went up again".

## Making the credits last

Cloud credits feel like free money, which is exactly the danger: architectures get designed around free compute, and the expiry date arrives like a repossession notice. Treat credits as an asset with a maturity schedule. Catalogue every provider credit, its expiry and which workloads are eligible. Burn credits in low-risk environments first — sandboxes and QA — while you tune the optimisation tactics that outlive them: rightsizing over-provisioned instances, scheduling shutdowns for anything that sleeps at night, and using spot capacity for interruptible work. Set budget alerts at 60, 80 and 100 per cent of expected usage so drift gets caught as a course correction, not a fire drill.

The monitoring toolkit is deliberately unheroic. Centralise billing exports into a warehouse or even a spreadsheet, so nobody is copy-pasting invoices at midnight. Tag resources by team, feature and environment — tags are what turn a raw bill into the sentence "the growth team's experiment caused last month's spike". Automate a weekly cost digest to Slack or email for each accountable owner, and trigger a lightweight review whenever a line moves more than 15 per cent week-on-week. The rhythm is the point: nobody should ever be surprised by the finance meeting.

## The monthly spend drill

The workshop exercise for this topic is a spend drill you should be able to reproduce for any company you join. The worked example, in Australian dollars, looks like this:

- Google Workspace Business Standard, 12 seats at $11 — **$132**
- AWS compute and storage — **$0 cash** (drawing down a 450-credit balance at about 70% burn)
- Datadog monitoring, 3 engineer seats at $27 — **$81**
- Customer support platform, 6 agents at $20 — **$120**
- Contingency and experiment buffer, 10% of baseline — **$33**

Total cash outlay: **$366 a month**, with credits covering roughly $150 of additional value. Two design choices in that little table matter. The contingency line normalises setting aside 10 per cent for surprises instead of hoping they never happen. And the total is expressed as *cash outlay*, not accrual value, because runway is a cash concept — the credits offsetting AWS are real value, but they are also a cliff to plan for.

To run the drill yourself: duplicate the table with your own stack and contract terms, adjust the assumptions until the cash outlay fits your guardrails, and — the step that produces the actual value — identify one optimisation lever per tool: renegotiate, downgrade, or automate. Done honestly, the drill forces real trade-offs ("keep the monitoring tool or fund a contractor?") and leaves you with next quarter's action list.

## Guardrails and red flags

Vendors have a well-rehearsed playbook for young companies, so it pays to have counter-moves ready. When a vendor pushes a multi-year deal before product-market fit, the discount is flattery and the term is a mortgage on your optionality — counter with quarterly. When usage spikes without a matching revenue signal, pause the automation rollouts and investigate before the spike becomes the new baseline. Silent auto-renewals are defeated by the least glamorous control in this course: a calendar hold 60 days before every renewal date.

> The reputational red flag is internal: founders who ignore their own chargeback and usage data erode trust with finance and investors faster than any single overspend. If the numbers exist and leadership won't look at them, why would anyone believe the forecast?

## The investor dividend

All of this discipline pays a second dividend in the boardroom. A monthly FinOps scorecard — spend versus forecast, credits remaining — signals control without a single slide of adjectives. Concrete optimisation stories land even better: when Sarah can say "rightsizing bought us two extra months of runway", the room pays attention, because most founders can't attribute runway to an operational decision at all. Variance explanations ("support costs rose 20% because we onboarded the enterprise pilot") demonstrate that spend is connected to strategy rather than drifting alongside it. Some teams go further and invite an investor observer to the quarterly FinOps review — converting what would otherwise be a due-diligence grilling into a collaboration months before the next raise.

Sarah's action plan, transplantable to any startup you land in: stand up a weekly cost review with engineering and finance; build one central ledger of credits, renewal dates and owners so the knowledge stops living in someone's inbox; pilot the monthly spend drill with leadership and then cascade it to team leads; and revisit the guardrails at every funding milestone so the controls scale with the company instead of strangling it. None of this requires a finance degree. It requires the professional habit — rare enough to be a career advantage — of treating every subscription as a claim on runway and being able to say, with numbers, whether it's earning its keep.
