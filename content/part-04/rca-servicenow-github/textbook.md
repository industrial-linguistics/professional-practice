"We'll remember to fix that" are famous last words. Every experienced engineer has watched the cycle: an outage, a genuinely excellent post-mortem, a whiteboard covered in insight, a shared document full of action items — and then a sprint deadline, and another, and six weeks later the document is sitting in the personal drive of an engineer who has since resigned. When the same outage returns, the new on-call engineer searches the ticketing system, finds nothing, and starts the investigation from scratch. The failure wasn't the analysis. The failure was memory. Post-mortems have a way of becoming post-mortems themselves — dead and buried in someone's email within a week.

The cure is unglamorous: put the findings where work is tracked, and wire the records together. In most IT organisations that means two systems. ServiceNow (or a similar IT service management tool) holds the operational record — what happened, what it cost, what was decided. GitHub (or GitLab, or Bitbucket) holds the engineering record — the issues, commits and pull requests that implement the fixes. Neither alone is enough: ServiceNow can't show you the code, and GitHub can't show an auditor the business impact. Linked, they turn scattered post-mortem notes into an actionable backlog, keep the root cause attached to its related incidents and changes, preserve an audit trail for compliance reviews, and give planning meetings a ranked list of improvements instead of a vague sense of dread.

When you join a team, two questions will tell you quickly how mature its incident practice is: *where do past RCAs live?* and *who actually reads them?* If the answers are "various places" and "nobody", you've found your first improvement project.

## The ServiceNow problem record

Recall the ITIL distinction from earlier in the course: an *incident* is the fire — restore service now — while a *problem* is the underlying cause that keeps lighting fires. The problem record is where root cause analysis findings belong, created once the investigation has something to say.

A good problem record has a specific anatomy. Start with a short title that leads with business impact: "Checkout failure during Black Friday — DB connection pool exhausted; manual phone orders used as workaround" tells a manager everything they need in one line, where "database issues" tells them nothing. Then the body: a clear timeline, the contributing factors the RCA uncovered, and any workarounds used during the incident — workarounds matter because they're what the support team will reach for when the problem recurs before the fix ships. Link every related artefact: the incident tickets this problem has caused, the change request that will eventually fix it, and any knowledge-base articles written along the way. Finally, assign an owner and a target resolution date. An ownerless problem record is a well-formatted shrug.

The payoff for writing it well is practical: managers can see the impact, which is how fixes get resourced. "Exhausted connection pool" competes badly for budget; "checkout down for ninety minutes on the year's biggest trading day" competes rather well.

## The GitHub half

The problem record says what should change; GitHub issues track the code work that changes it. Open one issue per improvement item, and put the ServiceNow number in the title — "Increase DB connection pool size - PRB0001234", never just "Fix database" — so that anyone searching either system can find the other end of the thread. In the issue description, restate the business impact in plain terms: developers prioritise better when they can see *why* the work matters without leaving GitHub, and a sentence like "this caused the Black Friday checkout outage" outranks any priority label.

From there, normal engineering discipline applies, with the links maintained. Commits and pull requests mention the issue number, so the whole implementation history hangs off one thread. The fix goes through code review like anything else — an RCA action item is not a hall pass around your quality gates, and it's worth asking explicitly who signs off. And the issue is closed only when the fix is deployed to production *and verified*, not when the pull request merges. Merged-but-not-deployed is precisely the gap where "fixed" problems recur. When the issue closes, update the ServiceNow record, and both systems now tell the same story.

## A cadence that keeps them honest

The linkage works when it follows a rhythm rather than relying on anyone's memory.

1. **During and immediately after the incident**: capture everything in a shared post-mortem document — logs, timelines, observations — while details are fresh. This is raw material, not a record system.
2. **Within 24 hours**: distil the findings into a ServiceNow problem ticket so managers and adjacent teams have a clear, findable summary.
3. **Same week**: open a GitHub issue for each action item, cross-linked to the problem ticket.
4. **Weekly**: review the problem record and its linked issues in the team's improvement meeting. Progress, blockers, re-prioritisation.
5. **On completion**: close the GitHub issue after production verification, update the problem ticket, and record the final resolution.

Done this way, the whole arc of an incident is readable in one place years later: outage began 2:45 pm, service restored 4:30 pm, root cause identified next morning, fix deployed two days later, verified, closed. That paragraph — reconstructable in five minutes — is what auditors, new team members and your own future self will thank you for.

## Where it falls apart

The failure modes are few and predictable, which makes them checkable.

- **The link never gets made.** The problem ticket and the GitHub issue drift apart: ServiceNow says open, the code shipped months ago, and nobody can prove the fix happened. Cross-reference at creation time, not later.
- **Vague problem statements.** "Intermittent errors in production" hides the business impact and guarantees the record gets ignored at planning time.
- **Issues open for months with no owner.** An action item without a name and a date isn't a plan; it's a wish.
- **The undocumented hotfix.** Something urgent gets patched straight to production outside the process, works, and is never written down. Two years later it's the change nobody can explain, and one refactor away from becoming an incident of its own.
- **The one-and-done review.** Records checked once, at creation, then never again. Lessons fade at exactly the speed you'd expect.

> A habit that costs thirty seconds and saves hours: whenever you touch either record — a comment, a status change, a deploy — glance at the other end of the link and make sure it still agrees. Divergence caught at one day old is a quick edit; caught at six months, it's archaeology.

The takeaway: ServiceNow captures the process, GitHub tracks the code, and the links between them are what turn an incident into documented organisational learning rather than another "we should totally fix that someday" conversation. There's a personal angle too. Post-mortem follow-through is unusually visible work — managers, auditors and senior engineers all read these records — and the person whose problem tickets reliably trace through to closed, verified fixes acquires a reputation for finishing things. In a field full of brilliant starters, that reputation is rarer than it should be, and it's the one that gets people trusted with problem management, then with teams.
