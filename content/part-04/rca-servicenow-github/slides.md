---
marp: true
title: Integrating RCA Records with ServiceNow and GitHub
---

# RCA Records in ServiceNow & GitHub
*Because "we'll remember to fix that" are famous last words*

---

## Why link RCA to problem tickets?
- Turns scattered post‑mortem notes into an actionable backlog
- Tracks the root cause alongside related incidents and changes
- Keeps an audit trail for compliance reviews
- Helps prioritize improvements during planning sessions
- Ensures lessons learned drive measurable fixes rather than fading away
- Questions to ask: Where do we store past RCAs? Who checks them?

---

## ServiceNow problem records
- ServiceNow is a ticketing system widely used in IT operations
- A problem record summarizes the investigation after an incident
- Include a timeline, contributing factors and workarounds
- Link any relevant incident tickets, change requests and knowledge articles
- Assign an owner and set a target resolution date
- Example: "Checkout failure during Black Friday—DB connection pool exhausted; manual phone orders used as workaround"
- Good descriptions help managers see impact and approve resources

---

## GitHub issue references
- GitHub issues track code work that addresses the problem
- Title should mention the ServiceNow number for easy searching
- Example: "Increase DB connection pool size - PRB0001234"
- Describe the fix in business terms so non-developers understand
- Link commits and pull requests back to the issue
- Close the issue only after the fix is in production and verified
- Questions to ask: Does this change need a code review? Who signs off?

---

## Putting it all together
- Start with a shared post‑mortem document capturing logs and timelines
- Within 24 hours, create a ServiceNow problem ticket summarizing the findings
- Open a GitHub issue for each improvement item and link it back
- Review progress weekly during improvement meetings
- Update the ServiceNow ticket when the GitHub issue closes
- Example timeline: incident 2:15 PM, outage 2:45 PM, resolved 4:30 PM; action item implemented two days later

---

## Common pitfalls
- Forgetting to link ServiceNow and GitHub so records drift apart
- Vague problem statements that hide the real business impact
- Issues left open for months with no clear owner
- Urgent hotfixes applied outside the process and never documented
- Reviewing status only once, so lessons fade quickly

---

## Key takeaway
- Integrated records keep teams aligned and accountable
- ServiceNow captures the process while GitHub tracks the code
- Clear links turn each incident into documented learning rather than another "we should totally fix that someday" conversation
