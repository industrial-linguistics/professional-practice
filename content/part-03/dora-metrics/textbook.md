Picture the monthly release meeting at Meridian Insurance, a mid-sized firm with a claims platform that most of its two thousand staff touch every day. The head of operations wants to push the next release back a fortnight: the last one caused a Saturday outage. The development manager wants to ship this week: three teams have finished features that customers were promised in March. Both are certain they're right, and the meeting settles it the way these meetings usually get settled — by whoever argues longest.

For most of the industry's history, that was the state of the art. Speed versus stability was treated as a tug-of-war, and every organisation picked a spot on the rope based on gut feel and recent trauma. The DORA research program is important because it replaced the tug-of-war with data.

## Where the metrics came from

DORA — DevOps Research and Assessment — was a research team led by Nicole Forsgren, Jez Humble and Gene Kim, whose multi-year study of software delivery is summarised in the course text *Accelerate*. Through the annual State of DevOps surveys they gathered responses from tens of thousands of practitioners across every industry and company size, then used statistical analysis to work out which practices actually distinguish high-performing technology organisations from the rest.

Four metrics emerged as the core measures of delivery performance, and the headline finding is worth stating carefully: organisations that scored well on these four metrics were roughly twice as likely to exceed their own goals for profitability, market share and productivity. That is a correlation drawn from survey data, not a controlled experiment — you can't randomly assign companies to be bad at deployment — but it has been replicated across years of studies and remains the best evidence we have that delivery performance and organisational performance move together.

## The four metrics

Two of the metrics measure throughput — how fast work flows — and two measure stability — what happens when it lands.

- **Deployment frequency** — how often you successfully release to production. Higher is better.
- **Lead time for changes** — how long a change takes to travel from commit to running in production. Lower is better.
- **Change failure rate** — what proportion of releases cause a problem needing a fix, a rollback or a patch. Lower is better.
- **Mean time to recovery (MTTR)** — when something does break, how long it takes to restore service. Lower is better.

The throughput pair tells you how smoothly work flows through your pipeline. If deployment frequency is monthly and lead time is measured in weeks, changes are queuing up somewhere — waiting for a release window, a manual test cycle, a change advisory board. The stability pair tells you what your speed is costing you. A team that ships daily but breaks production every third release hasn't achieved velocity; it has achieved motion.

It helps to read each metric as a direction of travel rather than a pass mark. A typical organisation starting out deploys monthly; a strong target is daily or on demand. Lead time of weeks should be heading towards under a day. Frequent rework after releases should become rare, with problems caught early in the pipeline rather than discovered by customers. Recovery that takes hours or days should be heading towards under an hour. The DORA reports do publish yearly benchmark bands for "elite" through "low" performers, but the bands shift from year to year. What matters for your team is the trend line, not the trophy.

## The finding that changes the argument

Here is the result that should have ended the Meridian release meeting: in the DORA data, the teams with the highest deployment frequency also had the *lowest* change failure rates and the fastest recovery. Speed and stability were not trade-offs. They clustered together.

Once you see why, it stops being surprising. A team that deploys monthly is pushing a month of accumulated changes in one lump. When that release breaks, nobody knows which of two hundred commits is responsible, so diagnosis is slow and rollback is terrifying. A team that deploys ten times a day pushes tiny changes; when one misbehaves, the culprit is obvious and reverting it is trivial. Frequent deployment doesn't just coexist with stability — it is one of the mechanisms that produces it. The practices you'll meet in the rest of this part (automated pipelines, trunk-based development, fast rollback) are exactly the practices that let both numbers improve at once.

## Using the metrics without weaponising them

Metrics only help if you use them the way the research intended: as a health check on your delivery process, tracked over time and interpreted together.

Track trends, not snapshots. A single week's numbers are noise; the interesting question is whether lead time this quarter is shorter than last quarter, and what changed. Correlate the numbers with business outcomes: if deployment frequency doubled but customer-reported incidents doubled too, the process isn't maturing, it's fraying. And keep the four in balance. The stability metrics exist precisely to catch teams gaming the throughput ones — if deployment frequency climbs and change failure rate climbs with it, the correct response is to slow down and reinforce your automated testing, not to celebrate the first number and hide the second.

> A rule of thumb from Goodhart's law: when a measure becomes a target, it ceases to be a good measure. The moment a manager publishes a league table of teams ranked by deployment frequency, engineers will start splitting one deployment into five. Use DORA metrics to ask questions, never to allocate blame or bonuses.

That last point matters for how the numbers are gathered, too. The healthiest implementations pull the metrics automatically from the pipeline and the incident tracker, where they're hard to fudge, and review them in retrospectives where the team itself decides what to try next.

## What you should be able to do now

You should be able to define all four metrics without notes, explain why the throughput pair and stability pair must be read together, and — most usefully — make the evidence-based argument in the release meeting: shipping smaller changes more often is not reckless; in the aggregate data it is the *safer* strategy. In this part's hands-on exercise you'll build a small pipeline, deliberately break it, and record your own baseline lead time and recovery time. They will be modest numbers from a toy system, but the habit of measuring is the thing being practised. Teams that measure their delivery performance can improve it deliberately; teams that don't are just guessing, one release meeting at a time.
