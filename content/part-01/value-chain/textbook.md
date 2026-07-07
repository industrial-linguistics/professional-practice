In March, Coralline's head of customer service asks for something simple: customers should be able to lodge a return online instead of phoning. Six words of business need. By the time that sentence becomes a working returns portal, it will have passed through planning meetings, stakeholder interviews, a build, a security review, a release, a support roster and — three months after launch — a redesign of the confirmation email that nobody predicted needing. ITIL 4 has a name for the machinery that turns a need like this into running, supported value: the service value chain.

The model describes six activities. They are not steps one to six — real work loops through them repeatedly and in varying order — but each activity answers a distinct question, and healthy organisations can point to where each one happens.

- **Plan** — do we share an understanding of where we are, where we're going, and what we should invest in? At Coralline, this is where the returns portal gets weighed against every other thing the IT budget could buy.
- **Engage** — are we actually talking to the people who need and use the service? Stakeholder interviews, requirement conversations, and the ongoing relationship with users all live here.
- **Design and transition** — will the new or changed service meet expectations for quality, cost and time, and can we move it into production without chaos?
- **Obtain/build** — are the components (code, hardware, licences, third-party services) available, to specification, when needed?
- **Deliver and support** — is the service running as agreed, and are users getting help when it isn't?
- **Improve** — are we getting better, everywhere, all the time?

![The ITIL 4 service value chain: six activities arranged around a continual improvement and feedback core.](images/service-value-chain-continual-improvement.png)

Notice where the diagram puts improvement: in the centre, connected to everything, not bolted on the end. That placement is the whole argument of this topic.

## A relay, not an assembly line

A useful first mental model is a relay race: each activity hands a baton to the next, and value reaches the customer only if every handoff lands. Planning hands a funded, understood piece of work to design. Design hands a tested, documented service to operations. Operations hands live feedback — what breaks, what confuses people, what they ask for next — back to planning and improvement.

The relay picture captures the importance of handoffs but misleads in one way: runners pass the baton once, while service work circulates continuously. The returns portal doesn't exit the chain at launch. Every support ticket it generates is *deliver and support*; every "customers keep asking if we could add photo upload" is *engage* feeding *plan*; the eventual version two goes back through *design and transition*. A service is in the value chain for its entire life.

For each piece of work moving through the chain, three questions keep everyone honest. Who owns this right now? What evidence proves it happened — a signed-off design, a passed test run, a closed ticket? And what handoff comes next? When you can't answer one of those, you've found where the work is about to stall. New team members are often the best at asking them, precisely because nobody has yet taught them which questions are considered impolite.

## Why improvement sits in the middle

The instinct in most organisations is to treat improvement as a project you run when things get bad enough — a "transformation" every few years, in between which processes quietly rot. ITIL 4's counter-position is that improvement is an activity you perform continuously, in small pieces, at every step, and the diagram encodes that by wiring the improvement core to all six activities with feedback arrows.

Three practical things follow. First, quality gets built into each step rather than inspected in at the end: if the design-to-build handoff produced confusion this month, you fix the handoff template now, not in next year's process review. Second, feedback loops become normal work. After the returns portal launches, the support team's ticket data flows back to the designers as a matter of routine — not as an escalation, not as a complaint, just as the ordinary circulation of the chain. Third, the service stays aligned with what the business actually needs, which drifts. Coralline's return volumes double when it starts selling furniture; a chain with working feedback loops notices and adapts, while a chain without them keeps polishing a service optimised for cushions.

Think of a cook tasting the sauce as they go rather than waiting for the restaurant reviews. Each taste is cheap. The alternative — discovering at the end that the whole batch is wrong — is not.

## Making the chain visible

Abstract models earn their keep when they change what you do on Tuesday. The most common way teams operationalise the value chain is embarrassingly low-tech: a board — physical or in a tool like Jira or ServiceNow — with columns tracking where each piece of work sits, from planning through build to live support. Kanban-style boards like this do two things the model alone can't.

They show *where work waits*. If items pile up between design and build week after week, that's not bad luck, it's a signal: maybe the handover checklist is missing, maybe two tools don't integrate and someone is retyping specifications by hand, maybe one approver is a bottleneck. The delay points at the process fault. At Coralline, the returns portal sat in "awaiting security review" for eleven days — not because the review took eleven days, but because nobody knew whose queue it was in. The fix wasn't heroics; it was a rule about assigning reviews within one business day.

They also give you something to measure. "Are we improving?" is unanswerable in the abstract, but "has the time from request to release shrunk since we changed the handover process?" is a number. Measure outcomes, adjust the approach, measure again. And when a team finds a fix — a checklist, an automation, a better form — the chain isn't finished until the lesson travels: written up, shared with the other teams who have the same problem, folded into the standard way of working. An improvement that stays inside one team's heads is a private win; the value chain is meant to compound them across the organisation.

## The takeaway

Continual improvement is what makes the value chain resilient instead of brittle. A chain that only executes will degrade, because the business around it keeps moving; a chain that also observes itself and adjusts gets stronger under load. None of this requires seniority. The habits that drive it — asking who owns the work, what evidence proves it happened, what handoff comes next, and how this step could hurt less next time — are available to you from your first week on a service desk. Ask "how can we do this better?" often enough, with data attached, and you'll be doing the *improve* activity before anyone gives you the job title for it. In the topics that follow, watch for the chain in the background: incident handling is *deliver and support*, escalation paths are its internal handoffs, and the after-action review of a major incident is the *improve* loop running at full speed.
