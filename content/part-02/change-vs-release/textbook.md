At 4:45 on a Friday afternoon, a developer at Kestrel Freight wants to push "one small config tweak" to the booking portal. Marcus, Kestrel's change manager, has heard this sentence before. The last time someone shipped a small Friday tweak, the portal rejected every booking from Western Australia for two days, and nobody noticed until Monday because the person who made the change was camping.

Two distinct disciplines exist to stop that story repeating, and this topic is about telling them apart. **Change enablement** asks: *should* this change happen, and what could it break? **Release management** asks: given the changes we've approved, *how* do we get them into production smoothly, and who needs to know? They're two sides of the same coin — one controls risk going in, the other coordinates work going out — and confusing them is one of the most common mistakes early-career practitioners make.

## Change enablement: gating the risk

In ITIL terms, a change is any addition, modification or removal that could affect services — code, configuration, infrastructure, even documentation that people rely on operationally. Change enablement exists to maximise the number of successful changes while protecting production stability, which means assessing risk *before* work starts, not after it explodes.

The key insight is that not all changes deserve the same scrutiny. ITIL recognises three types:

- **Standard changes** are low-risk, routine, well-understood, and pre-approved. Adding a user to a group, applying a certified patch to a non-critical server, increasing a disk quota. The risk assessment happened once, when the change type was defined; individual instances just follow the recipe.
- **Normal changes** need individual assessment and approval. Someone — a change authority, which for higher-risk items may be a change advisory board (CAB) of technical and business representatives — weighs the risk, checks the plan, and approves or rejects it.
- **Emergency changes** can't wait for the normal cycle: a security hole being actively exploited, a broken service that needs a fix *now*. They still get assessed and approved, just faster and by fewer people, with the paperwork completed retrospectively.

Matching scrutiny to risk is the whole game. A change process that forces a two-week approval cycle onto password resets doesn't reduce risk; it teaches people to route around the process, and changes that happen outside the process are precisely the ones that take production down. Marcus's rule at Kestrel: make the safe path the easy path. The more changes he can safely reclassify as standard, the more attention the CAB can give the genuinely dangerous ones.

## Following a minor change through the process

It's worth walking one change through the machinery end to end, because the flow reveals how much thinking is baked into even the "minor" path.

![The ITIL minor change process flow, from change request through implementation, verification and CMDB update](images/itil-minor-change.png)

The requester — say, Dana's database team wanting to bump a server's memory allocation — creates a **request for change (RFC)**. The service desk or change management function logs and categorises it, then hits the first decision point: *is this actually a minor change?* If not, it's routed to the normal or emergency process and this flowchart ends. If it is, the next step is to confirm it matches a **pre-approved authorisation** — that is, it genuinely fits the template of a standard change, rather than being a risky change wearing a minor change's clothing.

Then the technical team plans and schedules the implementation, does the work, and — this step matters — **verifies** that it succeeded. Not "the script ran without errors," but "the service behaves the way it should." If verification fails, the team initiates the **back-out plan**, restoring the previous state, and the change goes back for review, rescheduling or cancellation. Note the quiet implication: the back-out plan existed *before* implementation started. Writing a rollback procedure at 2 a.m., mid-failure, with a director on the phone, is not a plan; it's improvisation with witnesses.

Finally — and students skip this step in every simulation until it's beaten into them — the team **updates the CMDB and closes the record**. The configuration management database (covered in its own topic later in this part) is only trustworthy if every change updates it. A change process that ends at "it works" rather than "it works and the records reflect it" is slowly poisoning every future troubleshooting session.

## Release management: shipping the work

Approving changes one by one doesn't tell you how they reach users. Release management picks up where approval ends: it packages related changes into a coherent release, schedules deployment into agreed release windows, and communicates what's shipping to everyone affected.

Think of a magazine publisher. Individual articles get written and edited on their own timelines, but readers don't receive articles one at a time — they receive an *issue*, assembled, checked as a whole, and published on a known date. Release management does the same for software and infrastructure: version 2.4 of the booking portal might bundle a dozen approved changes — two features, six bug fixes, a security patch, three configuration updates — tested together, deployed together, and announced together.

The coordination work is unglamorous and essential:

- **Release windows.** Kestrel deploys portal releases on Tuesday nights, when freight bookings are at their weekly low. Windows are negotiated with the business, not decreed by IT — a release window in the middle of end-of-month invoicing is a self-inflicted incident.
- **Bundling and dependencies.** Changes that interact must ship together or in the right order. The database schema change goes out before the application version that depends on it, never after.
- **Communication.** Release notes for users, a heads-up to the service desk (who will take the calls if anything's off), and clear entry in the change calendar so nobody schedules conflicting work. When the service desk learns about a release from a confused caller, release management has failed regardless of whether the deployment worked.

## Two disciplines, one outcome

Put them together and the division of labour is clean: change enablement gates the work; release management plans the rollout. The gate ensures each individual change is worth its risk. The rollout ensures approved changes reach production in coherent, well-communicated batches instead of a random dribble. When both are working, something valuable happens to the organisation's mood: stakeholders know who approves what, when new features will appear, and what to do when something looks wrong. That predictability is what lets teams ship *faster*, not slower — confidence is a prerequisite for speed.

> If you've read anything about DevOps, you may be bristling: doesn't continuous deployment ship dozens of releases a day, with no CAB in sight? Hold that thought for Part 3. The short version: high-performing DevOps teams haven't abolished change enablement — they've automated the risk assessment and converted almost everything into standard changes, so the pipeline itself is the change authority. The principles survive; the meetings don't.

For your own career, notice that both disciplines are actual jobs. Change managers and release managers sit at the junction of technical teams, business stakeholders and process — roles that suit people who can read a technical plan critically *and* run a meeting where the network team and the application team disagree. And even if you never hold either title, you'll live inside these processes from your first week: the RFC you raise, the release notes you write, the back-out plan a reviewer demands. Write them like they matter, because on the bad Friday, they're the only things that do.
