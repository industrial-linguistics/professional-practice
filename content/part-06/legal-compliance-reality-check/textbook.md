"We'll sort compliance after launch" is one of the most expensive sentences in startup vocabulary, mostly because the deadline isn't yours to set. The enterprise pilot you're chasing sends its security questionnaire *before* the second sales call; the investor's diligence checklist arrives with the term sheet. Contracts, audits and pilots die quickly when a company cannot evidence basic compliance hygiene, and regulators and investors both expect intent to be documented early — even while the stack is still duct tape and shared logins. The point of getting ahead of obligations isn't bureaucratic virtue. It's keeping trust intact with customers who are handing you sensitive data while your engineers ship at speed.

The good news, and the actual content of this reality check: "good enough" compliance for a lean team is smaller, cheaper and faster than the folklore suggests.

## The milestones, demystified

SOC 2 in particular has acquired a mythology of years and rooms full of consultants. The real timeline for a focused small team looks like this:

- **Founding (months 0–3).** Policies drafted, access reviews tracked in a spreadsheet, vendor privacy assessments noted. Honestly costed, this is two to four working days of concentrated effort — a long weekend of adulthood, not a project.
- **SOC 2 Type I.** Controls designed and evidenced for a point-in-time audit, with a readiness assessment signed off. Three to four months with an external coach. Type I can genuinely land within a quarter if one person owns it, templates are reused, and evidence pulls are rehearsed monthly.
- **SOC 2 Type II.** The same controls proven to *operate* over three to six months, which is why the audit window can't be compressed. Plan on nine to twelve months from kickoff, and automate the access reviews and log collection early — auditors are watching the controls run, not reading your intentions.
- **ISO 27001.** Risk register, Statement of Applicability, internal audits and management review: twelve to fifteen months with a staged scope.

Knowing these numbers is itself a professional skill. When a salesperson promises a prospect "SOC 2 by next quarter", you are now the person in the room who can say which half of that promise is achievable.

## Making audits survivable at twenty people

Small teams pass audits by being organised, not by being big. Appoint a single owner — typically the COO, a security lead or a fractional CISO — plus one project-manager type to chase evidence. Use the tooling you already have: a ticket queue for control tasks, password-manager exports, MDM screenshots, change logs. The habit that separates calm audits from miserable ones is rehearsal: pull the evidence monthly, so nothing lives only in someone's inbox or head, and the audit becomes a filing exercise rather than an archaeology dig. Automate early where automation is cheap — cloud security posture tools, HRIS-to-identity-provider sync, log retention policies — because every gap you close before the auditor arrives is one that never makes the findings list.

## Open source licences are legal obligations, not vibes

Engineering teams pull in GPL, Apache and MIT libraries all day without a second thought, and most of the time that's fine — but licences travel with your code, and customer audits increasingly ask about them. The baseline discipline is a software bill of materials (SBOM): a maintained list of dependencies and their licence types. For copyleft components (GPL family), document how you meet source-provision obligations, including the network-interaction variants — this matters most if you distribute binaries or build on AGPL code. Even the permissive licences carry duties: Apache and MIT require attribution, which in practice means shipping a NOTICE file in the repository and product help centre.

Give library approval an owner, wire dependency updates into the security patch cycle, and record the licence posture where vendor assessments can find it. The cost of this is an afternoon a month. The cost of discovering a GPL obligation during due diligence for your acquisition is considerably more, and it will be discovered — licence scanning is now a standard diligence step.

## Privacy by design when you're shipping fast

Privacy review has a reputation as the blocker that kills launch dates, which is why the lean version is built for speed. For each new feature that touches personal data, map the flow — what's collected, where it's stored, which processors see it, how long it's retained. Run a quick data protection impact assessment (DPIA) from a template: fifteen minutes to log the risks, mitigations and who approved, which beats retrofitting controls after an incident by several orders of magnitude.

Default to data minimisation — drop optional fields, anonymise analytics, keep test data out of production — because data you never collected can't leak, can't be breached and never needs a deletion workflow. Build consent capture and deletion workflows once, as reusable components, so each squad isn't reinventing them under deadline pressure. And know when to escalate: routine cases run on the checklist, but cross-border data transfers and sector-specific rules go to legal counsel or an external advisor. The division of labour is the design: product squads handle the everyday cases, experts handle the exceptions.

> The 15-minute DPIA is a genuine trick of the trade. Teams that make it a launch-checklist item ship *faster* than teams that don't, because privacy questions surface while the design is still cheap to change — not in a panicked rewrite after a customer's counsel starts asking questions.

## Who actually does this work

At twenty people, nobody's title says "compliance", so the work lands on whoever combines meticulous note-taking with calm stakeholder management — often a fractional CISO on a few days a month, a security program manager, a privacy counsel on retainer, or an ops lead who discovered they were good at it. The entry pathways are broader than students expect: support engineers who wrangled their first audit, paralegals moving into tech, security analysts stepping up into governance. The defining trait is translation — turning legal clauses into engineering tickets and engineering reality into audit evidence. And the career ladder is real: compliance coordinator to trust-and-safety lead to head of security governance or VP of risk, a path that has minted plenty of executives who started by keeping the risk register tidy.

For founders — or the graduate who becomes their first compliance-minded hire — the quick-start checklist is five lines. Appoint a single compliance captain with a documented backup. Centralise policies, risk registers, DPIAs and SBOMs in one version-controlled place. Schedule quarterly control walkthroughs with engineering, product and legal. Budget for at least one external audit-readiness review a year. And celebrate the small wins — a policy gap closed, an access review automated — so the culture reads compliance as momentum rather than drag. That last item is not decoration: compliance programs die of resentment more often than of complexity, and the fix is making progress visible.
