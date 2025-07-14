---
marp: true
title: Post-mortem Culture
---

# Post-mortem Culture
*Fostering open discussion and avoiding finger-pointing*

---

## Why psychological safety matters
Failure is inevitable in any complex system, and people need room to talk about it honestly. Psychological safety is like a confession booth for code—team members must be confident that admitting mistakes won't lead to punishment. When that trust exists, engineers freely surface skipped checklist steps or confusing run books, giving us real data to fix the process. Without safety we see coverups, finger‑pointing and silence, leaving the root causes buried. Encourage compassion and a growth mindset so everyone learns from the incident rather than hiding from it. In practical terms, that might mean rewarding someone for admitting they skipped a test rather than scolding them, because we can only improve what we acknowledge.

---

## Avoiding finger-pointing
It's tempting to ask "Who broke it?" when an outage happens. Blame might satisfy curiosity, but it shuts down learning. Instead of "Why did you delete the database?" try "What circumstances led to this action?" We look for process gaps, not villains. For example, perhaps a lack of peer review allowed a risky command. Ask "How did our checklist fail us?" rather than "Who skipped it?" Debug the process, not the person—nobody ever fixed a system by making someone cry. A blameless approach uncovers what really went wrong and how we can prevent it next time. Over time this habit reinforces trust, making it easier to catch issues earlier.

---

## Open participation and roles
A productive post-mortem gathers everyone involved: junior devs who pushed code, senior engineers who diagnosed the outage, managers who coordinated the response, even customer support staff who fielded calls. Each role contributes unique context, from console logs to user reports. Encourage quieter voices by explicitly asking for their observations. Over time, a junior engineer might start by sharing a simple timeline and eventually lead discussions as they gain experience. Customer support helps translate user pain, while managers connect action items to budgets and policy. Good facilitators draw out all perspectives so improvements reflect the entire team's experience and career growth becomes part of the process.

---

## Post-mortem agenda and IT processes
Start by reviewing the ServiceNow incident ticket and any linked change requests to set the timeline. Walk through what happened, when alerts fired, who responded, and how the issue was mitigated. A simple agenda might list 09:00 outage detected, 09:10 rollback started, 09:25 service restored, then 09:30 discussion begins. Map each step to ITIL incident-management stages so everyone sees how the process flowed. Next, dig into contributing causes using tools like the five-whys or a fishbone diagram. Document action items as GitHub issues and track improvement with DORA metrics such as MTTR. Close by confirming owners and follow‑up dates so lessons feed back into daily operations and future audits.

---

## Common pitfalls
Blame can spiral into defensiveness, so keep discussions focused on processes. Another trap is the "solution rush"—jumping straight to fixes without understanding why the incident happened. Avoid the hero complex too: one person might try to take all responsibility like a lone Batman, but complex systems need the whole Justice League. It's equally unhelpful when people race to assign blame before the facts are clear. Effective post-mortems look beyond individual mistakes and examine systemic weaknesses. Capture improvements but also analyze how the team communicates under stress. Recognising these pitfalls helps teams build a culture of learning rather than fear and ensures improvements stick.

---

## Practice scenario
Imagine your team's website crashed during a promotion because the database server maxed out connections. In pairs, discuss how you'd run a post‑mortem. Who would attend? What questions would you ask to uncover gaps? How would you phrase them to avoid blame? Maybe the monitoring alerts were buried in Slack while half the team grabbed coffee. After a few minutes, share your approach. Notice how focusing on timeline, monitoring gaps, and documentation leads to constructive solutions, while accusations only derail the conversation. This exercise mirrors what you'd face during your capstone project or a real outage at a streaming service on launch day.

---

## Quick reference phrases
Keep these phrases handy when tensions rise. Start with "Help me understand..." or "What factors contributed to this event?" instead of "Who did it?" If someone's suggestion sounds accusatory, redirect gently: "Let's focus on how the process allowed this step." Ask, "What monitoring or review failed us?" rather than "Why didn't you catch this?" When summarizing, use "We learned that..." or "The system allowed..." to keep the spotlight on the workflow. Invite quiet participants with, "Anything we missed from your side?" These small shifts in language prevent defensiveness and encourage collaboration. Over time, speaking this way becomes second nature and shows leadership potential, especially for those looking to move into senior roles.
---

## Resources
- Post-mortem template: <https://sre.google/workbook/postmortem/> — a step-by-step guide from Google's SRE team that covers timeline, contributing factors, and action items.
- Further reading on psychological safety: *The Fearless Organization* by Amy Edmondson explains why trust improves performance and how to build it.
- ServiceNow problem-management guides show how to record action items and link incidents to change requests.
- DORA Metrics quick reference summarizes deployment frequency, lead time, MTTR, and change failure rate. These numbers help track whether your improvements actually work.
Use these resources as you prepare for your root-cause analysis assignment and the capstone project presentation. They illustrate industry standards and give you ready-made templates for documenting issues and communicating results.

---

## Key takeaway
A blame-free post-mortem culture turns every incident into a learning opportunity. By encouraging psychological safety, inviting all voices, linking to ITIL processes, and tracking improvements with DORA metrics, teams continuously refine both technology and collaboration. Junior staff gain confidence by admitting mistakes without fear, while senior engineers demonstrate leadership by guiding the analysis. Managers can tie action items to business goals and show progress in quarterly reports. These habits feed directly into your upcoming root-cause analysis assignment and the capstone project, where you'll need to present how you handled failure professionally. Failure becomes fuel for progress and a springboard for career growth.
