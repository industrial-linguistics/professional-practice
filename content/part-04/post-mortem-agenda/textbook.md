Left to their own devices, post-mortems drift. Someone opens with a war story, someone else relitigates a decision from forty minutes into the outage, two engineers start designing a fix on the whiteboard, and an hour later the meeting ends with no owners, no dates and a vague sense that everyone should be more careful. The cure is unglamorous: an agenda. A written, repeatable agenda keeps the discussion anchored to facts, gives every incident the same level of scrutiny regardless of who was involved, and — done well — gets the whole thing finished in under thirty minutes.

Timing matters as much as structure. Schedule the post-mortem within 24 to 48 hours of the incident: soon enough that memories and logs are fresh, late enough that people have slept and the adrenaline has drained. A post-mortem held during the outage is firefighting; one held three weeks later is archaeology.

## The seven stops on the timeline

The core of the agenda is a walk along the incident's timeline, and it helps to think of it as seven stops in a fixed order.

1. **Alert** — what triggered detection? Which monitor fired, at what time, and did a human notice it or did a customer phone in first?
2. **Acknowledge** — who took command? When did a responder pick up the alert and start acting? The gap between stops one and two is your response lag.
3. **Restore** — when was service stable again? Note what actually restored it: a rollback, a restart, a config change. This stamp defines your time to recovery.
4. **Impact** — who and what was hurt? Customers affected, revenue lost, operational disruption. Business language, with numbers.
5. **Root cause** — what were the contributing factors? This is where the five whys or a fishbone diagram come in, and it deliberately comes *after* the facts, not before.
6. **Actions** — what will change? Each item gets an owner, a due date and a definition of the evidence that will prove it happened.
7. **Verify** — did the fixes hold? Agree now on when you'll check, and against which metric.

The order is doing real work. Facts come first because they're the least contentious thing in the room — nobody argues about what time the alert fired. Impact comes before root cause so that the analysis stays proportionate to the damage. Actions come last so the team doesn't rush to solutions before understanding the problem. And running alongside all seven stops is the blameless rule from the previous section: describe system conditions and decisions, never hunt for a culprit.

A realistic pacing for a moderate incident: five minutes on the timeline, five on impact, ten on root cause, five capturing action items and confirming owners, five confirming due dates and the follow-up review. Thirty minutes, done. If the root cause discussion genuinely needs longer, book a separate working session rather than letting the meeting sprawl — most of the attendees don't need to be there for it.

## Who's in the room, and why

A good post-mortem needs a specific mix of perspectives, and each seat has a job.

- **Incident responders** bring the technical ground truth — what they saw, what they tried, what worked. They were there at 2 am; everyone else is reconstructing.
- **Service owners** speak to business impact and decide which fixes are worth prioritising. Not every possible improvement earns its cost.
- **A facilitator** runs the agenda, keeps the discussion moving, enforces the blameless rule and deliberately draws out quieter voices. Crucially, the facilitator should not be the person with the most at stake in the outcome.
- **A scribe** captures notes and action items in a shared document or ticketing system, live, so the meeting's output exists the moment it ends. Never make the facilitator scribe; both jobs suffer.
- **A business stakeholder** — someone from the product or customer side — keeps the conversation grounded in user impact rather than drifting into technical trivia.

For a small team these can double up (a service owner can facilitate a post-mortem for someone else's service), but the perspectives all need representing. If nobody in the room can say what the outage cost, the impact discussion becomes guesswork, and guesswork is how trivial bugs get week-long remediation projects while expensive ones get a shrug.

## Documentation: the part everyone skips

The meeting produces understanding; the write-up is what makes that understanding outlive the attendees. Documentation is routinely the most neglected part of the process, which is why the standards need to be explicit.

Use one central template for every incident report, so the reports are comparable and nobody has to decide what to write down while still tired. The template should carry the timeline, the impact assessment, the root-cause analysis, and the action items with owners and dates. Link everything: the ServiceNow or Jira tickets raised during the incident, and the GitHub commits or pull requests that contain the fixes. When a similar issue resurfaces in two years — and it will — the on-call engineer should be able to trace the whole history in ten minutes.

Add the metrics: mean time to recovery, number of users affected, duration of the outage. These feed the trend lines discussed later in this part, and they turn "we think we're getting better" into a graph. Then summarise the lessons learned in plain language — plain enough that the paragraph can be lifted straight into onboarding material or training, because that's exactly where it should end up.

Finally, publish. Store the report in a shared, findable location and announce it to the team, including people who weren't at the meeting. A post-mortem that only its attendees ever read has taught five people what it could have taught fifty.

> A quiet trust-killer: action items that are still open six months later, unowned and unmentioned. Set a recurring calendar entry — quarterly works — to review every unresolved post-mortem action. Teams notice whether these things get finished, and they calibrate their honesty in the next post-mortem accordingly.

## Making it routine

The payoff of all this structure is that post-mortems stop being dreaded and start being useful. A consistent agenda means engineers know what to expect and can prepare their part of the timeline in advance. Consistent roles mean nobody wonders whether they're supposed to be taking notes. Consistent documentation means the organisation accumulates a searchable memory of how it fails and what it did about it — which is a genuinely rare asset, and one that auditors, new hires and future incident commanders will all thank you for.

What you should be able to do now: given yesterday's outage, book the meeting inside the 48-hour window, invite the five roles, run the seven timeline stops in order, and leave behind a linked, metric-bearing report with owned action items and a verification date. That's the whole craft. It isn't hard; it's just discipline, applied every single time.
