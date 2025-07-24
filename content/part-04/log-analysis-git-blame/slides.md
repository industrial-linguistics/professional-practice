---
marp: true
title: Log Analysis & Git Blame
---

# Log Analysis & Git Blame
*Finding signals without pointing fingers*

---

## Why analyze logs?
- Reveal hidden chains of events
- Validate or disprove hunches quickly
- Spot trends before they become incidents
- Provide data for root cause analysis

---

## Log analysis techniques
- Search and filter with tools like grep or Splunk
- Correlate entries across systems by timestamps
- Tag events with context to aid troubleshooting
- Automate pattern detection for recurring issues

---

## Git blame: friend or foe?
- Shows who last changed each line
- Useful for context on design decisions
- Can feel accusatory if misused
- Focus on understanding, not shaming

---

## Using Git blame constructively
- Pair reviews to discuss code history openly
- Ask why a change was made before judging it
- Capture lessons in commit messages and docs
- Treat blame output as a conversation starter

---

## Example workflow
1. Review logs to trace symptom to code
2. Use blame to see who modified the area
3. Chat with them about reasoning and constraints
4. Update tests and docs based on findings

---

## Key takeaway
- Logs show what happened; blame hints at why
- Combine both to solve issues without finger‑pointing
- Aim for shared understanding and continuous improvement

