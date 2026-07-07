"Day zero" sounds dramatic, but it means something quite mundane: the first five business days of a company's existence, when incorporation paperwork, domains, devices and baseline tooling all race to go live at once. Miss a step and you spend week two chasing paperwork while customers wait — or, worse, you discover the gap months later when a contractor's invoice arrives and "Awesome Startup LLC" turns out never to have been registered. Nothing kills the entrepreneur vibe faster than admitting you're technically still a sole proprietorship.

Day zero is not just IT running off to configure email. It's a cross-functional sprint covering legal filings, banking, identity, communication and knowledge systems, with a named owner for every task and evidence you can later show an MSP, an investor or an auditor. The goal is a coherent plan, mapped out before the first hire even signs their contract.

## Incorporation and registrations

Start with the boring layer, because everything else depends on it. Lodge the legal entity, appoint directors and open a business bank account. Secure tax IDs and payroll registration before the first contractor invoice lands — "boring" stops being boring the moment someone asks to be paid and the payroll IDs aren't ready.

Two documents prevent the ugliest disputes later: a documented ownership structure and signed founder agreements. Startups have imploded over a departing founder and a handshake deal that nobody wrote down. Put the incorporation artefacts, board resolutions and founder agreements into a data room folder from day one. When due diligence eventually happens — and if the company succeeds, it will — that folder turns an interrogation into show-and-tell.

## Domains, DNS and website plumbing

Domains feel simple: buy the .com and you're done. In practice, register the primary domain plus the defensives — .co, relevant country codes — before a squatter does it for you at a thousand times the price. And put the registrar account under a shared operations email, never a founder's personal inbox. The failure modes are legion: the registrar tied to a personal Gmail nobody can access while the founder is on a plane; the domain controlled by the CEO's ex-partner who decides to get creative during the breakup; the college-era Hotmail account that quietly lapses along with the renewal notices.

Set up DNS hosting with templated records for MX, SPF, DKIM and the various verification tokens that every SaaS tool will demand. Then add uptime monitoring, so a silent DNS change doesn't break email on launch day.

This matters because DNS mistakes are spectacular in their blast radius. Sarah — the CEO whose startup we'll follow through this part of the course — registered her company's domain under her personal email and "learned DNS" at 1 a.m. Experimenting, she deleted the wildcard record, which took the product demo site offline for six hours. Sales woke up to bounced customer emails; an investor called before breakfast asking about the outage; every meeting that day had to be rescheduled. The fix was not heroic engineering. It was shared registrar access held in a vault, documented DNS records, and change windows — yes, change windows, even for a ten-person company. Real examples teach better than theoretical checklists, and this one cost Sarah a day of pipeline to learn.

## The productivity suite and identity backbone

The Google Workspace versus Microsoft 365 debate still sparks strong opinions, but the deciding questions are practical: which ecosystem do your customers expect, and what integrates with your toolchain? One B2B SaaS startup picked Google Workspace simply because its enterprise buyers expected Google SSO integration. Cost differences are real but modest at this scale — Google Workspace Business Standard runs about $12 per user per month against Microsoft 365 Business Premium at $22, and the Microsoft price buys you more built-in security tooling.

Whichever you choose, establish it as the primary identity provider and enforce MFA on admin roles from hour one — that cannot wait a month. Create shared mailboxes (hello@, finance@) and delegated calendar access for the founders, so company correspondence doesn't fossilise in one person's inbox. And even if "HR" is currently a spreadsheet, sync it against the identity system so joiners, movers and leavers stay in lockstep. The habit matters more than the tooling.

## Communication and knowledge hubs

Stand up chat — Slack or Teams — with channels pre-built for founders, delivery, customers and incidents. Then, on the same day, launch a lightweight knowledge base: Notion, Confluence, even a Google Site. A single page is enough to start. The point is deciding, deliberately, where policies, SOPs, meeting notes, board decks and investor updates live, so the company's history doesn't scatter across chat scrollback and personal drives.

Pre-create templates for announcements, incidents and customer escalations. Templates feel bureaucratic until 2 a.m. on the night something breaks, when the difference between "fill in the blanks" and "compose a customer apology from scratch while the site is down" is measured in customers kept.

## Devices: buffers, budgets and the gaming laptop

Hardware always turns up late unless you plan buffers. Order laptops with baseline images, asset tags and shipping templates ready to go, and order more than you strictly need — for a two-person team, buy three, so a backup exists for demos and travel hiccups. Budget $1,500–2,000 per laptop once warranty, MDM licensing and shipping are included. Allow two to three weeks for procurement, imaging and the inevitable shipping delay.

Pre-stage admin accounts in your MDM — Apple's Automated Device Enrollment or Windows Autopilot — before the boxes leave the supplier, so a new laptop configures itself out of the carton. Document the loaner process and assemble travel kits: power adapters, privacy filters, LTE dongles. Track serial numbers, warranty dates and assigned owners in the asset register so replacements aren't a scavenger hunt.

> There is always one founder who insists on a $4,000 gaming laptop "for better performance." It will receive its baptismal coffee spill during the first investor meeting. Standard images on standard hardware exist for a reason.

## Security guardrails on hour one

Security feels like overkill before the first customer signs — which is exactly when attackers prefer to strike, because the defaults are still wide open. The hour-one guardrails are cheap and fast: a team password manager (1Password for teams is about $8 per user per month), a phishing-reporting button, and bite-size security awareness modules rather than an annual training slog. Turn on default logging, backup policies and conditional access before inviting new users, not after.

Two less obvious items belong on the list. First, break-glass accounts: emergency admin credentials protected by hardware keys, stored off-site under dual control, for the day the identity provider locks everyone out. Second, the contact list: add the founders to the incident bridge, and make sure they know who to call — legal counsel, the cyber insurer, incident responders — before something goes sideways. Microsoft Defender for Business or the Google Workspace security centre cover baseline detection without a dedicated security hire.

## Money, compliance and the first-week runbook

Budget-wise, reserve $200–500 a month for productivity licensing, domain registration and DNS hosting, and line up $1,000–3,000 for incorporation legal fees plus trademark searches. Pre-approve founder credit cards so vendor sign-ups don't stall at a payment screen waiting for whoever holds the company card.

Compliance starts earlier than most founders expect. Check whether early contracts mandate specific data locations or certifications. Document which services store data in which regions — Slack in the US, email in the EU — so nothing surprises you when a customer's procurement team asks. Draft a lightweight privacy policy before collecting any customer information, and flag GDPR, CCPA or industry rules early enough that they can shape the vendor shortlist and architecture, rather than forcing a migration later.

To keep the week moving, run it like a small project: a Kanban board with day-zero tasks, owners and links to completion evidence; a daily 15-minute stand-up to clear blockers and surface vendor delays; and short walkthrough videos recorded for each critical system so future hires can ramp without live hand-holding. Note the external dependencies — lawyers, accountants, MSPs — and pre-book escalation contacts before you need them urgently.

## The takeaway

A disciplined day-zero setup makes incorporation, domains, devices and security feel intentional rather than improvised. The checklist you build this week isn't a launch-party artefact; it's a living runbook that has to survive founder vacations, vendor turnover and the first due-diligence call. When it's all documented, the team gets to focus on customers instead of hunting for the DNS login — and when the investors ring, you have answers instead of apologies.

Your assignment, when you reach the tutorial: draft a day-zero checklist for a hypothetical startup, and mark explicitly where outside experts — lawyer, accountant, MSP — are required rather than optional.
