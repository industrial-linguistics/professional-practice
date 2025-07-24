---
marp: true
title: Log Analysis & Git Blame
---

# Log Analysis & Git Blame
*Finding signals without pointing fingers*

---

## Why analyze logs?
Logs capture the raw truth of how software behaves. Each entry contains a timestamp and a log level such as DEBUG, INFO, WARN or ERROR. By lining these up you can spot patterns that metrics alone miss. Imagine debugging a checkout process that fails randomly. You might see `02:25 INFO user initiated payment`, `02:30 WARN database lock on orders table` and finally `02:31 ERROR payment service timeout after 30s`. The timeline reveals that the database lock triggered the timeout. Analyzing logs validates hunches, uncovers trends like memory spikes before incidents occur and provides evidence for root cause analysis. Remember that logs may hold personal data, so follow your organisation's retention and privacy rules when storing or sharing them.

---

## Log analysis techniques
Start with simple searches using `grep` or built‑in filters to spot recurring errors. As your stack grows, aggregators like the Elastic Stack or Splunk let you correlate events across dozens of microservices. Structured logs with consistent fields make queries reliable, while unstructured text requires regex tricks. Many teams tag each log line with request IDs so they can trace a single transaction end to end. Visual tools reveal spikes in WARN or ERROR levels and show whether a memory surge in Service A triggered cascading failures in Services B through F. Log aggregation also supports retention policies: you keep detailed DEBUG logs for a short period but retain ERROR summaries longer for compliance.

---

## Git blame: friend or foe?
`git blame` displays who last modified each line of code. It's powerful context for understanding design choices but can feel accusatory if used carelessly. People often worry that blame will be used to point fingers instead of improving the code. The reality is that the last editor may have been fixing someone else's bug or operating under tight deadlines. Treat blame information like fingerprints at a crime scene—useful evidence but not the full story. Combine it with commit messages, issue history and a conversation with the author before drawing conclusions. And sometimes it's best not to run blame at all when emotions are high or the goal is simply to refactor.

---

## Using Git blame constructively
When you do use blame, pair it with open dialogue. Suppose a function crashes on null inputs and you run `git blame src/user-service.py -L 45,55 -w`. Reach out to the contributor and ask what constraints they faced when writing that code. Maybe they were patching a production bug or following outdated requirements. Capture the lessons learned in commit messages or design docs so others won't repeat the mistake. Remember to respect privacy; if a blame trail uncovers systemic issues like unrealistic deadlines or missing reviews, escalate through your team's retrospective process rather than confronting individuals in public channels.

---

## Example workflow
Begin by reviewing logs to trace a symptom back to the code. Imagine a spike of `ERROR: database connection timeout` entries. After confirming that network latency wasn't the culprit, you check the commit history and see a recent change to connection pooling. Running `git blame` on that file reveals who altered the pool size. You chat with them to understand the reasoning and learn that the change fixed another outage months ago. Together you run new tests, adjust the pool size and update documentation. Finally, record the incident in your ticketing system and ensure the logs are stored according to retention policy so future teams can learn from them.

---

## Key takeaway
Logs show what happened and when, while Git blame hints at why. Combine them to build a narrative that explains both the technical symptoms and the human decisions behind them. Use tools like Splunk or the "-C" flag in git blame responsibly: keep sensitive data private and open a dialogue before drawing conclusions. Over time these practices shorten incident response, reveal recurring issues, and demonstrate progress with metrics like MTTR. Most importantly, they encourage a culture where admitting mistakes leads to stronger systems rather than shame. Treat these tools as instruments for learning and growth, not as weapons for calling people out.
