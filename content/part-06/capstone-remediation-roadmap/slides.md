---
marp: true
title: Capstone: Remediation Roadmap
---

# Capstone: Remediation Roadmap
*Take-home planning and reflection prompts*

Note:
- 30 seconds. Welcome learners and flag that this session produces a tangible plan they can reuse.

---

## Why a remediation roadmap?
Without a roadmap, your security findings become that gym membership you bought in January—great intentions, zero follow-through. We translate red-team evidence into funded, sequenced improvements that Sarah can show to investors, auditors and her customer success team without scrambling. The document also gives engineering, ops, GTM and finance a common script so nobody wonders who is fixing the production database exposure or how much headcount is needed. Finally, the roadmap anchors reflection: we capture what surprised us, which assumptions fell over, and where we must keep experimenting so the capstone evolves into an ongoing learning habit rather than a once-a-year panic drill.

Note:
- 2 minutes. Emphasise the “why” and share the gym membership line with a smile to break the ice.

---

## Inputs to capture before planning
Start by consolidating everything we already surfaced: top risks across people, process, technology and vendors; severity, likelihood and blast-radius notes from each tabletop; and the pod’s maturity scores. Add the qualitative color too—quotes from the red team, customer anecdotes, or the moment we realised customer support can reach production data with no logging. Log open questions for MSPs, SOC analysts, legal counsel and finance so that diligence follow-ups have named owners. The more complete this input pack, the less time we spend reinventing context when an executive, auditor or potential acquirer asks for proof that we understand our own gaps.

Note:
- 2 minutes. Encourage teams to screenshot findings and paste links rather than retype everything.

---

## Structuring the backlog
We organise the backlog into three swimlanes. **Stabilise** handles the immediate fires—enable MFA for all admin accounts, patch the critical vulnerabilities from the last 30 days, refresh the on-call contact tree. **Reinforce** locks in better habits: implement automated backup testing, stand up a vendor security review checklist, publish post-mortem templates. **Scale** funds the longer-term bets such as deploying a SIEM, negotiating enterprise support with key SaaS vendors, or rolling out company-wide security awareness training. Each item lists an owner, collaborators, budget cues and a success metric (e.g., “Security Lead, partner with Support Manager, target zero unlogged prod access within 45 days”). Sarah can now see how actions align to product delivery, customer support and compliance obligations.

Note:
- 3 minutes. Ask teams to label each backlog item before moving on.

---

## Prioritisation & due diligence prompts
Prioritisation blends rigor and pragmatism. Score each backlog item for business impact, regulatory exposure, customer promise, effort and sequencing constraints. When in doubt, ask, “What would our most risk-averse board member or biggest customer interrogate?” That lens often bumps data-handling controls higher than a cool automation experiment. Capture due diligence prompts alongside the work: “How do we verify MSP patch compliance?” “Where do we store customer PII backups?” “What’s the cost of SOC coverage after hours?” If everything is “critical,” nothing is—your startup can’t fix all the things in week one, no matter how caffeinated engineering feels. We name dependencies early so finance, legal and platform teams have time to respond.

Note:
- 3 minutes. Invite pods to draft one diligence question per backlog item.

---

## 30-60-90 action horizon
Time-boxing keeps the plan believable. In the first 30 days we chase the “keep Sarah out of the headlines” tasks—close MFA gaps, restrict prod database access, document emergency contacts, and send investor-ready summaries. Days 31-60 focus on process: refresh runbooks, formalise tabletop cadences, stand up a due diligence tracker in ServiceNow or Airtable. Days 61-90 fund the strategic moves like piloting a SIEM, renegotiating SOC contracts or aligning resilience OKRs. Each action notes prerequisites—purchase orders, legal reviews, headcount approvals—so delays are transparent. This horizon also feeds the budget conversation: executives see when cash leaves the bank and what risk drops as a result.

Note:
- 3 minutes. Highlight that teams can reframe to 15-30-45 if that cadence matches their sprint rhythm.

---

## Ownership, accountability & communication
Assign every item an executive sponsor, a delivery lead and a supporting squad. We document where progress will be reviewed—Monday ops stand-up, monthly security council, quarterly board pack—and which artefacts count as “done” (tickets, policy diffs, evidence screenshots). Customer-facing voices stay in the loop so rollout comms land well. And yes, assigning ownership without accountability is like making someone captain of a ship but not giving them the steering wheel. We also script how Sarah will brief investors or clients: short Loom updates, dashboard snapshots, and proactive notes about trade-offs to keep trust high.

