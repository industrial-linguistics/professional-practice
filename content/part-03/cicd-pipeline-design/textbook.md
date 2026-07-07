In Part 6 you'll meet Sarah, whose fifteen-person marketplace startup ships to customers every week. Early on, "shipping" meant one of her two engineers spending Friday afternoon copying files onto the production server by hand, running a half-remembered sequence of commands, and hoping. Twice the sequence was run out of order. Once a config file was skipped entirely, and the site served a broken checkout page all weekend because nobody thought to look. The problem wasn't carelessness — it was asking humans to be perfectly repeatable, which is the one thing humans are reliably bad at.

Continuous integration and continuous delivery — CI/CD — exist to end exactly that pain. **Continuous integration** means every code change is automatically built and tested the moment it lands, so problems surface in minutes rather than at release time. **Continuous delivery** means the software is kept in a releasable state, with deployment itself automated down to a button-press (or no press at all). Together they form a pipeline: an automated assembly line that carries a change from a developer's commit to running in production, applying the same checks in the same order every single time.

## Why pipelines exist

Manual deployments fail for predictable reasons. They're slow, so teams batch changes up and release rarely — which, as the DORA research showed, makes each release riskier. They depend on one person's memory, so knowledge concentrates in whoever "does the deploys" and evaporates when that person is on leave. And they're invisible: when the release breaks, reconstructing what actually happened means archaeology through shell histories.

Automation reverses each of these. A pipeline makes releases repeatable — the same steps, in the same order, with a log of every run. It makes them fast and cheap, so deploying twice a day costs no more courage than deploying twice a year. It gives quick feedback: a developer who broke the build finds out in ten minutes, while the change is still fresh in their head, instead of three weeks later during integration testing. And it returns engineers' attention to the product. Sarah's startup doesn't employ anyone whose job is "shipping chores" — the pipeline does that, and it doesn't take Fridays off.

This is not just a big-company practice. Small teams arguably benefit most, because they have no spare capacity to absorb a lost weekend. Even non-technical staff feel the difference: instead of asking whether the fix "actually made it to the customer site," anyone can look at the pipeline status and know.

## Four design principles

Well-designed pipelines vary enormously in tooling but share a small set of principles.

- **Automate the whole path.** Build, test and deploy steps all run without manual intervention. Anything a human must remember to do will eventually be forgotten.
- **Build once, deploy many times.** Compile or package the application exactly once, version that artifact, and promote *the same artifact* through test, staging and production. If you rebuild for each environment, you are no longer testing what you ship.
- **Fast feedback first.** Order the pipeline so the quickest checks run earliest. A developer should hear about a failing unit test in minutes, not after an hour-long deployment rehearsal.
- **Gates, not gatekeepers.** Security scans and quality checks are wired into the pipeline itself, so nothing ships without passing them — and nobody has to be the bad guy who blocks a release, because the pipeline does it impartially.

The second principle deserves emphasis because it's the one beginners violate most. The artifact — a container image, a zip of compiled code, a versioned package — is the unit of trust. Once it has passed testing, promoting that exact artifact means production runs the thing you validated, byte for byte.

## From commit to production

A typical pipeline runs as a sequence of stages, each of which either builds confidence in the change or stops it early.

It begins when a developer pushes a **commit** — code and configuration together — to source control. That event triggers the pipeline automatically; nobody has to remember to start it. The **build** stage spins up a clean, disposable environment and produces the versioned artifact there. The clean environment matters: leftover files from a previous build are a classic source of "works in CI, fails in production" mysteries. The **test** stage runs the automated suite — unit tests, integration tests, linting — against the artifact. A **security** stage scans dependencies for known vulnerabilities and enforces policy gates, so basic health checks can never be skipped in the rush to release.

Only then does **deployment** begin, and it proceeds progressively rather than in one leap. The artifact goes first to a staging environment that mirrors production as closely as possible; that's where smoke tests run and where a human approval can be required if the team wants one. When staging looks good, the same artifact is promoted to production. Finally — and this stage is skipped surprisingly often — the pipeline's job continues after release: an **observe** stage watches metrics, logs and alerts for signs that production is degrading. If the signals turn bad, the escape path is simple and fast: roll back to the previous release, which is still sitting there as a known-good artifact. A pipeline without a rehearsed rollback path is a one-way door.

> The whole flow is worth memorising as a chant: commit, build, test, security, deploy, observe — with a return arrow from observe back to the previous release. Every stage either builds confidence or stops the change early. That's the entire design philosophy in one sentence.

## What this looks like in practice

The most accessible way to build one of these today is GitHub Actions, which the next topic covers in detail. The short version: you describe the pipeline in a YAML file that lives in the repository itself, triggered whenever code is pushed. Separate jobs handle building, testing and deploying, which keeps failures easy to localise — when the run goes red, you can see at a glance which stage failed. Common tasks (checking out code, setting up a language runtime, uploading artifacts) use reusable actions shared by the community, and credentials live in encrypted secrets rather than being pasted into scripts. The pipeline gets a locked safe for its keys; your git history stays free of passwords.

## The takeaway

A pipeline is less a piece of tooling than a trust-building machine. Every green run is a small proof that the path from laptop to production works; over hundreds of runs, that proof compounds into a team that deploys on a Tuesday afternoon without holding its breath. Mistakes still happen — pipelines catch many of them before customers notice, and make the rest cheap to reverse.

The practical advice is to invest early. A pipeline built in week one of a project costs an afternoon; retrofitting one onto two years of manual-deployment habits costs a quarter. Sarah's startup got there after the broken-checkout weekend, and the pattern held: faster feedback, fewer surprises, and calmer releases — moved from midnight to mid-morning, because there was no longer any reason to hide them in the quiet hours.
