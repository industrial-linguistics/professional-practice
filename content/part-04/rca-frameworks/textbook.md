The previous sections established the culture and the meeting; this one supplies the toolkit. Once a post-mortem reaches stop five on the timeline — root cause — the team needs a method for digging, because unstructured digging goes wrong in predictable ways. People jump to the first plausible explanation. The loudest theory wins. Someone proposes a fix before anyone has established what's broken. A root cause analysis (RCA) framework is a defence against all of that: a step-by-step path from the visible symptom down to the system weakness underneath it.

Why does structure matter so much here? Three reasons. First, a framework moves the discussion from blame to causes almost automatically — when the next step is always "what evidence supports that answer?", there's no room for "well, Dave broke it". Second, it's repeatable: if every incident is analysed the same way, new team members learn the method quickly, and the organisation builds a comparable knowledge base of root causes instead of a pile of one-off essays. Third, the framework guides documentation for free, because the questions you asked and the evidence you gathered *are* the record. Teams that apply consistent RCA methods report dramatic drops in repeat incidents — the commonly cited figure is more than half — and repeat incidents are the most expensive kind, because you've already paid for the lesson once.

Two frameworks cover the overwhelming majority of IT incidents: the five whys and the fishbone diagram.

## The five whys

The five whys is exactly what it sounds like. Start with the problem statement and ask why it happened. Take the answer, and ask why *that* happened. Repeat until you hit something structural. Here's a worked chain from a real-shaped incident:

1. The website went offline. **Why?** The database became unreachable.
2. **Why was the database unreachable?** A deployment script changed the network settings.
3. **Why did the script change them?** The change went out without peer review.
4. **Why was there no review?** The automation pipeline doesn't enforce one.
5. **Why doesn't it?** Because nobody has made approval a mandatory step in the pipeline.

Notice the shape of that descent. The first answer is a symptom. The second is a mechanism. By the fourth and fifth, you're looking at a *process* weakness — and the fix ("add a mandatory approval step to the pipeline") prevents a whole family of future incidents, not just this one. Compare that with stopping at why number two: you'd revert the network settings, close the ticket, and wait for the same pipeline to ship the next unreviewed change.

Two disciplines keep the technique honest. The first: don't stop early. The second and third whys almost always land on something that *feels* like a root cause — a bad script, a wrong config — and the temptation to switch into solution mode right there is strong. Keep going until the answers run out of evidence, not until you run out of patience. The second discipline: every answer must be backed by evidence — a log line, a commit, a timestamp — not speculation. "Probably the cache" is not an answer; it's a hypothesis waiting for a log entry. Document each question-and-answer pair as you go, so anyone reading the post-mortem later can follow the logic and challenge it.

The number five is a guideline, not a law. Some chains bottom out in three whys; some need seven. You've gone deep enough when the answer is something your team can change with a process, tool or test — and, as the previous section warned, if your chain ends at a person, keep digging.

## Fishbone diagrams

The five whys assumes the incident follows a single causal chain. Plenty don't. When an outage has several intertwined contributors — the deploy was risky *and* the monitoring was blind *and* the on-call handover dropped the context — forcing it into one chain of whys either loses causes or turns into an argument about which chain is "the real one". That's the moment to switch to a fishbone diagram (also called an Ishikawa or cause-and-effect diagram).

The diagram looks like a fish skeleton: the problem sits at the head, and major cause categories branch off the spine. The classic categories are People, Process, Technology, Environment, Materials and Methods; in an IT context the Technology branch might carry entries like "network configuration drift", while Process might reveal "no change-management gate for config edits". For each branch, the team brainstorms possible contributing factors and pins them on. Nothing is judged during the brainstorm; the structure itself keeps the ideas organised so nothing gets lost while people are thinking out loud.

The visual layout is the point. As the branches fill in, clusters emerge — six sticky notes on Process and one on Technology tells you where to investigate first. It also makes contributions easy: someone who'd never interrupt a debate will happily add a note to a branch. Draw it on a whiteboard or in a collaboration tool, photograph or export it, and attach it to the post-mortem record, because the diagram doubles as documentation of what the team considered, not just what it concluded.

## Choosing, combining, and knowing the limits

A practical decision rule: **start with the five whys** when the incident looks like a single chain of events — it's fast, needs nothing but a whiteboard, and most incidents genuinely are one chain. **Switch to a fishbone** when the conversation stalls, when new causal branches keep sprouting mid-analysis, or when you know going in that the failure had many hands. And combine them freely: a common pattern is to use the fishbone to map the territory, then run a five-whys descent down each branch that looks load-bearing. The frameworks are lenses, not loyalty oaths.

Whichever you use, capture everything — the questions asked, the evidence gathered, the dead ends, the conclusions. That record becomes part of the post-mortem notes, feeds directly into the ServiceNow problem tickets covered later in this part, and lets the next team understand not just what you concluded but how you got there.

> Know when you're out of your depth. A five-whys session is built for technical and process failures. If the analysis keeps surfacing things like sustained understaffing, a vendor dispute, or decisions made three levels above the team, you've found something a whiteboard exercise can't fix. Escalate to a formal investigation rather than pretending a sticky note will hold it.

The takeaway is the same for both tools: the goal is to get underneath the symptom to the cause that, once fixed, stays fixed. Run the analysis consistently, share the findings beyond the room, and track the action items that fall out of it. Over months, the accumulated records start showing patterns across incidents — the same process gaps recurring in different costumes — and that's when RCA stops being a meeting technique and becomes an improvement engine. It's also a skill with a career attached: the person who can facilitate a crisp root-cause analysis is the person who ends up leading problem management, and there are worse things to be known for than "makes problems stay dead".
