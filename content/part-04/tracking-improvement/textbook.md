Every post-mortem ends the same way: a list of confident action items and a shared feeling that this time will be different. The question almost nobody asks eight weeks later is the only one that matters — did any of it work? Did the new staging step actually reduce failures, or did the problem just move somewhere quieter? Teams that don't check are running an improvement theatre: action items pile up, effort gets spent, and whether anything improved remains a matter of vibes.

This section is about closing that loop with data — specifically, deployment metrics and incident trends, measured before and after the changes you make.

## Why trends beat anecdotes

Four reasons to bother. First, metrics show whether fixes actually work, which is the entire point of doing root cause analysis in the first place. Second, they reveal patterns no individual remembers — incidents clustering after Friday releases, severity creeping up quarter by quarter. Third, they support business cases: "we need another engineer" is a request, while "recovery time fell 40% after we automated rollbacks; here's what the next automation would cost and save" is an argument. Fourth, and most under-rated: trends end debates. Part 3 opened with a release meeting settled by whoever argued longest; a visible trend line settles the same argument in thirty seconds, and everyone gets to lunch on time.

## What to collect

The core set is the four DORA metrics from Part 3 — deployment frequency, lead time for changes, change failure rate and mean time to recovery — now wearing a different hat. In Part 3 they described your delivery performance; here they serve as the before-and-after instrument for your improvement work. Alongside them, track incident count and severity, and plot everything on one timeline so deployments and incidents can be read against each other.

Collection is less work than people fear. GitHub Insights and your CI/CD dashboard already know your deployment stats; Jira or ServiceNow already hold your incident history. The step teams actually skip is the baseline: capture the numbers *before* you roll out a new process, because without a before, your after is just a number. If you're proposing a change in next week's retro, tonight is the right time to screenshot the current state.

Read the numbers as connected to humans, not as abstractions. A long recovery time is customers staring at error pages; a high change failure rate is usually inadequate testing or rushed releases somewhere upstream. And read them together: if deployment frequency is climbing but incident severity is climbing with it, the correct response is to revisit your quality gates, not to celebrate the deployment number. The stability metrics exist to keep the speed metrics honest.

## Reading the results

Give a change a few sprints, then compare against the baseline. Did lead time shrink? Are rollbacks rarer? When the numbers improve, show them — a quick dashboard demo in the post-mortem, a trend line in the team channel. A graph moving from two-week deployment cycles to two-day cycles has convinced more leadership teams to keep funding automation than any slide full of adjectives ever has.

When the numbers move the wrong way, resist the urge to explain them away. Dig into the timeline around each spike: maybe the new testing tool genuinely slowed the pipeline; maybe incidents correlate with a Friday release habit. Then invite the team to propose fixes rather than assigning fault — the same blameless stance that runs through this whole part applies to metrics reviews, because the moment a chart becomes an indictment, people start managing the chart.

Translate for management in plain language, proposal attached: "Our recovery time increased last month, most likely due to rushed hotfixes. We propose adding a staging step." That sentence carries evidence, an interpretation honestly labelled as likely rather than certain, and a costed next move — which is exactly the shape of communication that gets approvals. Roll the same material up into quarterly summaries so long-term progress stays visible; week-to-week noise hides improvements that a quarter-scale view makes obvious.

## Staying honest with the numbers

Four disciplines keep the practice trustworthy. **Patience**: real patterns take a month or two to emerge, and reacting to a single week's blip mostly generates churn. **Humility about causation**: correlation doesn't imply causation — though as the saying goes, it does wave its arms and point suggestively. Incidents dropped after the staging step, but the traffic mix changed that month too; hold interpretations loosely and let more data arbitrate. **Vigilance about gaming**: if someone deploys "fix typo" fifty times on a Friday, your deployment count is now measuring enthusiasm, not health. Balance every speed metric with a quality metric like change failure rate, and revisit what you measure when behaviour starts orbiting the metric instead of the work. **Connection to consequences**: use the numbers. One team's documented 40% drop in recovery time secured the budget for an additional SRE; conversely, when three months of data showed a cherished process change had achieved nothing, they dropped it without a fight. Data lets you pivot quickly when things don't work and celebrate honestly when they do.

> Keep the dashboard where the team can't avoid seeing it — the wiki homepage, the wall monitor, the top of the retro agenda. A metric reviewed monthly changes decisions; a metric filed in a folder changes nothing. The half-life of an invisible dashboard is about three weeks.

One clarification to keep this section distinct from its sibling earlier in the part: the follow-up metrics covered there — recurrence rates, action-item completion, age of open items — tell you whether your *improvement process* is being worked. The deployment and incident trends here tell you whether the *system itself* is getting better. You need both, because a team can dutifully complete every action item while the outage rate stays flat — that's a process running perfectly on the wrong fixes, and only the second set of numbers will catch it.

The takeaway fits in two sentences. Metrics turn vague promises into measurable progress: baseline first, change second, comparison third, decision fourth. Teams that run that cycle find out what works while it still matters; teams that skip it find out from their customers.
