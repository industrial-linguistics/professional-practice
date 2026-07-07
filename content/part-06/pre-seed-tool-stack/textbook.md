There's a predictable failure mode in pre-seed companies: the founder signs up for Asana, the designer wants Figma, the engineer prefers Jira, and three months in, nobody can find anything, none of it syncs, and the company is quietly burning $150 a month on tools that fight each other. Every new hire arrives with their own "game-changing" productivity app, and suddenly you're administering more tools than you have team members. Then a diligence call arrives, an investor asks "who administers access to your systems?", and the honest answer is "we'll get back to you."

A curated pre-seed stack exists to prevent exactly that. It keeps the founding team focused on shipping product instead of chasing logins, it shows investors and early customers that basic governance exists, and it avoids the try-every-tool chaos that can quietly burn $500 or more a month. Just as importantly, it creates artefacts — templates, rituals, admin settings — that scale into Series A instead of needing to be rebuilt. Think of this section as handing Sarah a starter pack she can actually afford to run for six months.

## The guardrails

The budget baseline is about **$200 a month for six to eight active seats**. That number is deliberate: it keeps payroll sane while still covering email, chat, documentation and security basics. Three rules keep it honest.

First, optimise for tools that bundle multiple workflows — email plus drive plus calendar in one subscription beats three separate products. Second, prefer monthly billing until product-market fit is clearer. Long contracts always look cheaper per seat, but they erode optionality if the product pivots — or dies. Third, track the true cost-to-serve: count founders, contractors *and bots*. Automation accounts quietly consume paid licences like hungry ghosts in the billing system, and nobody notices until the seat count is double the headcount.

## The core five

Here is the reference stack, with real monthly prices for a small team:

- **Google Workspace Business Starter — $72.** Email, calendar and Drive with basic admin controls and entry-level data-loss prevention. This is the identity backbone as well as the productivity suite.
- **Slack Pro — $54.** Async conversations, searchable history, and guest channels so partners can join without legal headaches.
- **Notion Plus — $32.** The shared wiki, lightweight project tracking, and investor update templates. This is where standard operating procedures and onboarding playbooks live, so a new hire lands smoothly inside week one.
- **Airtable Team — $20.** The structured layer: a CRM-lite, a partnership pipeline, lightweight inventory tracking — without buying a full Salesforce instance years early.
- **1Password Teams Starter — $24.** Secrets management with a vault per function, onboarding checklists and emergency access.

Total: around $202 a month. Every category a small company genuinely needs — collaboration, knowledge, structured data, security — is covered, and nothing else is.

Each tool comes with a discipline attached. On the communication core, the decision cue is explicit: stay on the Starter and Pro tiers until customers actually demand SSO or message retention beyond 90 days — that demand *is* the upgrade trigger, and it hasn't arrived yet. On the knowledge tools, the discipline is resisting sprawl: build new workflows inside Notion and Airtable before swiping the card for a sixth niche app, and audit the editor list monthly, because many contributors only need free viewer seats. Notion in particular can become a black hole where documentation goes to die unless someone owns its structure. And capture the compliance basics early — GDPR and Australian Privacy Act considerations, where primary data resides, which regions host the backups — because retrofitting those answers is far harder than recording them now.

If someone insists on Microsoft 365 parity, don't argue; make them cost it. Document the total migration lift — identity mapping, data residency shifts, retraining, migration time — before agreeing. What looks like a $20-a-month subscription swap frequently turns out to be a $10K decision in disguise.

## Security hygiene without security spend

Security cannot wait until Series A, but the pre-seed version is cheap. 1Password anchors secrets management; the onboarding checklist lives inside it — who gets which shared vault, when MFA was confirmed, what needs rotating. Hardware security keys via Google Advanced Protection are genuinely excellent, but they're an escalation for after a high-risk trigger, not a day-one purchase. Likewise, skip the dedicated cloud access security broker (CASB): Google Workspace's context-aware access covers the need at this scale for free.

The control that pays for itself fastest is boring: document the joiner/mover/leaver steps in Notion so offboarding becomes a ten-minute ritual. Here's the counterexample. Sarah brought on a contract developer for three months. When the contract ended, there was no checklist, so nobody revoked Drive access — and six months later, during a privacy review, the auditors found an ex-contractor with standing access to customer documents. The remediation conversation was considerably longer than ten minutes.

## Add-ons that must earn their seat

Some additions are worth the money — but only when the pain point is measurable, and every add-on gets a sunset review date so it can be cancelled if the pain evaporates.

- **Calendly Teams** once demo volume passes ten a week and the founders have become scheduling bottlenecks. Before that threshold, you're paying to schedule meetings you aren't having — nobody should spend more time scheduling meetings than being in them.
- **Gusto or Rippling** for contractor payroll when payments outgrow a quarterly manual workflow and invoices arrive monthly.
- **Freshdesk Growth** only when support volume genuinely surpasses shared-inbox discipline and customer deadlines start slipping.

Before adding any of these, map the API and SSO integrations. A tool that doesn't hook into your identity and automation flows creates integration debt — manual syncing, duplicate records, orphaned accounts — that costs more than the subscription.

## The art of "not yet"

Upsell pressure at this stage is relentless, and the correct response is usually a scripted, polite "not yet."

Slack's enterprise team will demo Enterprise Grid with its analytics and compliance exports. Sarah declines until a signed enterprise customer contractually requires those exports. Google will email about storage limits and upgrade tiers; she stays put until storage or legal-hold needs are real, not projected. Vendors will offer "founder discounts" in exchange for 24-month commitments; those get weighed against the cash-runway impact and pivot risk, and they usually lose. When a board advisor insists on a tool, the move is respectful but firm: ask them to map the exact control gap it closes. Sometimes they can — and then you buy it. Usually the conversation ends there.

> A Slack Enterprise rep once led with "99.99% uptime SLA." The startup's Pro plan already met every commitment in every customer contract they'd signed. The correct answer was to keep the cash.

## Customising without losing the plot

The reference stack is a template, not scripture. Swap Google Workspace for Microsoft 365 if your product already depends on Azure AD — the identity gravity is real. Replace Airtable with HubSpot Starter when marketing automation becomes a genuine priority. What matters is that every substitution is documented: why it preserves the $200-a-month guardrail, who owns the new admin tasks, and what changed.

Keep one source of truth listing domains, billing owners and renewal dates. And maintain exit plans for every tool: note the export formats, the backup cadence, and how you'd unwind vendor lock-in before you ever upgrade. A tool you can't leave is a tool that owns you, and vendors price accordingly.

## Try it yourself

The workshop exercise for this topic asks you to do what a founding IT generalist or fractional CTO does in week one: draft your own six-tool stack under $250 a month and justify each choice; identify the specific trigger that would force an upgrade or an extra tool; nominate who owns configuration and governance for each (founder, ops lead, fractional CTO); and present it back with a "stay lean" checklist for your peers to attack. Constructive pushback now is free — the same conversation in a boardroom, after real money has been spent, is not. The question you're rehearsing is the one every board eventually asks: *why this tool, why now, and what happens if it fails?*

The takeaway: start with a deliberate, budget-conscious stack that covers collaboration, knowledge, security and customer touchpoints, and treat every tool purchase as an experiment with a runway impact statement, success criteria and an exit plan. That mindset protects cash, keeps audits boring, and leaves room to scale when product-market fit finally lands.
