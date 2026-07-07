Every Monday between 9:00 and 9:20 a.m., Kestrel Freight's booking portal falls over. The service desk knows the drill by now: restart the application server, watch the portal come back, close the ticket. Twenty minutes, textbook incident management, SLA met. It has happened eleven Mondays in a row.

Here's the uncomfortable observation: by every incident-management measure, Kestrel is doing *well*. Fast response, fast restoration, tidy records. And nothing is getting better. The same failure, the same scramble, the same twenty minutes of lost bookings, every single week. Incident management is designed to restore service quickly — it is explicitly *not* designed to make failures stop happening. That's a different practice with a different mindset, and it's the subject of this topic: problem management.

## Incidents and problems are not the same thing

The vocabulary matters, because the two practices pull in opposite directions. An **incident** is an unplanned interruption or degradation of a service. A **problem** is the underlying cause of one or more incidents. Kestrel has had eleven incidents; it has one problem.

Incident management is a sprint: restore service by whatever safe means available, and if a workaround gets users going again, use it — understanding *why* can wait. Problem management is the practice that makes sure "can wait" doesn't become "never happens." It steps back from the individual ticket, analyses patterns across many tickets, and pursues the root cause with the patience incident response can't afford. The two practices even want different things from the same event: the incident manager wants the server restarted *now*; the problem manager would secretly love ten minutes to capture diagnostics before the evidence disappears in the reboot. Mature teams negotiate that tension explicitly rather than pretending it doesn't exist.

## When to open a problem record

Not every incident deserves a root cause investigation — analysis costs skilled people's time, and a one-off glitch with trivial impact may simply not be worth it. Problem management earns its keep in three situations:

- **Repeated incidents pointing at a common cause.** Kestrel's Monday crashes are the canonical case. Any time the service desk finds itself saying "this again," a problem record should exist.
- **High-impact incidents with no obvious fix.** After a major incident, even a one-off, the organisation needs to know why it happened and whether it can recur. If the honest answer to "could this happen again tomorrow?" is "no idea," that's a problem record.
- **Preventing disruption you can see coming.** The proactive side: trawling incident data, vendor security bulletins and monitoring trends for trouble that hasn't struck yet. Reactive problem management asks "why did that happen?"; proactive problem management asks "what's going to happen next?" — and it's a reliable marker of a mature operation.

## Finding the root cause

Root cause analysis (RCA) sounds grand, but its core techniques are disarmingly simple. What makes them work is discipline and evidence, not cleverness.

**The 5 Whys** is exactly what it sounds like: start with the failure and keep asking why until you hit something fundamental. Watch it work on Kestrel's Monday problem:

1. Why did the portal crash? The application server ran out of memory.
2. Why did it run out of memory? A scheduled reporting job spikes memory use at 9 a.m. Mondays.
3. Why does the job spike memory? It loads the entire weekend's bookings into memory at once.
4. Why does it load everything at once? It was written five years ago when weekend volume was a tenth of today's, and it's never been revisited.
5. Why was it never revisited? Nothing in Kestrel's process reviews scheduled jobs against data growth.

Five questions took us from "server crashed" to two findings: an immediate technical cause (fix the job to process bookings in batches) and a process gap (nobody reviews capacity assumptions as the business grows). That second finding is the more valuable one — it's the difference between fixing this problem and preventing the next three like it. Five is a guideline, not a rule; stop when another "why" stops producing anything actionable.

**Fishbone (Ishikawa) diagrams** suit messier situations where multiple factors interact and no single chain of whys captures it. You draw the effect at the fish's head and branch the possible contributing causes along the spine, grouped by category — people, process, technology, environment, suppliers are common groupings for IT. The diagram's real value is social: it structures a workshop, forces the group to consider categories they'd otherwise skip ("could this be a *process* cause?"), and stops the loudest theory in the room from crowding out the others.

Whichever technique you use, two habits separate real RCA from ritual. First, **link the incident records to the problem record** in your ITSM tool. Eleven linked tickets give you timestamps, error messages, affected users and duration — a dataset. Eleven orphaned tickets give you vibes. Second, **gather evidence across teams**. Kestrel's Monday problem touched the application team (the job), Dana's database team (the query behaviour) and the infrastructure team (the memory limits); any single team investigating alone would have seen a third of the picture. And keep the investigation blameless: the question is always "why did the system let this happen?", never "who touched it last?" The moment RCA becomes a search for a culprit, people stop volunteering the evidence you need.

## Known errors and workarounds

RCA takes time, and users are not going to stop working while you diagram fish. Problem management handles the interim with two artefacts. A **workaround** is a documented way to reduce or eliminate the impact of incidents whose root cause isn't fixed yet — for Kestrel, "restart the app server; takes four minutes; here's the script." A **known error** is a problem that has been analysed to the point where the root cause is understood and a workaround is documented, recorded in a known error database the service desk can search.

This is quietly one of the highest-leverage things a support organisation does. When the twelfth Monday crash hits, the L1 analyst who's never seen it before searches the known error database, finds the entry, applies the scripted workaround in four minutes, and links the ticket to the problem record — no escalation, no rediscovery, no heroics. Institutional memory, written down, beats institutional memory in someone's head, because the someone eventually resigns.

## Removing the cause — and checking it worked

Diagnosis without treatment is just expensive documentation. The permanent fix for a root cause is a *change*, which means it flows through the change enablement process from the previous topic: an RFC to rewrite the reporting job, risk-assessed, approved, scheduled, with a back-out plan. Problem management and change enablement are deliberately interlocked — one identifies what must change, the other governs changing it safely.

Then comes the step that turns problem management into a cycle rather than a filing exercise: **review effectiveness**. After the fix ships, watch the linked incident category. Did the Monday crashes stop? Kestrel's did — eleven weeks of failures, then silence, which is the most satisfying flat line in operations. If they hadn't stopped, that's not failure, it's information: the root cause analysis was wrong or incomplete, and the problem record reopens with better data. Either way, close the loop: update the known error database, retire the workaround if it's no longer needed, and feed any process findings (like Kestrel's missing capacity reviews) into continual improvement, which we'll meet later in this part.

> A rule of thumb from the field: problem management is the practice most likely to be quietly abandoned under pressure, because its payoff is invisible — the reward for doing it well is incidents that *don't happen*, and nobody gets a trophy for an absence. Organisations that protect problem-management time anyway are the ones whose on-call rosters slowly get boring. Boring is the goal.

If the detective work appeals to you, this is a career signal worth noticing. Problem analysts and problem managers are the people trusted to run RCA workshops, challenge comfortable explanations, and tell a room of senior engineers that the evidence doesn't support their favourite theory. It rewards curiosity, statistical literacy and tact in roughly equal measure — and it's a common step from senior support roles toward service management leadership. The practical takeaway is smaller and starts immediately: the next time you see the same ticket twice, don't just fix it faster. Ask why it exists at all.
