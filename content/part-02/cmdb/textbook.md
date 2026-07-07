Mid-incident at Kestrel Freight, the booking portal limping, Dana's team has traced the trouble to a struggling database server and the fix is a failover — until someone asks the question that stalls the bridge: "what else is on that box?" There are two versions of what happens next. In one, an engineer queries the configuration management database and answers in thirty seconds: `kf-db-04` also hosts the depot rostering service, so warn that team, then fail over. In the other, the answer is an archaeology expedition — a wiki page last edited two years ago, a spreadsheet called `server-list-FINAL-v7.xlsx`, and the recollections of an engineer who resigned in March. Kestrel gets the first version because it invested in the second-least-glamorous artefact in IT operations. This topic is about that artefact: what a CMDB is, how you build one, and why keeping it truthful is the hard part.

## An inventory, plus the part that matters

A **configuration management database (CMDB)** is the central inventory of an organisation's systems and services. Its records are **configuration items (CIs)** — servers, network gear, databases, applications, SaaS subscriptions — each carrying attributes: version, owner, environment, support group. So far, that's an asset register, and plenty of organisations already have one gathering dust.

What makes a CMDB more is the **relationships**. An asset register tells you `web01` exists and what it cost. The CMDB tells you `web01` serves the booking portal's front end and *depends on* the `db01` database service — which means a change to `db01` is a change to the portal, whether anyone intended that or not. Dependencies are where outages hide, and mapping them is the entire point.

Every practice in this part leans on that map. Incident diagnosis uses it to establish blast radius and to ask "what changed recently near this CI?" Change enablement uses it for risk assessment. Problem management uses it to spot patterns across related CIs. Even the SLA topic quietly assumed it: "the booking portal" in Schedule 4 of Kestrel's supermarket contract is, operationally, a named set of CIs, and you can't defend an availability number for a service you can't enumerate.

## Building one without boiling the ocean

Construction has three steps, each simpler to state than to do.

1. **Identify the key CIs.** Not everything — the services that matter, and the CIs they're built from. Kestrel started with the booking portal chain and payroll, modelled those properly, and expanded outward. A CMDB that attempts to catalogue every cable on day one dies of its own ambition before it's ever useful.
2. **Populate attributes from trusted sources.** Cloud provider APIs, the hypervisor's inventory, Active Directory, procurement records — wherever a system of record already exists, pull from it rather than retype it. Hand-entered data is wrong at birth or wrong within a month; automated feeds are wrong less often and, more importantly, get corrected in one place.
3. **Map the relationships.** *Runs on*, *depends on*, *connects to*. Discovery tooling can infer some of this from network traffic and installed software, but the semantic layer — that this database is what the rostering service actually depends on — needs humans who know what things are *for*. This is the slow, expensive step, and the valuable one.

## The change management handshake

A CMDB and a change process keep each other honest, and the integration runs in both directions.

Going in, every request for change lists the CIs it will touch — Marcus, Kestrel's change manager, won't assess an RFC without that list, because the list is what makes risk assessment mechanical instead of psychic: walk the relationship graph outward from the named CIs and you can see what the change could break, and who needs to be warned. Coming out, an approved and implemented change updates the affected CI records. That's the closing step the change topic insisted on earlier in this part, and here is the reason: the CMDB's claim to be the **approved state** of the environment holds only if every change lands in it.

Then automated **discovery** closes the loop. Discovery tools scan networks, cloud accounts and servers on a schedule and report the **observed state** — what's actually out there, actually configured, actually running. Compare observed against approved. When they match, your records are trustworthy and your change process is being followed. When they don't, you've learned something either way.

## When records and reality diverge

Divergence has four canonical sources, and each one names a different failure:

- **Unauthorised changes.** Someone altered production outside change control — sometimes an emergency fix whose paperwork never happened, sometimes an administrator who couldn't be bothered. Discovery-versus-CMDB comparison is how change control gets teeth: the bypass that used to be invisible now surfaces as a mismatch within a day.
- **Configuration drift.** Small manual tweaks — a timeout raised here, a package updated there — accumulating until servers that are supposed to be identical aren't. No single tweak was worth a change record, in someone's judgement; collectively they've made the environment unpredictable.
- **Unknown devices.** Discovery finds hardware or services the CMDB has never heard of: shadow IT, a team's "temporary" experiment, the box under a bench nobody mentioned.
- **Phantom CIs.** The mirror image — records for equipment retired long ago, still haunting reports, still counted in licence audits, still paged about during incidents.

The response discipline is the same for all four: treat every mismatch as information and run it down. Either the record is stale, in which case you fix the record, or the change was unauthorised, in which case you fix the process or the behaviour. What you must not do is shrug, because trust in a CMDB is binary in practice. A database that's 70 per cent accurate is arguably worse than none: people trust it into mistakes for a while, then stop trusting it, then stop updating it — the death spiral that ends in `server-list-FINAL-v7.xlsx`. Staying out of the spiral takes all three maintenance habits the practice prescribes: update records as changes happen, automate discovery and comparison, and schedule periodic audits to catch what both missed.

> Kestrel's first full audit found thirty-one phantom servers still marked live — and one very real server in no record at all, sitting under a bench at the Perth depot, printing the labels for every Western Australian consignment. It had been "temporary" for four years: never patched, never backed up, never in anyone's disaster recovery plan. The audit took two weeks and was widely resented; discovering that server *during* an outage would have been considerably more expensive. Rule of thumb: any diagram or inventory older than its author's tenure should be treated as folklore until discovery confirms it.

## Why it matters, and to whom

The payoff shows up as speed and absence. Speed, because incident calls stop stalling on "what else is on that box?" and change assessments stop requiring séances. Absence, because the outages caused by unknown dependencies — the ones where nobody knew the rostering service shared a database server — simply stop happening. A well-kept CMDB is the single source of truth that every other practice quietly consults, and like most infrastructure, it's invisible exactly when it's working.

There are careers here: configuration managers own the CMDB's structure and accuracy, and IT asset managers extend the same records into financial and licensing territory — unglamorous titles that senior operations people rely on daily and remember at promotion time. But the more immediate takeaway is a habit that starts in your first job, at any tier: when you touch a system, leave the record as true as you left the system. The thirty seconds that costs you is the archaeology expedition it saves everyone else. And accurate records are about to matter for a different reason — the last two topics of this part are about improving and measuring the operation, and you can't improve what you can't even enumerate.
