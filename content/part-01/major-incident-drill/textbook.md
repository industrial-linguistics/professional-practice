At ten o'clock on a Wednesday morning, Marcus Chen stands up in Coralline's operations area and announces that the checkout system is rejecting every payment, in every region, in the middle of the mid-year sale. Nothing is actually broken. This is a drill — a fire drill for IT — and for the next ninety minutes the team will respond as if the outage were real: bridge open, roles assigned, runbook out, clock running. Priya Sharma, two months into her service desk job, has a seat at the table. The reasoning is the same as for the fire kind of fire drill: when the real emergency arrives, you want people executing steps they've practised, not inventing procedure while the adrenaline is flowing.

## What makes an incident "major"

Not every P1 is a major incident. The label — and the special machinery it activates — is reserved for incidents with three properties. They impact critical business services: not one user, not one team, but something the organisation visibly runs on. They require cross-team coordination: no single tier can resolve them, so the escalation lanes from the previous topic stop being enough. And they demand immediate communication: executives, affected staff, sometimes customers all need to know what's happening *while* it's happening.

Checkout failing across all regions during a sale ticks every box. Each minute is lost revenue, abandoned carts and shoppers deciding to buy their cushions elsewhere; the diagnosis could sit anywhere from the network to the payment provider; and the marketing team currently emailing discount codes to half of Queensland urgently needs to know the shop is broken.

Declaration matters more than definition. Someone with authority — at Coralline, the duty incident manager — formally declares a major incident, and that declaration flips the organisation into a different operating mode: normal queue discipline is suspended, a war room or conference bridge opens, and named roles activate. The practical trigger is a judgement call: widespread impact, or an SLA breach on the horizon, plus more than one team needed. The standing advice is to declare early. Standing down a false alarm costs an hour of mild embarrassment; declaring late costs an hour of uncoordinated flailing at the exact moment coordination is worth the most.

## Know the terrain before the fire

The drill uses a concrete scenario because diagnosis is a search problem, and you can't search territory you haven't mapped. Coralline's checkout looks like most modern e-commerce stacks. The web front end is served from a content delivery network, so customers load pages from servers near them. The browser's requests hit an API gateway, which routes them to microservices — one for payments, one for inventory, one for orders. The payment service talks to an external payment provider over the internet; the inventory and order services sit on clustered databases. Monitoring agents watch every layer.

That last detail is what turns architecture knowledge into response speed. "Checkout is down" is a symptom with a dozen possible causes. Monitoring at each layer converts it into something narrower: if the CDN is serving pages, the gateway is healthy and only the calls that touch the payment service are erroring, the search space just collapsed from the whole stack to one service and its external dependency. Teams that know their architecture cold do that narrowing in minutes. Teams that don't spend the first hour of a real outage drawing the diagram on a whiteboard — and if that happens during a drill, the drill has already earned its keep by exposing it.

## Who is in the room

A major incident response is a temporary organisation with named roles, and the roles exist to stop three predictable failure modes: everyone fixing and nobody deciding, engineers being interrupted for status updates, and nobody remembering afterwards what was done or why.

- **The incident commander** coordinates the response. Critically, the IC does *not* touch a keyboard: their job is to set priorities, allocate people, and make the calls nobody else can — do we fail over now, or spend ten minutes gathering diagnostics first? For the duration of the incident their decisions are final; the authority lapses the moment the incident closes.
- **The communications lead** keeps stakeholders informed so the IC and the engineers don't have to. Executives get a summary, the status page gets an honest note, and updates go out on a fixed cadence — "next update at 10:40" — even when there's nothing new, because silence reads as chaos.
- **The technical responders**: front-end and backend engineers chase code paths, database administrators check queries and replication, network operations verify connectivity and DNS, and a liaison works the phone to the payment provider — external dependencies need a dedicated human, because vendors move faster for a named contact than for a ticket.
- **The service desk** holds the front line: fielding user reports with an agreed holding statement, and feeding intelligence back into the room — which regions are calling, what errors they're reading out.
- **A scribe** logs every decision, action and timestamp.

The scribe looks like the junior job and is quietly one of the most valuable. Memory under stress is terrible, and questions like "who decided to restart the gateway, when, and on what evidence?" should never depend on recollection. The timeline the scribe captures becomes the raw material for the review afterwards — and for the root cause analysis later.

## Running the drill

The drill itself has three disciplines. First, assign clear roles fast: Coralline keeps an on-call roster naming the incident commander of the week, so the first step is a lookup, not a debate. Minutes spent negotiating who's in charge are minutes of unmanaged outage. Second, follow the runbook step by step. Runbooks are written in calm daylight hours precisely so that nobody has to be clever at the worst possible moment; if a step turns out to be wrong or missing, that's a finding — surface it, don't silently improvise around it, or the gap survives to ambush the real event. Third, capture decisions and timelines as you go, exactly as you would in production.

Above all: treat it as the real thing, no shortcuts. The value of a rehearsal is proportional to its realism. Priya spends the drill in the service desk seat, practising the holding statement and logging simulated calls — and discovers she doesn't have access to post to the status page. That's a perfect drill outcome: a small, cheap discovery that would have been a large, expensive one at 2 a.m.

## The after-action review

When the drill ends — and equally after any real major incident — the team gathers while memory is fresh and walks the timeline. Three questions: what went well, what didn't, and what surprised us? The framing is blameless; the moment a review becomes a search for whose fault it was, people stop reporting the very near-misses you most need to hear about.

The output must be concrete. Coralline's review produced two fixes: the payment provider's escalation number in the runbook reached someone who'd left that company a year earlier, and nobody in the room knew who could authorise pausing the sale's marketing emails while checkout was down. Both were fixed within a day. Both would have cost twenty minutes each during a genuine outage. Then the last agenda item: book the next drill. Playbooks, like muscles, detrain — teams change, architectures change, and a runbook nobody has walked in a year is a historical document.

> If you find you're good at this — staying level while others spike, holding the whole picture, making calls with partial information — take it seriously as a career signal. Incident commander is a real, recognised capability, and in mature organisations it's a rotation that senior engineers and managers train for deliberately. Calm under pressure isn't a personality trait; it's what practice looks like from the outside.

Three months later, when a payment provider genuinely fell over on a Saturday morning, Coralline's response was almost boring: roles claimed in four minutes, customers informed in ten, service degraded gracefully to a "payments delayed" mode a drill had suggested building. Boring is the goal. In the next topic we look at the tool where all of this — tickets, states, assignments, timelines — actually lives.
