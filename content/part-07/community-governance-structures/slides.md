---
marp: true
title: Community Governance Structures in Open Source
---

# Governance Journeys
*How open-source projects evolve from a single maintainer to community institutions*

We’re zooming out from the Te Hiku example now to examine mainstream open-source communities. Projects rarely jump from hobby repo to nonprofit overnight. Healthy governance grows in layers: early contributors document norms alongside code; mid-stage teams add facilitation rituals; mature foundations balance budgets, legal protection and public accountability. Each step should lower individual load and widen community agency rather than calcify power. Remember governance is people-work across cultures and time zones—stewardship means designing decision paths that are legible to newcomers, respectful of marginalised voices and responsive when circumstances change.

---

## Solo stewardship
Single maintainers juggle vision, releases and community tone-setting while also guarding their personal energy. Consider Sindre Sorhus shepherding 1,000+ npm packages solo or Daniel Stenberg steering curl for 25 years—the pace is fast but fragile. Governance here lives in CONTRIBUTING.md checklists, publish-once-a-week issue triage streams and an explicit roadmap so users know what will not be built. Risk: burnout, unreviewed security fixes, bus factor of one. The “bus factor” is shorthand for how many people can get hit by a bus before the project dies—spoiler: aim higher than one. Mitigate by inviting trusted lieutenants for triage, delegating release tokens, documenting deployment passwords and scheduling real vacations before 3am pager stress arrives.

---

## Core team collectives
When three to ten maintainers coordinate, clarity beats charisma. Codify onboarding playbooks that explain code review expectations, decision timelines and how to escalate conflict. Rotate roles—review captain, release manager, community moderator—so knowledge spreads. Before Mastodon restructured, founder Eugen Rochko was handling code reviews, harassment reports and server bills alone. The shift created squads for iOS/Android clients, server administration and community moderation, each with two to three maintainers plus shared decision logs in public forums. Conflict resolution can move from private DMs to a published process using lazy consensus with fallback votes. Pair this with mentorship cohorts for diverse regions so contributors in Latin America or South Asia know how to surface blockers despite time zone gaps.

---

## Foundation-backed projects
Foundations add legal, fiscal and reputational scaffolding once a project becomes critical infrastructure. The Linux Foundation now stewards 750+ projects with a $177M annual budget, funding security audits, conformance programs and marketing. Apache hosts 350+ volunteer-led projects, offering neutral trademarks and a proven meritocratic ladder. Umbrella groups like the CNCF or Software Freedom Conservancy provide insurance, contract staff and cross-project working groups on topics like accessibility or inclusive language. Expect contributor licence agreements, governance charters and codes of conduct to become formal documents rather than wiki pages. In exchange, maintainers gain vendor-neutral roadmaps, multi-year funding commitments and a buffer when commercial or geopolitical interests collide with community priorities.

---

## Deciding when to formalise
Look for leading indicators: unresolved security patches aging past 30 days, Fortune 100 adopters requesting SLA-like assurances, or maintainers skipping parental leave because no one else can ship. Run community health surveys asking, “How long do security fixes usually take?” and “Do you feel comfortable challenging technical decisions?” React, for example, spent three years moving from a Facebook tool to a more open governance model as enterprises demanded neutrality; the hand-off included drafting an RFC process and escalating final authority to a cross-company steering group. Publish timelines, decision criteria and retrospective notes so stakeholders understand why a fiscal sponsor, incorporated nonprofit or foundation membership best matches current risk.

---

## Governance anti-patterns
Watch for failure modes. BDFL burnout happens when a founder clings to every decision; rotate authority and document delegation triggers. Committee paralysis emerges when every choice requires consensus from a dozen people—set quorum rules, empower working groups and time-box debates. Corporate capture looms if a single vendor funds more than ~40% of budget or staff; diversify revenue, publish conflict-of-interest disclosures and ensure board seats reflect community demographics. Fork wars escalate when communication breaks; invest in mediation channels, transparent decision logs and cultural competency training so disagreements stay technical rather than personal. Use incident reviews to turn anti-patterns into learning moments instead of repeating cycles.

---

## Roles, pathways and traits
Sustainable governance blends paid and volunteer roles: maintainers, release engineers, program managers, community stewards, translators, legal counsel and accessibility reviewers. Aim for roughly one community manager per 200 active contributors—if you reach that headcount, your “side project” problems have officially become good problems. Map geographic distribution to avoid North America-only leadership; dedicate budget for stipend-supported maintainers in underrepresented regions and ensure meetings rotate time zones. Pathways include contributor streaks, Google Summer of Code alumni, corporate OSPO rotations and fellowship programs centring historically excluded communities. Effective leaders communicate transparently, mediate cross-cultural tension, and respect Indigenous data sovereignty where relevant. Career arcs can move from maintainer to technical steering chair to foundation executive or policy advisor.

---

## Practical playbook
Document governance so newcomers can self-serve. Create a GOVERNANCE.md describing decision rights, a CODEOWNERS file for reviews, and an RFC template outlining proposal stages. Provide onboarding kits with buddy assignments, office hours in multiple languages and primers on inclusive communication. Track community health metrics—median PR review time, ratio of first-time contributors merged, moderation response within 24 hours—and share dashboards publicly. Adopt decision frameworks that fit your culture: consensus-seeking for technical design, majority vote for budget approvals, and veto powers reserved for safety issues. Pair transparent funding reports with conflict resolution channels facilitated by trained moderators or ombudspeople.

---

## Key takeaway
Intentional governance choices—paired with documentation, mentorship and cultural humility—let projects scale participation without losing their values.

---
