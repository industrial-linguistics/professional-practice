Six months after Meridian Insurance adopted blameless post-mortems, the head of operations asked a fair question in a budget meeting: "These reviews cost us about forty staff-hours a month. How do I know they're working?" The room offered adjectives — things felt calmer, the last big incident seemed to go more smoothly — and adjectives were not what she asked for. Improvement you can't measure is an opinion, and opinions lose budget meetings.

This section is about the small set of numbers that answer her question: metrics that show whether your incident-response and root-cause-analysis process is actually making the organisation more reliable, or just generating well-formatted documents.

## Why measure at all

Five reasons, in roughly descending order of how often they'll matter to you. First, measurement shows whether improvements work — whether the fix from March actually prevented the April repeat, or whether you patched a symptom. Second, it spots repeat issues early: a recurrence trend is visible in a chart weeks before it becomes obvious in anyone's memory. Third, it lets you prioritise with data. Every team has more improvement ideas than capacity; the numbers tell you which category of incident is eating the most recovery time and deserves the next slice of effort. Fourth, it keeps leadership informed in the only language that survives translation up the org chart: trends. And fifth, auditors ask. Compliance frameworks such as ISO 27001 expect evidence that incidents were followed up, and a metrics trail is exactly that evidence, pre-assembled.

## The five numbers worth tracking

You could track dozens of things. Five earn their keep.

- **Mean time to recovery (MTTR)** — the average time from an incident being detected to full service restoration. You met MTTR as a DORA metric in Part 3; here you read it per incident category and watch the trend. If your post-mortems are producing better runbooks and monitoring, MTTR falls.
- **Recurrence rate** — how often the same type of incident reappears within a set window, say ninety days. This is the single sharpest test of your root cause analysis: if the same class of outage keeps returning, your five-whys chains are stopping early.
- **Action item completion ratio** — the percentage of agreed post-mortem fixes that were actually carried out. A team completing 90% of its action items is improving; a team completing 30% is holding meetings.
- **Age of open follow-ups** — how long items have been sitting open. A 200-day-old action item is really a decision to accept a known risk, made by nobody in particular, which is the worst way to make it.
- **Updates sent to stakeholders** — a crude but honest proxy for communication discipline: how many progress updates went out per incident. It matters because silence after an incident corrodes trust faster than the incident did, a theme the communication section of this part takes up properly.

Define each one precisely and write the definition down. "Recovery" means what, exactly — service responding, or backlog cleared? Does the recurrence window reset after a fix ships? Ambiguous definitions produce arguments dressed up as data.

## Tools, in ascending order of ceremony

For a small team, a shared spreadsheet is genuinely fine — one row per incident, columns for the five metrics — provided one named person updates it every week. The habit matters far more than the tooling, and a stale dashboard is worse than a current spreadsheet because it looks authoritative while being wrong.

Beyond that, ServiceNow and Jira will both report directly from your incident and problem records, which is a strong argument for the disciplined ticket-linking covered elsewhere in this part: if the records are linked properly, the metrics fall out for free. Grafana or Kibana can graph MTTR and recurrence trends alongside your deployment metrics, which is where interesting correlations show up — a jump in change failure rate and a jump in recurrence often share a cause. Whatever you choose, make sure it exports to CSV, because when the auditors arrive they will not want a guided tour of your dashboard; they'll want the file.

One placement decision matters more than the tool: where the numbers get looked at. Metrics reviewed only by managers become surveillance, and people respond to surveillance by managing the numbers rather than the work. Metrics reviewed by the team in its own retrospectives become feedback, and people respond to feedback by fixing things. Same data, opposite cultures.

## Acting on the data

Numbers only help if something happens because of them, so build a small routine around each one. Compare trends month to month, and treat any spike as a question rather than a verdict — the interesting part is always *why*. When recurrence stays high for a category of incident, escalate and reopen the analysis: a root cause was probably missed, and re-running the five whys with fresh eyes is cheaper than a fourth outage. When MTTR drops or a post-mortem's action items all close on time, say so loudly — in the team channel, in the monthly report — because celebrated wins are what keep people filling in the tracking data honestly. Review overdue action items in stand-ups, where the conversation is "what's blocking this and should we re-prioritise?", not "why haven't you done it?". And when the evidence says a process isn't working — the completion ratio has sagged for a quarter, say — change the process, not the chart.

> Recurrence is the metric people are most tempted to fudge, because a repeat incident feels like a public failure of the last post-mortem. Watch for quiet reclassification — "it's not the *same* issue, this time the pool exhausted from the read side" — and count the embarrassing way. A recurrence counted honestly costs you a red cell in a spreadsheet. A recurrence hidden costs you the whole system, because every number downstream of it becomes fiction.

Back at Meridian, the answer to the operations head's question eventually took the form of one slide: MTTR for claims-platform incidents down from 3.1 hours to 1.4 over two quarters, recurrence within ninety days down from four incidents to one, action-item completion up to 85%. Forty staff-hours a month suddenly looked like the cheapest reliability programme in the building — and the number of adjectives required was zero.

That's the takeaway. Fixes without measurement are one-off events; measured fixes compound. Track recovery time, recurrence, and whether the promised work actually happens, review the trends with the team monthly, and let the evidence — not the loudest voice, not the most recent trauma — decide where the improvement effort goes next.
