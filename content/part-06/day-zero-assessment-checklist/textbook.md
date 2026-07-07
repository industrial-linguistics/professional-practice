Sarah closed her seed round on a Tuesday. By Friday she had wired the first payroll run, bought a domain, ordered six laptops, and shared the accounting software password — "admin123" — with everyone who asked, because everyone was busy and everyone needed it. Nobody wrote any of this down. Six months later, a contractor who left on bad terms still knew that password, and what would have been a five-minute offboarding task became a $50K breach notification exercise instead.

That is the problem a day-zero IT assessment exists to solve. In the first 48 hours of a company's life, founders are juggling payroll, domains, customer trials and device orders all at once, while their investors quietly assume security is happening by default. Every shortcut taken in that window — a shared login, an unencrypted laptop, a vendor contract signed from a personal Gmail — becomes technical debt that compounds. A structured checklist freezes the chaos long enough to get intentional about who can touch what, and turns tribal knowledge into a repeatable ritual you can run for every new hire and contractor. It also produces something surprisingly valuable later: a baseline document for MSP handovers, cyber insurance applications and investor due diligence.

## Run it as a workshop, not a document

The assessment works best as a live working session, not a form someone fills in alone at midnight. Block 90 minutes and invite the people who actually flip the switches: the founders, the operations lead, and any fractional CTO or MSP partner already involved.

Start by drawing the current state on a whiteboard before you touch a single control. Seeing that payroll is tied to the bank account, that the CRM feeds the support tool, that the website DNS lives in a registrar account only one founder can access — that context grounds everything that follows. People grasp systems before they grasp checkboxes.

Then nominate a scribe who updates the checklist in real time, so "we should really enable MFA" instantly becomes an owner and a due date rather than a hallway promise. Before moving off each section, pause to log blockers — missing licences, unclear vendor contacts — so they don't drift into the startup graveyard of "we should get around to that someday." The action items go into the task tracker that same afternoon.

## Four blocks, scored honestly

The checklist itself has four blocks, and each line item gets a simple green, amber or red score:

- **Identity** — who has access to what, how accounts are created, and where MFA is actually enforced.
- **Endpoints** — device inventory, hardening steps, and whether you could wipe a lost laptop.
- **Backups and continuity** — what data is protected, whether restores have been tested, and what the manual fallback is.
- **Security and governance** — logging, password policies, vendor reviews and incident contacts.

The traffic-light scoring matters more than it looks. It keeps the conversation focused on risk instead of blame, and it signals where limited time and money should go first. Beside each control, note the system of record — Google Workspace, Okta, the password manager — so anyone reading later knows where truth lives. That clarity is exactly what a fractional CTO or MSP needs when the assessment is handed over: they can see the hotspots at a glance.

## Identity first

Identity leads because every other control depends on who can log in where. Map every system back to an identity source — the HR roster, Google Workspace, Microsoft 365, or a password manager — and record whether MFA is enforced or merely available. Admin consoles, finance tools and anything holding customer data get MFA before the next hire is invited, not after.

Then document the joiner, mover and leaver steps, including the uncomfortable one: who revokes access at 5pm when someone resigns abruptly? Picture Sarah's sales director walking out on a Friday afternoon. Without a documented process, his Salesforce admin rights, his ownership of the customer Slack channels and his access to the shared Dropbox folders all stay live over the weekend — and nobody even notices, because nobody's job is to notice.

Shared secrets belong in a vault with rotation dates, not in spreadsheets or Slack threads. And wherever the mapping exercise turns up personal email addresses on vendor contracts — a founder's Gmail on the Stripe account is the classic — flag it for legal to renegotiate before renewal, while the leverage still exists.

## Endpoints: spreadsheets beat wishful thinking

The endpoint block starts with an asset list: owner, device type, OS version, last patch date. A spreadsheet is perfectly fine at this stage, as long as one named person owns keeping it current. From there, standardise a baseline build — disk encryption on, auto-lock timers set, an approved software image — because consistency stops shadow IT before it spreads.

The control most startups skip is remote wipe. Enable MDM, or at minimum remote lock, before the first travel-heavy sales push. Founders travel, laptops get left in rideshares, and suddenly the company's most sensitive data is riding through downtown in someone else's Tesla. Round out the block by confirming antivirus or EDR coverage, deciding how alerts route to whoever is on call, and writing down the loaner-device process so a day-one hire isn't idle while procurement catches up.

## Backups: two questions and a test

