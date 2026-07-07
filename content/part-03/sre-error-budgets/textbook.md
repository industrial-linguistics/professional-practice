Suppose your company promises customers that its app will be available 99.9% of the time. That sounds close enough to perfect that most people file it under "always works." Do the arithmetic, though, and 99.9% allows roughly nine hours of downtime a year — about forty minutes a month. Those forty minutes are not a failure of the promise. They *are* the promise, read from the other side.

Site Reliability Engineering — SRE, the discipline Google developed for running planet-scale services — is built on taking that arithmetic seriously. Instead of treating reliability as a vague aspiration ("the site should stay up"), SRE turns it into maths you can track, budget and spend. The two key instruments are service level objectives and the error budgets derived from them, and together they answer the question every product team fights about: when is it safe to keep shipping, and when must we stop and stabilise?

## Service level objectives

A **service level objective (SLO)** is a measurable reliability target for a service: "99.9% of requests succeed," or "we respond to user requests within two seconds, 99% of the time." A good SLO has two defining properties. It's expressed as a percentage over a time window, and it measures something *user-facing*. Users don't experience your CPU utilisation; they experience slow pages, failed checkouts and error screens. SLOs are written about the latter, because that's what keeps customers — or loses them.

For non-technical colleagues, the honest translation of an SLO is a promise. Hit it, and users stay happy; miss it, and they notice glitches and slow pages whether or not anyone tells them a number was involved. That's why SLOs are monitored continuously — the point is to notice the service drifting out of the acceptable range before the complaints arrive, not after.

> Three acronyms travel together and are worth separating once. An **SLI** (service level indicator) is the measurement itself — the observed success rate this month. An **SLO** is your internal target for that indicator. An **SLA** (service level agreement) is the contractual version, the one with refunds attached, which is why SLAs are set looser than SLOs: you want to breach your own target well before you breach the contract.

The deepest idea in the SLO is choosing a number *below* 100%. Perfect reliability is unattainable — and long before you got there, each extra "nine" would cost more than users would ever notice or pay for. An SLO is an explicit decision about what "good enough" looks like: reliable enough to keep customers, honest enough to leave room for change. Because every change — every deployment, migration and config update — carries some risk, a service that tolerates zero failure is a service that can never improve.

## The error budget

That gap between perfection and the SLO has a name: the **error budget**. At 99.9%, your error budget is the 0.1% of the window in which the service may fail — those forty-ish minutes a month. And the crucial move is in the word *budget*: this is not shameful slack to be minimised, it's an allowance to be spent.

Every incident, outage and burst of slow responses spends some of it. A twenty-minute outage on Tuesday consumes half the month's budget. What remains tells you, objectively, how much risk you can still afford. Plenty of budget left? Ship the ambitious refactor; run the migration. Budget nearly gone? The data is telling you to slow down. And when the budget is fully spent, a pre-agreed rule kicks in: feature releases pause, and engineering effort pivots to reliability work — fixing the flaky deployment process, adding the missing tests, paying down whatever has been causing the incidents — until the service is back within its SLO.

The elegance of this mechanism is who it aligns. Product managers can see, in hours-remaining terms, how instability eats into feature development time. Engineers know exactly when to slow their release pace, without needing anyone to win an argument. The old standoff — product pushing for speed, operations pleading for caution, decided by whoever shouts loudest — is replaced by a number both sides agreed to in advance.

## Burn rate: reading the budget over time

A budget is only useful if you watch the rate at which it's being spent. SRE teams track **burn rate** — how fast the error budget is being consumed relative to time elapsed in the window. Picture a chart with the weeks of a quarter along the bottom and remaining budget, 100% down to 0%, up the side. A healthy service traces a gentle steady slope: routine spending on small incidents, finishing the quarter with budget to spare. A troubled one traces a spiky line — flat stretches punctuated by cliff-drops where a bad release or a cascading failure devours weeks of budget in an afternoon, hitting zero with half the quarter still to run.

Teams commonly mark zones on that chart and attach pre-agreed responses:

- **Green (healthy):** plenty of budget for the time elapsed — keep shipping normally.
- **Amber (caution):** burning faster than the window allows — slow down, defer the risky changes, add extra review and testing.
- **Red (freeze):** budget exhausted or nearly so — stop feature releases and put engineering effort into recovery and prevention.

The point of pre-agreeing the zones is that nobody has to improvise policy during a bad week; the chart makes the call. A fast burn is also diagnostic. It means one of two things: your releases are riskier than your process can absorb, or your SLO is stricter than your architecture can honestly support. Both are fixable — tighten testing and slow deployments in the first case; renegotiate the SLO in the second, if the customer impact genuinely warrants it. An SLO is a decision, and decisions can be revisited — openly, with data, rather than by quietly ignoring the target.

## What error budgets change

Notice what has happened to the conversation. "Is the service reliable enough?" used to be answered with anecdotes and anxiety. With SLOs and error budgets it's answered with a number, and the follow-up — "so can we ship this week?" — answers itself. The framework takes emotion out of decisions that used to be political, which is why it has spread far beyond Google.

For you, entering the industry, the practical takeaway is twofold. First, reliability is a feature with a cost and a target — not an absolute — and you should be suspicious of any team that claims to aim for 100%, because they're really aiming for "we haven't decided." Second, when you're under budget you have earned the freedom to move fast, and when the budget is nearly spent, stability *is* the roadmap. Teams that internalise this stop having the speed-versus-reliability argument entirely. They had it once, wrote the answer down as an SLO, and let the budget referee every week since.
