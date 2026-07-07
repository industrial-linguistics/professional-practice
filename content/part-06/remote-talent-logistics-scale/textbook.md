The previous topic taught Sarah's startup to survive remote work. This one is about what happens when survival tactics meet scale. Somewhere around eighty contributors spread across six or more countries, the "one ops person with a spreadsheet" era ends — not gradually, but all at once, usually during a hiring surge that coincides with a contractor rotation and an executive travelling with a dying laptop. Three people approving every purchase worked at twenty staff. At a hundred, with parallel hiring sprints running in Manila, Warsaw and São Paulo, it's a bottleneck with a personality.

The mental shift that fixes this is worth stating plainly: logistics becomes a product. You're not shipping laptops; you're shipping a first-day experience, repeated hundreds of times, with a service level. The goal is that every hire is productive within 48 hours of their start date — device ready, core access working — without anyone begging for favours across time zones. That means replacing heroics with systems: think of it as moving from a craft table to a production line, while keeping the same care for each new teammate.

## Hardware standards that survive contact with growth

The anchor is the persona kit. Instead of negotiating every laptop individually, you publish standard kits per role type — engineer, customer-experience, executive — each with approved SKUs, accessories and MDM baseline attached. Procurement knows what to order, finance knows what it costs, and your automation scripts know what to enrol. When someone wants an exception, they're arguing against a published standard rather than a person, which changes the conversation entirely.

Personas also make inventory maths possible. Hold a 5–10% buffer of stock per region, staged in bonded warehouses or MSP lockers, so a replacement or a surprise hire never waits on a trans-Pacific shipment. Devices go out pre-imaged with tamper seals and a welcome pack, and every serial number lands in the asset database before the box leaves the shelf. Then, quarterly, review the vendor lineup and refresh specifications — on a schedule, so the standards evolve without derailing procurement or breaking the enrolment automation that depends on them.

## Lifecycle visibility, from purchase order to e-waste

Shipping the device is half the battle; knowing where it is turns out to be the other half. At scale you need a single dashboard tracking every device from purchase order to first login: shipment status, customs holds, delivery confirmation, and a first-day check-in confirming the human actually got working. Customs is the recurring villain here — a held shipment you discover on day one is a crisis, while one you spot four days early is a rebooking.

The reverse flows matter just as much. Failures route through regional depots with prepaid return labels and wipe certificates, so the swap is painless and the data handling is provable. Warranty claims run automatically through distributor portals rather than someone's inbox. Finance gets a feed for capital-expenditure tracking, because a fleet of laptops is a real asset register whether or not anyone treats it as one. And at end of life, contracted e-waste partners on each continent handle compliant disposal and donation — the unglamorous close of the loop that auditors and sustainability reports both eventually ask about.

## Access provisioning without human hands

Hardware without access is an expensive paperweight, so identity has to move at the same speed as the courier. The pattern: the HR or applicant-tracking system is the source of truth, and its events trigger everything downstream. A signed contract fires a SCIM provisioning flow into Okta or Microsoft Entra, which creates the identity and attaches the baseline app bundle for that persona. Nobody files a ticket; the ticket is the employment record.

Technical teams get a further layer — infrastructure-as-code grants least-privilege roles, scoped secrets and repository access, reviewed like any other code change. Service accounts carry expiry dates tied to the contracts that justify them, so no zombie credentials haunt the next audit. Mobile enrolment enforces the zero-trust posture on whatever device shows up. And the joiner/mover/leaver playbooks live in runbooks with explicit recovery targets per access class: how fast must email come back after an outage versus how fast production credentials must die after a termination. Writing those numbers down is what separates a policy from a wish.

## Reviews on autopilot

Provisioning answers "who gets access?"; the harder question is "who still deserves it six months later?" At small scale nobody checks, and access only ever accumulates. At scale, that drift is an audit finding waiting to happen.

The fix is quarterly attestation campaigns run inside the IAM tool itself, routed to managers with usage signals pre-filled — "this person hasn't opened this system in 90 days" is a much easier decision than a bare list of application names. Dormant and over-privileged accounts get flagged for automatic suspension after a grace window, so the default outcome is safe even when a manager ignores the email. Critical systems — finance, source code, production — run on a tighter loop: 30-day reviews with dual approvals. Every remediation leaves an audit-ready trail of tickets, timestamps and revoked roles, which means that when due diligence arrives (and in this course, it always arrives), the evidence already exists.

## Payroll, benefits and the trust ledger

Logistics isn't only devices. Nothing corrodes a remote employee's trust faster than a payslip that's late, wrong, or taxed for the wrong country. Employer-of-record platforms — Deel, Remote, Papaya — integrate with the HRIS to handle contract drafting, tax setup and payslip distribution across jurisdictions your two-person people team could never cover alone. Benefits aggregators such as Ben, Forma or Humaans localise wellness stipends and statutory coverage without a spreadsheet per country.

Two details separate the competent from the chaotic. First, sync time-off calendars and statutory holidays into scheduling and payroll, or you'll deduct leave twice for the same festival — a small error with an outsized emotional cost. Second, maintain a data residency map and limit how far personal data replicates across finance, HR and IT systems. Every extra copy of an employee's passport scan is a liability with no matching benefit.

## Culture that scales with geography

Technology only works if culture keeps pace with the map. Left alone, every distributed company develops HQ gravity: decisions, rituals and visibility pool wherever the founders sit. Counter it deliberately. Regional ambassadors — local champions with a real budget — own welcome rituals, wellness stipends and office hours in their own time zones. Leadership rotates visits and quarterly regional meetups so presence doesn't require relocation. Written cultural playbooks cover meeting etiquette, feedback norms and holiday swaps, so HQ habits don't steamroll local practice by default. And async storytelling — recorded updates, written narratives — blends with live celebration so the company's story isn't told exclusively in one time zone's working hours.

## Steering the machine

Four families of metrics tell you whether the production line is working. Time-to-productive: hardware ready and core access live within 48 hours of start. Access drift: the percentage of accounts needing remediation each review cycle — rising drift means provisioning is outrunning governance. Global payroll accuracy: error rates per country plus the support tickets they generate, a scorecard that finance, security and people ops can share. And the human pulse: logistics satisfaction scores, inclusivity measures, and attrition by region, because attrition clustered in one geography is usually an experience problem wearing a resignation letter.

> If time-to-productive is 48 hours but attrition in one region is double everywhere else, the machine is delivering laptops and failing people. Metrics come in pairs for a reason.

None of this needs to be built in one heroic quarter, but it does need a sequence. Month one: lock the persona catalogues and sign regional logistics SLAs with real service targets. Month two: light up the HRIS-to-IAM automation with audit logging, and pilot payroll and benefits integrations in two countries before going global. Month three: launch the ambassador network with playbooks and budget guardrails, and bake pulse surveys into the operating rhythm. Ninety days from spreadsheet heroics to a system — which, for the IT generalist who builds it, is also a rather persuasive line on a CV heading toward head-of-IT.
