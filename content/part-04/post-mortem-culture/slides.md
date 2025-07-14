---
marp: true
title: Post-mortem Culture
---

# Post-mortem Culture
*Fostering open discussion and avoiding finger-pointing*

---

## Why psychological safety matters
Failure is inevitable in any complex system, and people need room to talk about it honestly. Psychological safety is like a confession booth for code—team members must be confident that admitting mistakes won't lead to punishment. When that trust exists, engineers freely surface skipped checklist steps or confusing run books, giving us real data to fix the process. Without safety we see coverups, finger‑pointing and silence, leaving the root causes buried. Encourage compassion and a growth mindset so everyone learns from the incident rather than hiding from it.

---

## Avoiding finger-pointing
It's tempting to ask "Who broke it?" when an outage happens. Blame might satisfy curiosity, but it shuts down learning. Instead of "Why did you delete the database?" try "What circumstances led to this action?" We look for process gaps, not villains. For example, perhaps a lack of peer review allowed a risky command. Debug the process, not the person—nobody ever fixed a system by making someone cry. A blameless approach uncovers what really went wrong and how we can prevent it next time.

---

## Open participation and roles
A productive post-mortem gathers everyone involved: junior devs who pushed code, senior engineers who diagnosed the outage, managers who coordinated the response, even customer support staff who fielded calls. Each role contributes unique context, from console logs to user reports. Encourage quieter voices by explicitly asking for their observations. Over time, a junior engineer might start by sharing a simple timeline and eventually lead discussions as they grow. Good facilitators draw out all perspectives so action items reflect the entire team's experience.

---

## Post-mortem agenda and IT processes
Start by reviewing the ServiceNow incident ticket and any linked change requests to set the timeline. Walk through what happened, when alerts fired, who responded, and how the issue was mitigated. Map each step to ITIL incident-management stages so everyone sees how the process flowed. Next, dig into contributing causes using tools like the five‑whys. Document action items as GitHub issues and track improvement with DORA metrics such as MTTR. Close by confirming owners and follow‑up dates so lessons feed back into daily operations.

---

## Common pitfalls
Blame can spiral into defensiveness, so keep discussions focused on processes. Another trap is the "solution rush"—jumping straight to fixes without understanding why the incident happened. Avoid the hero complex too, where one person shoulders all responsibility. Effective post-mortems look beyond individual mistakes and examine systemic weaknesses. Capture improvements but also examine how the team communicates under stress. Recognising these pitfalls helps teams build a culture of learning rather than fear.

---

## Practice scenario
Imagine your team's website crashed during a promotion because the database server maxed out connections. In pairs, discuss how you'd run a post-mortem. Who would attend? What questions would you ask to uncover gaps? How would you phrase them to avoid blame? After a few minutes, share your approach. Notice how focusing on timeline, monitoring gaps, and documentation leads to constructive solutions, while accusations only derail the conversation.

---

## Resources
- Post-mortem template: <https://sre.google/workbook/postmortem/> 
- Further reading on psychological safety: *The Fearless Organization* by Amy Edmondson
- ServiceNow problem-management guides
- DORA Metrics quick reference
Use these resources to refine your practice and connect post-mortems with broader IT workflows.

---

## Key takeaway
A blame-free post-mortem culture turns every incident into a learning opportunity. By encouraging psychological safety, inviting all voices, linking to ITIL processes and tracking improvements with DORA metrics, teams continuously refine both technology and collaboration. Failure becomes fuel for progress.
