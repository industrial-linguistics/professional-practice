Policy memos don't build reflexes; rehearsal does. This capstone is your chance to break things safely: a ninety-minute group exercise that pressure-tests a fifteen-person startup's toolchain, culture and vendor choices without touching anyone's production stack. You'll practise red-team curiosity, blue-team calm, and the facilitation skills that keep stakeholders engaged instead of defensive — then translate every insight into a maturity score and a remediation backlog that leaders could actually fund. Along the way it showcases the cross-functional cast — fractional CTO, security lead, customer success, ops — that makes improvements stick after the workshop ends.

## The scenario on the table

The subject is Sarah's marketplace startup: fifteen people, a mix of founders and contractors, shipping weekly product updates to a global customer base. The stack is modern but stitched together — managed Kubernetes, GitHub Actions for CI/CD, Google Workspace, Notion, HubSpot and Stripe. Three third parties sit inside the trust boundary: a fractional SOC provider, an MSP handling endpoints, and an offshore data-labelling partner. The pain points are already on the table, because this is a diagnosis exercise, not a treasure hunt: ad-hoc onboarding, shadow SaaS creep, almost no incident rehearsal, and compliance debt that chases the team into every enterprise sales call.

The scenario is deliberately ordinary. This isn't a hardened fintech or a naive lemonade stand — it's roughly half the startups you will actually join, which is what makes the findings transferable.

## Pods, timeboxes and tone

Participants form pods of five or six: red-team analysts, blue-team responders, a business stakeholder and a scribe. The business voice is not decorative — a risk that can't be explained to sales or support isn't finished. Ninety minutes goes fast, so the facilitator guards four timeboxes: twenty minutes of recon, a thirty-minute incident drill, twenty-five minutes of debrief, and fifteen to prepare the report-out.

The facilitator's other job is tone. Injects keep everyone honest, but the register stays curious rather than accusatory — you are diagnosing a friend's company, not humiliating one. Everything the pods need lives in a shared workspace: architecture diagram, SaaS inventory, contract excerpts and customer personas. Nobody should be guessing about the environment; the scarce resource is judgement, not information.

## Phase 1 — recon and hypothesis building

The red team maps the startup's assets, data flows, trust boundaries and third-party dependencies, then commits to its top three attack vectors — credential reuse, a misconfigured S3 bucket, a vendor breach cascading into production — each with supporting evidence from the materials. The discipline that matters most: every hypothesis is written as an "assume breach" scenario that articulates business impact for the sales, support and engineering leaders. "An attacker could pivot from the labelling partner into the customer database" is an observation; "and that ends the two enterprise deals in the pipeline" is a finding. Threats that can't be expressed in business terms don't get funded, in this room or any other. The scribe logs open questions for the facilitator to answer or park — momentum now, homework later.

## Phase 2 — the simulated incident

The facilitator triggers a scenario, classically a compromised GitHub token leading to tampered container images. The blue team narrates its response out loud: which detection sources would actually fire, the containment steps, the communication cadence, and when legal and finance get pulled in. Then the injects land — the incident collides with a product launch, the MSP's lead engineer is on leave, the SOC's ticket queue is already full — because real incidents never arrive on a quiet Tuesday.

Push the pods to produce artefacts while the adrenaline is flowing: a draft customer update, board-brief talking points, the skeleton of a postmortem. Talking about communication is easy; writing the first three sentences of a customer email during a simulated breach is where the learning actually happens.

## Phase 3 — debrief and maturity mapping

The debrief switches to evidence-based grading. Each pod scores the startup across four dimensions — people, process, technology, governance — on a one-to-five scale, and every score must tie to an artefact: the outdated runbook, the missing tabletop cadence, the single approver on critical releases. Then the observations become a prioritised backlog: quick wins like closing MFA gaps, medium-term plays like renegotiating vendor contracts, strategic bets like platform observability. Finish by capturing the leadership asks — the budget, headcount or policy changes without which the backlog is a wish list.

The maturity model keeps the scoring consistent across pods:

- **Level 1 — Ad hoc:** hero-driven fixes, no defined playbooks, limited logging or third-party oversight
- **Level 2 — Emerging:** basic runbooks, partial MFA rollout, informal retros with inconsistent follow-through
- **Level 3 — Scaling:** quarterly tabletop drills, defined SLAs, vendor scorecards, baseline observability
- **Level 4 — Measured:** automated controls, resilience OKRs, integrated risk dashboards, dedicated budget
- **Level 5 — Optimized:** continuous assurance, proactive purple teaming, shared outcomes with partners

Most honest fifteen-person startups land between levels one and two, and that's fine — the exercise isn't about shame, it's about a sequenced route to level three.

## Deliverables and what good looks like

Each pod leaves with four artefacts: a risk map, an attack narrative, maturity scores, and a top-five remediation backlog with owners and timelines. Visual formats — journey maps, swimlanes, heat maps — earn their keep here, because they anchor executive conversations in something concrete rather than theoretical.

Good work has a recognisable texture. Every maturity score carries an evidence citation. The attack narrative reads like a story an account manager could retell to a worried customer. The backlog is sequenced and roughly costed, not a pile of undated good intentions. And the leadership asks are specific: "a part-time security lead and $20k for observability tooling" beats "more security investment" every time.

## Facilitation and marking guidance

Run the closing debrief in a start-stop-continue format so cultural shifts surface alongside the technical fixes, and end with a commitment round: each participant, in role, states the next concrete action they would champion back at the office. That final round is what separates a memorable workshop from a useful one.

For assessors: reward evidence discipline over exotic attack paths — a boring, well-evidenced credential-reuse chain outscores an implausible zero-day story. Mark facilitation and stakeholder empathy explicitly: did the business voice get airtime, or did the technical members steamroll the room? Check the backlog for owners, timeframes and sequencing. And watch for the classic failure mode, red-team grandstanding while the blue team gets defensive — the tone brief exists precisely to prevent it, and a pod that kept the conversation collaborative under pressure has demonstrated the rarest skill in the room.

## Where this leads

The exercise deliberately mirrors real roles: fractional CTO, security lead, product manager, customer success manager, operations analyst. The entry pathways are just as real — support engineers stepping into incident command, consultants pivoting into virtual-CISO work, ops generalists growing into vendor management. The standout traits are consistent across all of them: facilitation under pressure, systems thinking, empathy for non-technical stakeholders, and genuine curiosity about adversary tradecraft. People who lead exercises like this professionally grow into security program managers, heads of resilience and platform engineering directors.

The takeaway is the one the whole part has been building toward: rehearsal builds muscle memory faster than any policy memo. By red-teaming Sarah's startup together, you leave with evidence-backed maturity scores, a sequenced roadmap, and renewed respect for cross-functional partnership. Treat the session as a dress rehearsal for the next funding-round diligence meeting — and as an invitation to invest in shared accountability before the real incident, which does not schedule itself ninety minutes in advance.
