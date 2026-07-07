One mid-sized firm's database licensing fees spiked so sharply that it spent $200,000 migrating from Oracle to PostgreSQL — not because the technology had failed, but because the commercial relationship had. The bill for leaving was the price of never having planned to leave. That's vendor risk in a sentence: vendors make bold promises, but what happens when they change their pricing, get breached, get acquired, or disappear entirely? If your operations depend on them, even a minor hiccup can snowball into a major disruption. Risk management is disaster planning for external relationships — thinking through the "what if" moments before they happen, so you negotiate contracts from foresight instead of scrambling through crises.

## Lock-in: negotiate the exit at the entrance

**Vendor lock-in** is what happens when switching away from a service becomes prohibitively expensive or technically painful. Imagine all your files saved in a format only one vendor's software understands, or a car that only runs on fuel from one specific service station chain. Real examples are everywhere: custom Salesforce integrations that won't export cleanly, cloud platforms with no practical migration path, proprietary data formats that turn "leaving" into a re-keying project. One company spent six months and $50,000 just migrating its customer database to a new CRM.

The mechanism is gradual, which is why it's underestimated. It's like dating someone who slowly moves all your stuff to their place — no single box seemed like a commitment, but leaving suddenly is now a major project. And the power dynamics follow the switching costs: the more trapped you are, the less incentive the vendor has to keep earning your business.

Warning signs are visible in the paperwork before you sign: contracts demanding twelve months' notice to terminate, proprietary data formats, integration fees that grow over time. The counter-moves are equally concrete. Ask, up front, "How do we get our data out if we need to leave?" — and don't accept a paragraph of reassurance as an answer. Ask to see an actual export demonstration *during the sales process*, when the vendor is still motivated to impress you, not after signature when the motivation has evaporated. Negotiate reasonable notice periods and export capabilities into the contract. The principle underneath all of it: when switching is possible before you need to switch, you keep the power in the relationship.

> If a vendor won't demonstrate a working data export while they're still trying to win your business, you already know what leaving will be like.

## Security: you're handing over the keys

Giving a vendor your data is giving someone the keys to your house — you want to know their locks are strong and that they actually watch who comes and goes. That justifies a set of questions no reputable vendor should mind answering:

- Is data **encrypted in transit and at rest**?
- Do staff undergo **background checks** before touching customer data, and are access controls tight enough that not just anyone at the vendor can peek at your information?
- **Where are the servers** — physically? Privacy laws differ by country, and the answer determines which ones apply to you.
- What's their **breach history**? Have they disclosed incidents before, and how long did notification take? A past breach isn't automatically a deal-breaker — silence or slow notification definitely is.
- Can they produce **SOC 2 or ISO 27001 certification** and walk you through their incident response process, including how quickly you'd be told if they were hacked?

The meta-signal matters as much as the answers. A mature vendor hands over the documentation gladly; asking about security shouldn't feel like interrogating a spy. If they dodge, deflect, or offer "trust us" as a control framework — that evasiveness *is* your answer.

Legal exposure rides alongside the technical questions. Contracts should spell out who owns the data, how the vendor may use it, and what liability they carry for privacy or security failures — including insurance coverage and indemnity clauses, which decide who pays when things go wrong. Sector rules stack on top: healthcare providers must verify HIPAA compliance before records touch a cloud, retailers may need PCI DSS for payment data, and some jurisdictions require data to remain in-country — so confirm server locations *and* backup locations, because backups have a habit of quietly living somewhere else. (The previous topics on contracts and legislation cover the clause-drafting in detail; here the point is that these questions belong in vendor *selection*, not just vendor paperwork.)

## When the vendor goes dark

Every vendor claims to have backups. The question that separates marketing from engineering is: have those backups ever been restored in a real emergency? A written recovery plan that's never been executed is a hypothesis. Ask for evidence — test results from drills where the vendor simulated a failure and measured how quickly systems came back. Backup plans are like fire drills: they only work if they've actually been practised.

Continuity thinking then widens beyond any single provider. Could you pivot to a secondary supplier, or at least invoke an exit clause and bring operations in-house? Map escalation paths by severity — who do you call if the service is down for an hour, and who if it's down for a day? — so the outage isn't also an org-chart puzzle.

Then trace your **operational dependencies**, because modern outages propagate. When Slack went down for about six hours in 2021, plenty of teams discovered their chatbots, alerting and help desks all flowed through that single tool — the outage took their *response to the outage* down with it. Document the alternative workflows in advance (when chat dies, which email thread or phone tree takes over?), and budget realistic training time for any replacement system, because "we'll just switch" assumes staff who already know the new tool. It's carrying an umbrella even when the forecast looks sunny — mildly tedious right up until it isn't.

## The money risks

Financial risk assessment has two halves: the vendor's finances and yours.

Yours first. Analyse the licensing model itself: is pricing based on users, data volume, transactions, or something else entirely — and what does your bill look like if the business triples? Per-seat pricing that looks cheap at 10 users can explode to $50,000 at 500. Factor in currency swings on foreign-denominated contracts and the automatic renewal clauses that increase fees annually. The Oracle-to-PostgreSQL story from the opening is what the failure mode costs when it fully matures.

Then the vendor's. A hungry startup may undercut an established firm dramatically — while carrying a real chance of pivoting, being acquired, or folding with your data inside. The incumbent costs more and moves slower, but will still exist in five years. Neither answer is wrong; pricing the difference is the job. Thorough financial review early prevents the expensive surprises later.

## Due diligence, red flags and the exit file

Condensed to a pre-signing checklist, the discipline looks like this:

1. Evaluate financial stability and call customer references.
2. Review security certifications and audit reports — and evidence of tested backups.
3. Test the data export options *before* signing, not after.

And the red flags that should make you slow down: evasive answers about pricing or compliance, an absence of references or only vague case studies, and implementation timelines too good to be true — a vendor promising a six-week enterprise rollout is telling you either that they don't understand the work or that they assume you don't.

Finally, keep a living **exit strategy**, negotiated at the start and maintained thereafter: clear termination clauses and notice periods, documented data migration steps with realistic cost estimates, and a shortlist of alternative vendors you refresh occasionally. You'll probably never use it. Its existence changes every conversation you have with the vendor anyway.

All of this adds up to a stance of disciplined scepticism. Ask about data export before signing; verify the certifications and demand proof the backups restore; document who owns each vendor relationship internally, so every risk has a named human watching it; and hold a quarterly risk review so emerging issues surface while they're still small. None of this is cynicism about vendors — most are competent and well-intentioned. It is the recognition that hope is not a continuity plan, and that the organisations that survive vendor failures are the ones that documented the exit while they still had negotiating power.
