---
marp: true
title: Communicating Outcomes
---

# Communicating Outcomes
*Tracking action items for accountability*

---

## Why share outcomes?
- Build trust by showing incidents are taken seriously and systematically addressed
- Prevent repeats across teams by openly sharing root causes and fixes
- Demonstrate accountability with owners and deadlines for each action item
- Create an organizational memory of lessons learned for future reference
- Meet compliance requirements such as ISO 27001 follow-up evidence
- **Example:** After a database outage affecting 10k users, a summary email helped other teams spot similar risks in their own systems
- Make the business impact clear so leaders can prioritise investments
- Candid details build credibility even if everything isn't perfect

---

## Communication timing and audiences
- Send an initial summary within 24 hours to leadership and directly impacted teams
- Follow up weekly until all high-priority actions are closed
- Tailor messaging: leadership wants business impact and timelines, technical staff need root cause details, customers need reassurance and next steps
- Use dashboards or status pages for company-wide updates
- Keep a single thread in Slack or Teams for ongoing questions
- Reserve sensitive technical notes for internal docs and keep public messages short
- Set expectations early by outlining major milestones and when each update will arrive
- Invite questions so you can address them in subsequent follow-ups

---

## Track each action item
- Assign one owner and a clear due date so nothing gets lost
- Capture items in a ticketing system like ServiceNow or GitHub
- **Example ticket:** `[OUT-123] Update database configuration – Owner: Lee, Due: 2025‑08‑01`
- Review progress in stand-ups and team meetings
- Escalate to management when an item misses its deadline or stalls for a week
- Write specific descriptions like "upgrade library X to version Y" rather than vague phrases
- Link to relevant documentation or runbooks for more context
- Check off each action when complete so progress stays visible
- When new tasks emerge during remediation, create follow-up tickets right away

---

## Template examples
- **Email:** "Team, our post‑mortem identified three fixes. See the attached doc for details. Jane owns the first, due Friday."
- **Slack:** "Heads up: database patch rolling out tonight. Track progress in #incident‑123."
- **Dashboard update:** Add a section summarizing closed and open items from recent incidents
- Short, consistent templates make it easy for anyone to share updates without reinventing the wheel
- A one-page summary template captures the incident, root cause, owners and due dates
- Use a Slack snippet like `/incident update` to auto-fill your status channel
- Maintain a wiki page with a table of updates for longer-running work
- A simple table of item, owner, due date and status makes progress clear at a glance
- Using the same structure across teams reduces confusion and speeds up handoffs

---

## Close the loop
- Post updates in the original ticket or chat thread so everyone sees progress
- **Example update:** "Patch deployed to production at 22:00 UTC. Monitoring shows no errors."
- Note completed actions directly in the tracking system to keep records tidy
- Revisit outstanding items at the next post-mortem and highlight improvements using metrics
- When tasks drag on, call out the delay and reassign resources if needed
- Celebrate completions with a quick thank-you to keep momentum going
- Final message example: "Thanks for everyone's help—OUT-123 and OUT-124 are now closed."
- Schedule a quick check-in a month later to confirm the fixes are holding
- If open items stall, remind the team why they matter and escalate to leadership

---

## Metrics and success measures
- Track completion rate of action items over time to show improvement
- Monitor recurrence of similar incidents to gauge effectiveness of fixes
- Report average time from incident to final follow‑up
- Display these stats on team dashboards or monthly review meetings
- Measuring progress keeps everyone honest and celebrates wins when numbers trend in the right direction
- Compare current metrics with past baselines to prove communication efforts are paying off
- Include graphs of MTTR trends to highlight faster recovery
- Track how many updates were sent for each incident to gauge responsiveness
- Share success stories when metrics improve to motivate the team

---

## Key takeaway
Clear, timely communication and thorough follow‑up turn insights into real progress and demonstrate professionalism.
