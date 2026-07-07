A team once chased an intermittent checkout failure for the better part of a week. Payments would randomly fail for a handful of customers, then behave perfectly through every test anyone ran. Theories multiplied — the network, the payment provider, a bad deploy, cosmic rays — and each theory had a passionate advocate. The argument ended the moment someone lined up three log entries on a single timeline:

```
02:25 INFO  user initiated payment
02:30 WARN  database lock on orders table
02:31 ERROR payment service timeout after 30s
```

A lock on the orders table was starving the payment service until it timed out. Days of hunches, dissolved by three timestamps. That is the promise of log analysis: the system has been writing down what actually happened all along, and the discipline is mostly about going and reading it.

## Logs are where software confesses

A log is the running commentary an application writes about itself: each entry carries a timestamp and a severity level — DEBUG for developer chatter, INFO for normal events, WARN for things that look off, ERROR for things that definitely are. One engineer in this course's running cast describes logs as the place your application goes to confess its sins, and the confession metaphor is apt: the entries are honest, unflattering, and only useful if someone listens.

DevOps engineers, SREs and level-2/3 support staff live in logs daily, and for the same reason detectives like security footage: logs capture sequences that summary metrics miss. A dashboard tells you memory usage was high at 02:00; the log tells you it had been creeping up for six hours before the crash, which is the difference between "the service died" and "we have a leak, and here's roughly where". During a root cause analysis, log evidence is what turns the five-whys chain from speculation into fact — and, just as valuably, what stops the finger-pointing, because nobody argues with a timestamp.

One professional obligation before we go further: logs frequently contain personal data — user IDs, email addresses, sometimes worse. Your organisation will have retention and privacy rules about how long logs are kept and who may see them. Follow them. Pasting a raw production log into a public Slack channel can be a privacy breach, not just bad manners.

## Techniques that scale with the system

For a small application, the command line is enough. Something like:

```
grep "ERROR.*timeout" app.log | tail -20
```

fetches the last twenty timeout errors, and for a single service on a single server that may be all the tooling you ever need. But the approach stops scaling quickly — nobody greps a 10 GB file across twelve microservices with any joy — and that's where log aggregators come in. The Elastic Stack (free, beloved of hobby projects and plenty of production ones) and Splunk (paid, with enterprise support) collect logs from every service via lightweight agents into central, searchable storage, enforce retention rules automatically, and integrate with ServiceNow or Jira so an alarming pattern can become a ticket without anyone retyping it.

Two practices make aggregated logs dramatically more useful. The first is structure: logs written as JSON with named fields can be queried reliably, while free-text logs demand increasingly desperate regular expressions. The second is request IDs — a unique tag attached to each incoming request and passed along to every downstream service it touches. With request IDs (and their grown-up sibling, distributed tracing), you can follow one user's request from the front end through each downstream service and see exactly where it went wrong. Dashboards complete the picture: a rising count of WARN entries often flags memory pressure or resource exhaustion before anything actually breaks, and a well-built graph will show whether a surge in Service A cascaded into failures across Services B through F.

A word of restraint: logging isn't free. DEBUG-level logging in production slows applications and devours storage, so keep DEBUG output short-lived and be deliberate about what's worth writing down.

## git blame: the worst-named tool in the industry

Once the logs have traced a symptom to a region of code, a different question arises: how did the code get that way? Git answers with `git blame`, which annotates every line of a file with the commit, author and date that last changed it. It's the ultimate "it wasn't me" detector, and its name is a standing invitation to use it badly.

Here is the trap. The last person to touch a line is very often not its author in any meaningful sense — they may have been fixing someone else's bug, reformatting the file, or patching production at 11 pm under a deadline against requirements that changed the following month. Treat blame output like fingerprints at a crime scene: genuinely useful evidence, nowhere near the full story. Before drawing any conclusion, combine it with the commit message, the linked issue history, and — this is the step that separates professionals from prosecutors — a conversation with the person.

Two flags make the evidence itself more honest. `-w` ignores whitespace-only changes, so the person who re-indented the file doesn't inherit its bugs; `-C` tracks code moved between files, so the person who relocated a function isn't credited with writing it. A typical constructive invocation looks like `git blame src/user-service.py -L 45,55 -w` — narrow line range, whitespace ignored — followed by a message to the author asking what constraints they were working under. The usual answer is illuminating: a hotfix, an outdated spec, a review that never happened. Capture what you learn in commit messages or design docs so the next investigator doesn't repeat the dig.

And know when not to run it at all. If tempers are hot in the middle of an incident, blame output will be read as an indictment no matter how it's offered — wait. If the goal is a refactor, the history rarely matters. And if a blame trail keeps exposing systemic problems — unrealistic deadlines, changes shipping without review — that finding belongs in the team retrospective, raised as a process issue, not in a public channel with a name attached.

> A war story worth keeping: a team once spent three hours blaming the database for an outage before anyone noticed a typo in a config file. The log line pointing at the config had been there the whole time; nobody had actually read it, because everyone already "knew" what was wrong. Rule of thumb: gather the evidence before you form the theory, because the theory will happily bend the evidence to fit.

## A worked investigation

Here's how the pieces fit together in practice. A spike of `ERROR: database connection timeout` entries appears. First, logs: the network metrics look normal, so latency is ruled out and attention turns to the application side. Second, history: the commit log shows a recent change to connection pooling. Third, blame: run on that file, it identifies who altered the pool size. Fourth — and this is the step that defines the culture — a conversation, not an accusation. It turns out the change fixed a different outage months earlier; the pool was shrunk to stop the database being overwhelmed, and today's traffic has outgrown the compromise. That reframes everything: this isn't a blunder to correct but a trade-off to renegotiate. Together, you and the original author test new settings, adjust the pool, update the documentation, and record the whole thread in the incident ticket. The logs get stored according to retention policy, so when a future team meets the next incarnation of this problem, the history is waiting for them.

Notice what each tool contributed: the logs established *what happened and when*; blame hinted at *why the code was the way it was*; the conversation supplied the context neither tool could. That combined narrative — technical symptoms plus human decisions — is exactly what a good post-mortem needs, and assembling it quickly is what shortens your mean time to recovery.

The takeaway is a professional stance as much as a technique. Logs and `git blame` are instruments for learning: used with curiosity, they shorten incidents, expose recurring weaknesses, and build the kind of team where admitting a mistake is safe because everyone has watched mistakes lead to better systems instead of public shamings. Used as weapons, they produce silence, and silence is how the same outage happens twice. You now know how to read the confession; make sure your team never regrets making one.
