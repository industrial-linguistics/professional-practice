At Meridian Insurance — the firm from the DORA metrics topic — a contractor once spent six weeks building a quoting feature on his own branch. The work was good. The merge was not. In the six weeks his branch had been drifting away from the main line, four other teams had reshaped the modules he depended on. Reconciling the two histories took nine days, broke two things the tests didn't cover, and produced the sentence every engineering manager dreads: "it worked before the merge."

How a team uses branches sounds like a low-stakes tooling preference. It isn't. Branching strategy determines how quickly changes integrate with everyone else's work, and therefore how much merge pain you accumulate — which makes it one of the strongest levers on the DORA metrics you've just met. There are two poles to the debate, and most real teams live somewhere between them.

## Trunk-based development

In trunk-based development, everyone commits to a single shared main line — the trunk — in small, frequent increments, at least daily. There are no long-lived personal branches accumulating private history; integration happens continuously, which is what "continuous integration" originally meant before it became the name of a build server.

The immediate objection is obvious: what about half-finished work? You can't ship half a quoting feature to production. The trunk-based answer is the **feature toggle** (or feature flag): the incomplete code merges into trunk and deploys with everything else, but sits behind a switch that keeps it invisible to users until it's ready. The code integrates early; the *feature* launches when you choose. Toggles bring their own housekeeping — old flags need removing, and testing must cover both switch positions — but they decouple two things that were never naturally coupled: integrating code and releasing features.

What trunk-based development buys you is the near-elimination of merge conflicts. When everyone integrates daily, nobody's view of the codebase is more than a day stale, so collisions are small and caught while both authors still remember what they wrote. What it demands is discipline: a solid automated test suite (because trunk must stay releasable), the skill of slicing features into small safe increments, and a team that treats a broken build as everyone's top priority.

## Feature branching

Feature branching is the strategy most students meet first, because it's the default shape of working with GitHub. Each piece of work gets its own isolated branch; when it's finished, a pull request proposes the merge back, a colleague reviews the diff, the automated checks run, and the branch lands.

Isolation is genuinely valuable. You can experiment without destabilising anyone, park work when priorities shift, and — most importantly — the pull request gives code review a natural home. The review conversation attached to a PR is often the best design documentation a change ever gets, and for open source projects, where contributors are strangers, this model is essentially mandatory.

The cost is drift. Every day a branch lives apart from trunk, two things grow silently: the branch's ignorance of what has changed underneath it, and trunk's ignorance of what the branch is about to do to it. Merge conflicts are the visible symptom; the invisible one is worse — two branches that don't textually conflict but break each other's assumptions, sailing through the merge and failing in production. Integration pain isn't eliminated by branching; it's deferred, and it compounds while it waits. Meridian's nine-day merge wasn't bad luck. It was six weeks of deferred integration, paid back with interest.

## Choosing — and blending

Framed as a binary, the choice looks hard: trunk-based development maximises flow and feedback; feature branches give you isolation and reviewable units of work. In practice, almost every effective team blends the two, and the blend is less a compromise than a synthesis.

The recipe: keep branches, but keep them *short-lived*. A branch carries one small piece of work, lives a day or two, and merges via a pull request that a colleague can actually review in ten minutes — because it's a two-hundred-line diff, not a six-week epic. Larger features are sliced into a sequence of such branches, integrated one at a time behind a toggle if needed. You get the review culture and safety of pull requests with integration frequency close enough to trunk-based to keep merges trivial.

The evidence backs the blend. The *Accelerate* research found that teams with branches lasting less than about a day, and only a handful active at once, showed higher delivery performance — while long-lived branches were associated with slower, less stable delivery. The finding, notably, is about branch *lifetime*, not about whether branches exist at all.

> A useful team norm: if a branch is about to see its third sunrise, something is wrong — slice the work smaller, or merge what's safe behind a toggle. Branch age is one of the cheapest early-warning metrics a team can watch.

It's the mirror image of the DORA logic from earlier in this part: many small deployments beat one big deployment, and many small merges beat one big merge, for the same reason. Small changes are easy to understand, easy to review, easy to test and easy to reverse.

## The takeaway

Don't get religious about the label; get disciplined about the interval. Whether your team calls its process trunk-based or feature branching matters far less than how long changes stay isolated from the main line. Keep merges small and frequent, keep branches measured in hours or days rather than weeks, use toggles to separate integration from release, and reserve long-lived branches for the rare cases that truly need them. When you join a team, you can read its health in its repository: dozens of stale branches and dreaded "merge parties" mean deferred integration debt; a busy trunk fed by short-lived branches means the debt is being paid daily, in small instalments, while it's still cheap.