Note:
- 3 minutes. Encourage teams to rehearse their investor one-liner about progress.

---

## Risk communication playbook
Security storytelling matters. Start with an executive summary that translates tech jargon into customer impact, cost exposure and compliance obligations. Use a simple heat-map or RAG dashboard to highlight where Sarah’s team is burning risk down. Pair every finding with a proposed mitigation, owner and estimated cost so leaders are choosing between options, not drowning in problems. Have a one-page leave-behind for investors with the three biggest risks, financial implications, and the date they will hear the next update. Rehearse how you will answer, “Are we safe today?”—the honest response anchors on trend lines (“We eliminated unlogged prod access this month; phishing resilience is now our top risk”).

Note:
- 3 minutes. Suggest teams screenshot dashboards or draft them in FigJam/Canva quickly.

---

## Change management tactics
Even the best roadmap fails without hearts and minds. Start by mapping stakeholders—engineering, support, sales, finance, MSP partners—and their likely worries. Prepare tailored messaging: support hears how tighter access protects customers, finance sees the cost avoidance, engineers get clarity on workload. Anticipate resistance (“Do we really need another approval step?”) and decide where to flex. Use lightweight enablement like five-minute Loom walkthroughs, office hours and quickstart guides. Pair policy changes with training commitments so people feel set up to succeed. Celebrate early adopters publicly, and give laggards a path to catch up without shame. The goal is adoption, not compliance theater.

Note:
- 3 minutes. Prompt pods to script one message per stakeholder group.

---

## Measurement, reporting & celebration
What gets measured gets maintained. Stand up a lightweight dashboard—Airtable, Notion, ServiceNow or even Google Sheets—that tracks status, burndown of risk scores, spend versus budget, and outstanding dependencies. Define leading indicators (MFA enrolment rate, time-to-close vendor tickets) and lagging ones (reduction in unlogged prod access, MTTR). Schedule cadences: weekly squad syncs, monthly executive readouts, quarterly retros. Close the loop by documenting lessons learned and celebrating wins—ring a Slack bell when Sarah’s team retires a high-risk finding or nails a due diligence interview. When setbacks happen, log what we learned and the next experiment so momentum is never lost.

Note:
- 3 minutes. Show example dashboards if available; otherwise describe metrics in detail.

---

## Reflection prompts to close the capstone
End with curiosity. What surprised us about our resilience posture compared with expectations? Which assumptions about vendors, tooling or people broke under pressure, and what did that teach us about the startup’s culture? How will we maintain psychological safety while still holding people accountable? Where do we need leadership support—budget, headcount, MSP upgrades—to keep the roadmap alive? Encourage pods to capture these reflections alongside their backlog; investors and auditors love to see that learning loop, and it keeps the team honest about progress.

Note:
- 2 minutes. Invite a quick round-robin share from each pod.

---

## Workshop & take-home assignment
Before leaving the room, each pod drafts a sample roadmap for Sarah’s startup using the provided template. Document the context, top five actions, success measures and next review date. Add a mini risk register entry for at least one item, plus an executive brief paragraph that could drop into a board deck tomorrow. Schedule 5-minute readouts for the next session—one risk retired, one still open, one open question for an MSP or legal partner. Homework: line up follow-up interviews, update the due diligence tracker, and bring the lessons to your next investor update or client renewal call.

Note:
- 3 minutes setup + 15-minute working time. Circulate to coach teams while they build their draft.

---

## Templates & companion resources
You have access to a remediation backlog spreadsheet, a one-page executive summary template, and a risk register pulled from earlier capstone materials. Reuse the tabletop maturity rubric to baseline progress after 30 and 90 days. For tooling inspiration, check ServiceNow for incident tracking, Jira or Linear for task execution, and Okta for MFA rollout tracking. Link your roadmap to the earlier vendor diligence checklist so Sarah can answer investor questions with confidence. Bookmark the communication plan template from Part 5 to keep cadence rituals aligned.

Note:
- 2 minutes. Show where templates live in the shared drive or LMS.

---

## Key takeaway
A remediation roadmap turns the capstone from a one-off adrenaline rush into a continuous improvement flywheel. By sequencing actions, naming owners, capturing diligence questions and communicating clearly, teams leave ready to advocate for investment and prove progress with evidence. The roadmap also sparks better habits—celebrating wins, learning from setbacks, and keeping stakeholders looped in—so Sarah’s company (and yours) keeps resilience front of mind long after the workshop ends.

Note:
- 1 minute. Close with a call-to-action: publish the roadmap draft within 48 hours.

---