For each data store that would genuinely hurt to lose — source code, CRM, finance records, shared drives, product telemetry — ask two questions. Is there an automated backup? And when did we last test restoring it? Retention has to meet whatever your contracts and tax obligations actually promise, not what feels reasonable.

> One startup lost three months of customer support tickets when their help desk vendor had a data-centre fire. They had assumed "it's SaaS, they handle backups" — right up until they read the fine print and discovered the vendor promised no such thing.

Test a sample restore quarterly and document who validated it, how long it took, and what broke. That anecdote becomes gold when auditors or investors ask about resilience. Plan manual fallbacks too — exporting CSVs, printing key documents, switching to a secondary tool — so the team can keep shipping while a vendor is down. Finally, track the compliance drivers (tax, privacy law, customer contracts) that dictate how long data must stay recoverable, because "we deleted it to save money" is not an acceptable answer to a regulator.

## Where the workloads actually live

Catalogue where everything runs: fully managed SaaS, cloud-native infrastructure, or the closet server humming beside the coffee machine. Cloud-first startups lean heavily on identity providers and vendor assurances, so validate the things the vendor controls — data export options and incident SLAs in particular. Hybrid environments demand more: network diagrams, VPN policies, and a named owner for patching the on-prem gear. And flag data residency constraints early. Some investors, and many enterprise customers, will demand proof of where data physically rests, and retrofitting residency is far more expensive than choosing it up front.

## Spending the money in the right order

Not every red item deserves budget this quarter. Triage controls by risk and runway: what must be solved inside a $500-a-month envelope, and what can genuinely wait for a $5K allocation. The quick wins — enforced MFA, a password manager, baseline device hardening — come before the pricier SIEM and managed-detection contracts, because they eliminate the most common attack paths for almost no money.

Map the bigger spend to business milestones so finance understands why costs jump: Series A, the first enterprise customer, the first regulated market. And capture deferred items with explicit triggers rather than vague intentions — "upgrade logging when monthly recurring revenue hits $250K" is a plan; "improve logging eventually" is a wish.

## Pitfalls, vendors and monitoring

The same failures recur across almost every early-stage company: personal Gmail accounts holding vendor contracts and Stripe access; encryption skipped because "it's just a prototype laptop"; the assumption that vendors handle backups, incident response or compliance without written proof; contractors never offboarded, their privileged accounts active for months; and security tasks treated as best-effort, quietly dying in the backlog the moment sales gets hectic.

Vendor discipline is the cheap insurance here. Build a lightweight intake form covering what data the vendor stores, its access model, compliance attestations and breach history. Ask for security documentation — a SOC 2 report, a pen-test summary — before signing, not after the renewal. Check the termination clauses: how fast can you retrieve or purge your data when the contract ends? Add every vendor to the asset and identity maps so joiner/leaver workflows catch shared integrations, and keep a template questionnaire email ready to fire off the moment someone proposes a new tool.

The security block ties it together: review password policies and SSO coverage, rename or disable default admin accounts, and make sure authentication events, financial transactions and production infrastructure are logged somewhere you can actually search. Draft the incident contact tree now — who calls legal, PR, investors and affected customers — so nobody is inventing a communications plan mid-crisis. Set a vulnerability scanning cadence and patch response windows, and put vendor attestation renewals on the calendar.

## What you walk out with

A good workshop ends with artefacts, not vibes: a scored checklist with red/amber/green status and named owners; a 30/60/90-day remediation roadmap aligned to risk and milestones; refreshed runbooks for account lifecycle, device setup, backup testing and escalation; template emails for vendor questionnaires and customer assurances; starter policies for access control, devices and incident response; quick-reference cards for the emergencies (lost device, suspected phishing, production outage); and an evidence folder of screenshots, policies and contracts for the next audit or funding round. Book the follow-up review before everyone leaves the room, ideally timed before the next hire or investor update.

These assessments are usually championed by fractional CTOs, security-minded operations managers or MSP onboarding leads — and they are a superb shadowing opportunity for junior analysts and IT generalists, who get to watch stakeholder facilitation and control baselining up close. The real skill is empathy: explaining why MFA matters without sounding like the "no" police. Practitioners who master that translation grow into heads of IT, risk leads and customer-trust roles with board visibility.

The takeaway is simple: the checklist is a living playbook, not a one-off audit. Revisit it after every hire, vendor change and funding milestone. When investors or auditors eventually call, the evidence folders and named owners are already there — and the conversation shifts from defensive to confident.
