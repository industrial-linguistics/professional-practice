At 9:02 on a Tuesday, two tickets land in Coralline's queue thirty seconds apart. The first: "Payroll portal won't load for anyone in Finance — pay run is due today." The second: "New starter joining Monday, needs a laptop, email account and warehouse system access." Same queue, same polite tone, utterly different kinds of work. The first is a fire; the second is a form. Treat the fire like a form and Finance misses the pay run. Treat the form like a fire and you burn a senior engineer's afternoon on something a workflow could have handled unattended.

The distinction between an **incident** and a **service request** is the first classification every support professional learns, and it's worth learning properly, because everything downstream — urgency, process, metrics, even who's allowed to do the work — hangs off it.

## What makes something an incident

An incident is an unplanned interruption to a service, or an unplanned reduction in its quality. The key words are *unplanned* and *service*. Nobody scheduled the payroll portal to die, and something people depend on has stopped working. That combination triggers a specific mode of response: restore normal service as fast as possible.

"As fast as possible" has a precise implication that surprises newcomers: during an incident, you are not obliged to understand what went wrong. If restarting the application server brings payroll back, you restart it, confirm users are working, and log what you saw. The deep question — *why* did it fall over, and will it again? — belongs to a different practice (problem management, which we'll meet shortly). Incident response optimises for the users' time, not the engineer's curiosity. Workarounds are legitimate wins.

Because speed is the point, incidents get triaged by impact and urgency. The payroll outage affects an entire department against a same-day deadline: high impact, high urgency, drop everything. One person's second monitor flickering is also technically an incident — a degradation of their service — but it queues politely behind the fires.

## What makes something a request

A service request is a pre-approved, standard action: something the organisation has decided in advance it's happy to do, has documented a procedure for, and offers from a catalogue. New accounts, standard hardware, access to a shared drive, a password reset. Nothing is broken. Nothing is urgent in the firefighting sense. The user is asking for something ordinary, and the right response is a defined workflow: capture the details, route the approval to the right manager, execute the steps, confirm completion.

The economics of requests are what make the distinction pay. Because requests repeat — Coralline onboards a couple of new starters most weeks — every step is a candidate for automation, and whatever can't be automated can be handled by the most junior person on the team following the procedure. That's not a slight on junior staff; it's the design. Requests are where new analysts build fluency safely, and every request handled by workflow or by an L1 analyst is senior-engineer time preserved for the incidents that genuinely need it.

The "pre-approved" part matters more than it looks. A request for a standard laptop sails through, because the approval decision was made once, globally, when the item entered the catalogue. A request for something *non*-standard — admin rights to production, say — is not a service request no matter how politely it's phrased. It needs a real decision by someone accountable, which routes it into change territory.

## Four questions that route any ticket

New work rarely arrives labelled. Users report symptoms and make asks; classification is your job. A reliable way to do it is to put four questions to every ticket, in order, and stop at the first yes.

1. **Is a service degraded or unavailable?** Yes → it's an **incident**. Restore service fast, using a workaround if you must, and track how long restoration takes.
2. **Is it a standard, pre-approved ask?** Yes → it's a **service request**. Send it through the catalogue item and its workflow, approvals included.
3. **Are we hunting for an underlying cause?** Yes → it's a **problem**. Problems are investigations: the payroll portal has crashed three Tuesdays running, each incident was resolved with a restart, and now someone needs to find out why and stop the recurrence. No user is waiting on a problem ticket minute by minute; the deliverable is prevention, not restoration.
4. **None of the above?** Then someone wants the environment to be different — new software rolled out, a server reconfigured, a non-standard permission granted. That's a **change**, and it gets planned properly: risk review, approval by whoever owns that risk, and a scheduled implementation window. Changes are how you alter production *without* creating tomorrow's incidents.

Run the 9:02 tickets through the questions. Payroll: degraded? Yes — incident, stop there. New starter: degraded? No. Standard and pre-approved? Yes — request, stop there. Ten seconds each, and both tickets are now on rails that suit them.

The order of the questions encodes a value judgement: restoration outranks everything. If a ticket could arguably be several things, ask first whether anyone is currently unable to work. Only when the answer is no do you consider the calmer categories.

## Why the split is worth defending

The obvious payoff is fit: fires get firefighting, forms get workflow. The less obvious payoff is measurement, and it's the one managers care about.

Incident handling is judged by restoration speed — headline metric **MTTR**, mean time to restore. It answers: when things break, how long do our users bleed? Request fulfilment is judged by turnaround time and user satisfaction: when people ask for routine things, do they get them promptly and pleasantly? Both numbers steer real decisions — staffing, automation spend, whether the on-call roster needs help. But they only mean anything if the categories are clean. Let requests leak into the incident queue and your MTTR looks mysteriously wonderful, padded with hundreds of easy five-minute "restorations". Let incidents leak into the request queue and the damage is worse than statistical.

> A war story that does the rounds at Coralline: a warehouse supervisor once lodged "can't scan barcodes — need a new scanner please" as a hardware request. It sat in the fulfilment queue for two days awaiting a cost-centre approval while an entire receiving dock hand-keyed stock codes. The scanner was fine; the wireless access point above the dock had died. It was an incident wearing a request's clothing, and nobody looked past the label. The lesson stuck: classify by symptom — *is something not working?* — never by whatever fix the user has already guessed at.

Users will always describe solutions ("I need a new scanner", "please reboot the server"). Your job at triage is to hear the symptom underneath and classify that. It's a small discipline with outsized returns: queues stay honest, metrics stay meaningful, and the right seniority of person lands on each piece of work.

You should now be able to take any ticket — however it's phrased — and place it as incident, request, problem or change, and say why. In the next topic we follow the hardest of those, incidents, through the layers of a support organisation: what happens when the first person to touch a fire can't put it out alone.
