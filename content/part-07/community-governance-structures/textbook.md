Much open-source infrastructure begins with one person sharing a useful tool, then acquires users and organisational dependants faster than it acquires maintainers. Governance is how a community decides who may act, who has a vote, how conflict is handled and how money, if there is any, gets spent.

The useful mental model is progressive scaffolding. You don't pour concrete foundations for a garden shed, but you also don't balance a skyscraper on a folding chair. Projects rarely jump from hobby repo to incorporated nonprofit overnight; healthy governance grows in layers. Early contributors document norms alongside code. Mid-stage teams add facilitation rituals. Mature foundations balance budgets, legal protection and public accountability. The test for each new layer is the same: it should lower the load on individuals and widen community agency, not calcify power around whoever got there first. And because contributors span cultures and time zones, governance is people-work — designing decision paths that are legible to newcomers, respectful of marginalised voices, and able to change when circumstances do.

Where a project's community is grounded in its own cultural governance, the structures may look different. Te Hiku Media, examined later in this part, is one such case. Treat what follows as a mainstream open-source toolkit to compare with other systems, not as a universal model.

## Solo stewardship

In the single-maintainer phase, governance is basically the maintainer's judgement plus whatever norms they capture in the README. Decisions are fast, vision is coherent, and the whole thing is one bad month from collapse. The jargon for this is the *bus factor*: how many people can get hit by a bus before the project dies. Aim higher than one.

Solo governance still deserves artefacts. A CONTRIBUTING.md that sets expectations, a regular issue-triage rhythm, and an explicit roadmap (including what will *not* be built) let the community help instead of guess. The risks are predictable: burnout, security fixes that ship unreviewed because there is nobody to review them, and knowledge that lives in one head. The mitigations are equally predictable and routinely skipped. Recruit trusted lieutenants and give them triage or release permissions, even on a trial basis; the people to trust are the ones who already follow the contribution guidelines reliably, communicate edge cases, and respect boundaries. Delegate release tokens. Document the deployment passwords. Schedule real vacations before the 3am "the server is down and only I know the password" stress arrives, because it will.

## Core team collectives

Once three to ten maintainers coordinate, clarity beats charisma. This is the stage for onboarding playbooks that explain code-review expectations, decision timelines and how to escalate conflict — and for rotating roles like review captain, release manager and community moderator so knowledge spreads and nobody becomes the permanent bottleneck.

Mastodon is the instructive example. Before its restructure, founder Eugen Rochko was personally handling code reviews, harassment reports and server bills — no sustainable separation of duties, everything routed through late-night direct messages. The shift created squads for the iOS and Android clients, server administration and community moderation, each with two or three maintainers, plus shared decision logs in public forums.

Two practices carry most of the weight at this stage. The first is *lazy consensus*: a proposal passes unless someone objects within a set timeframe, with a fallback vote if objections can't be resolved. It keeps decisions moving without demanding a meeting for every change. The second is transparency: publish decision logs somewhere public (GitHub Discussions, an open Notion space) so contributors can follow the reasoning rather than reverse-engineer it. Pair both with mentorship cohorts aimed at underrepresented regions, so contributors in Latin America or South Asia know how to surface blockers despite the time zone gap.

## Foundations and fiscal sponsors

When a project becomes critical infrastructure, a foundation can add legal, fiscal and reputational scaffolding. Foundations and fiscal sponsors may hold trademarks, accept funds, contract staff, arrange insurance and support cross-project work. Those services and governance models change, so a project should compare current charters, fees and decision rights before choosing a home.

Expect the paperwork to harden: contributor licence agreements, governance charters and codes of conduct become formal documents rather than wiki pages, and a board plus a technical steering committee keeps roadmap authority with engineers while adding accountability and succession planning. That bureaucracy buys real things — vendor-neutral roadmaps, multi-year funding commitments, and a buffer when commercial or geopolitical interests collide with community priorities, which they eventually do. If all you actually need is a bank account, a fiscal sponsor such as Open Collective Foundation can handle the money without the full institutional apparatus.

## When to formalise — and how it goes wrong

The trigger for adding structure is pain, and the pain has leading indicators: security patches ageing past thirty days, Fortune 100 adopters asking for SLA-like assurances, maintainers skipping parental leave because nobody else can cut a release. A short community health survey surfaces problems before they become departures. Two questions do a lot of work: "How long do security fixes usually take?" and "Do you feel comfortable challenging technical decisions?" Ask them regularly and track the trend. React took three years to move from a Facebook-internal tool to a more open governance model as enterprises demanded neutrality; the hand-off included an RFC process and a cross-company steering group with final authority. Whatever you choose, publish the timelines, the decision criteria and the retrospectives, so stakeholders understand why this structure matches the current risk.

Formalising badly has its own catalogue of failure modes:

- **BDFL burnout.** A founder clings to every decision until they crack. Rotate authority and document delegation triggers before the crisis.
- **Committee paralysis.** Every choice needs consensus from a dozen people, so nothing ships. Set quorum rules, empower working groups, time-box debates.
- **Corporate capture.** One vendor supplies enough funding or staff to bend the roadmap. Diversify revenue, publish conflict-of-interest disclosures, and design board representation and voting rules before dependence becomes control.
- **Fork wars.** Communication breaks down and disagreement turns personal. Invest in mediation channels, transparent decision logs and cultural competency training so disputes stay technical.

Run incident reviews on governance failures the way you would on outages: the point is to learn, not to repeat the cycle with new personnel.

## The playbook, and the people who run it

Good governance is documented well enough that newcomers can self-serve. Concretely: a GOVERNANCE.md describing decision rights, a CODEOWNERS file routing reviews, and an RFC template that shows a proposal's stages. Add onboarding kits with buddy assignments, office hours in multiple languages, and primers on inclusive communication. Track community health like you'd track uptime (median PR review time, the ratio of first-time contributors whose work gets merged, moderation responses within twenty-four hours) and share the dashboards publicly. Match decision frameworks to the decision: consensus-seeking for technical design, majority vote for budget approvals, veto powers reserved for safety issues. Pair transparent funding reports with conflict-resolution channels facilitated by trained moderators or ombudspeople.

All of this is paid work as well as volunteer work, which makes it a career path. Sustainable projects blend maintainers, release engineers, program managers, community stewards, translators, legal counsel and accessibility reviewers, with roughly one community manager per two hundred active contributors — reach that headcount and your "side project" problems have officially become good problems. Map the geography too: leadership shouldn't be North America-only, budgets should include stipends for maintainers in underrepresented regions, and meetings should rotate time zones. People arrive via contributor streaks, Google Summer of Code, corporate OSPO rotations and fellowships centring historically excluded communities. The ones who thrive communicate transparently, mediate cross-cultural tension, and respect Indigenous data sovereignty where projects touch it. From maintainer, the arc runs to technical steering chair, then foundation executive or policy advisor.

> Rule of thumb: if a governance question keeps getting answered in private messages, it isn't governed yet. Write it down where the next person can find it.

The takeaway: governance is not paperwork bolted onto code, it is the mechanism by which a project scales participation without losing its values. Intentional structural choices (paired with documentation, mentorship and cultural humility) are what separate the projects that outlive their founders from the ones that burn them out.
