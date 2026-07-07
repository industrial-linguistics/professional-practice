When your whole company is a dozen people, losing one system for a morning can wipe out a week of bookings and sour customers who took years to win. Worse, small teams run on single points of knowledge: if the only person who knows how to reboot the point-of-sale server is halfway up a hiking trail, a tiny knowledge gap becomes a revenue gap by lunchtime. Business continuity planning is the antidote — not a 90-page corporate binder, but a map of the moments that matter, drawn before you need it. Think of it as operational insurance: a few focused hours now versus weeks of apologising later.

## The market-day outage

This topic's cautionary tale is deliberately low-tech, because continuity isn't a luxury reserved for cloud-native startups. Sarah co-owns a neighbourhood meal-prep shop. She and three teammates run Saturday market orders on Square for payments, Google Drive for recipes, and a single Wi-Fi router in the storefront office.

The night before their biggest farmers' market of the season, the internet provider had a regional outage. The Square terminals couldn't phone home. The shared recipe spreadsheet wouldn't load. Nobody had printed backup recipe cards; nobody had enabled Square's offline card mode. Dawn was spent calling regulars, rewriting shopping lists from memory, and hunting for a working mobile hotspot. They made it to the market — but the cleanup weekend of apologies, rush delivery fees and refunds erased the event's entire profit.

Notice what didn't fail: no server crashed, no data was lost, no one was hacked. A routine ISP outage, colliding with an absence of ten minutes' preparation, converted a good business day into a bad business week. Two trivial mitigations — a printed recipe pack and one settings toggle — would have made the outage a non-event. That gap between "trivial to prepare" and "expensive to improvise" is the whole subject.

## The building blocks

A continuity plan for a small team has five parts, and none of them requires enterprise software.

- **Impact analysis.** List your critical services and ask two questions of each: who notices first when it wobbles, and how long before customer trust or a compliance obligation breaks? This ordering — customer-visible pain first — keeps the plan honest.
- **Recovery objectives.** For each service, set a recovery time objective (how long you can be down) and a recovery point objective (how much data you can afford to lose). These aren't aspirations; they're the tripwires that tell the team when to stop fixing the primary system and switch to a backup or manual workaround.
- **Runbooks.** Capture the decisions in step-by-step playbooks — restoring data, rerouting support, updating leadership, coordinating with vendors — so that anyone on the team can open a document and follow the breadcrumbs, not just the person who wrote it.
- **Testing cadence.** Quarterly tabletop discussions and twice-yearly restore drills, run in calm weather. Rehearsal is what turns a document into a capability.
- **Feedback loop.** After every incident or drill, capture lessons, update the documents, and retire steps that no longer match how the business actually works. A plan that doesn't change is a plan that's drifting from reality.

## Backups that actually restore

Backups are only useful if they restore, and an alarming number of small teams discover the difference during their first real disaster. The essentials: automate daily snapshots for slow-changing files, layer point-in-time recovery onto transactional data, and check that your cloud providers can actually meet the recovery-point targets you wrote down. Keep at least one copy isolated from the primary environment — a different cloud region, an encrypted drive at the office, or a managed backup service — so the failure that takes out production can't take out the safety net too.

Then the discipline most teams skip: every quarter, boot the backups in a staging space and confirm they open, import and connect the way you expect. "The files exist" and "the system works from the files" are very different claims. Document retention periods and legal-hold requirements so an enthusiastic cleanup never purges regulatory evidence or customer contracts. And assign two owners to every backup workflow, so a vacation, an illness or a resignation never leaves the team guessing while a restore clock ticks.

## Communicate like you rehearsed it — because you did

When systems flicker, communication is half the battle, and the middle of a crisis is the worst possible time to wordsmith. Draft the templates now, while you're calm: a status-page post, a customer email, a social update, an internal leadership brief. Each template records who triggers it, who approves the wording, and how often follow-ups go out until things stabilise — a promise of cadence ("next update in 60 minutes") calms people more than technical detail does.

Match the register to the audience: plain-language summaries for customers, tighter technical timelines for partners and regulators who need the gritty details. Keep an SMS or phone tree for the people who must not learn about your outage from social media — key clients, executives, the board. And when the dust settles, archive the final messages alongside a timeline. Those artifacts become postmortem evidence and training material for the next new hire.

## Vendors: lifelines and single points of failure

For a small business, vendors are the infrastructure — which makes them both lifelines and single points of failure. Start with a list of every external tool that revenue depends on — payments, scheduling, shipping — and rate the operational impact if each went dark for a day. Then capture the safety nets that already exist but nobody has turned on: offline modes, mobile hotspots, a secondary domain, a free tier of a rival product that could bridge a bad afternoon.

Talk to the vendors before the crisis. Ask about emergency credits, burst capacity and expedited support, and record account numbers, contacts and the relevant contract clauses somewhere everyone can find. Keep offline copies of contact trees, API keys, setup instructions and invoice histories — the outage that takes your internet down also takes down your ability to google "how do I contact my ISP." Finally, define the low-tech workarounds explicitly: paper intake forms, a cash drawer, a temporary spreadsheet. Customer-facing teams keep moving while systems recover, and customers see a wobble instead of a collapse.

## Who does this work?

In a small organisation, continuity leadership is almost never a full-time job. It's a fractional CTO, an operations generalist, or the compliance-minded manager who quietly loves tidy processes. Entry points are equally informal: a support engineer who volunteers to own incident response, a founder doubling as IT admin, an MSP on retainer. The people who excel share three traits — calm decision-making under pressure, documentation-first instincts, and empathy for teammates juggling anxious customers while the systems misbehave. It's also a genuine career track: ops generalist to continuity lead to head of resilience or enterprise risk as the company grows. Cross-train finance, HR and customer-success leads on the plan too; ambassadors in every function keep resilience prioritised when budgets and attention get tight.

> The lightweight checklist, kept on one page: inventory critical services and owners; write RTO/RPO targets beside each with evidence you can meet them; refresh contact trees, vendor lists and templates quarterly; put drills on the shared calendar with named facilitators; log lessons after every exercise and redistribute the plan.

The through-line is simple: preparedness beats heroics. When backups, communication scripts and vendor contacts are documented and practised, a 2am outage becomes a routine you already know — customers feel cared for, teammates avoid burnout, and when a regulator or investor asks for evidence, the timelines and test logs already exist. Start with one small improvement this week: print the backup recipes, update the contact tree, or book the next tabletop drill. Incremental steps like these are how setbacks become stories of resilience rather than regret.
