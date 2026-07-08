# Current Status

Last checked: 2026-07-08.

## Executive Summary

The content phase is essentially finished. The bottleneck has moved from writing to packaging, assessment, delivery, and commercial validation.

Parts 1-7 contain 81 complete learner topics with slides, narratives, and authored `textbook.md` files. The narrative mismatch audit currently reports 81 matched topics and 0 mismatched topics. The build pipeline has enough working pieces to generate the learner site, textbook, run sheets, and media assets.

What is not yet finished is the product layer: audio coverage is sparse, video coverage is minimal, Part 8 is still a stub, quiz content is not deployed as a learner-facing engine, there is no SCORM package, there is no completion/certificate layer, and there is no explicit licence or terms statement.

The main commercial implication is simple: the course is no longer blocked on more course writing. It is blocked on making a buyer-ready package.

## Verified Repo Snapshot

- Parts 1-7 have 81 topic folders with `slides.html`.
- Parts 1-7 have 81 topic folders with `textbook.md`.
- Topic counts by part:
  - Part 1: 7 topics, plus a separate `quiz/` folder.
  - Part 2: 6 topics.
  - Part 3: 6 topics.
  - Part 4: 11 topics.
  - Part 5: 23 topics.
  - Part 6: 23 topics.
  - Part 7: 5 topics.
- Part 8 currently has `outline.md`, `practice-artifact.md`, and `textbook-intro.md`, but no topic set.
- The narrative mismatch audit reports:
  - Topics: 81.
  - Mismatched topics: 0.
  - Matched topics: 81.
- There are 14 audio files in `content/`.
- There is one MP4: `content/part-01/overview/final.mp4`.
- Quiz source exists for Parts 1-7, but it is not yet a deployed course assessment layer.
- No SCORM package or `imsmanifest.xml` is present under `output/`.
- No top-level `LICENSE` or `TERMS` file is present.

## Product Finding

The repo's centre of gravity still pulls toward more writing and polish. That is now a risk. More Part 7 topics, more Part 8 prose, and more wording passes may improve the content, but they do not answer whether anyone can buy, run, assess, or procure the course.

The commercialisation plan already named the right path:

1. A polished landing page.
2. Three sample lessons.
3. One SCORM pilot.
4. One pilot cohort.
5. Direct outreach and buyer feedback.

That should become the working priority.

## Assessment Is The Sellable Layer

Institutions and graduate programs are unlikely to buy "content" alone. They buy assessment, reporting, reduced instructor effort, and confidence that learners can demonstrate workplace judgement.

The existing quiz banks are useful raw material, but they are mostly source markdown with inline answers. The next step is to turn assessment into a first-class generated artefact:

- Learner-visible quizzes.
- Scenario interactions.
- Scoring.
- Feedback.
- Completion status.
- LMS reporting.
- Downloadable or exportable artefacts for human-marked work.

## SCORM Assessment Ideas

Most SCORM assessment should be scenario-driven rather than vocabulary-driven. Multiple-choice recall can stay, but it should not dominate.

| Part | Good SCORM Question Types |
| --- | --- |
| 1. ITIL Foundations | Classify incoming records as incident, request, problem, or change; choose priority; assign L1/L2/L3/incident commander; draft the first customer update from multiple options. |
| 2. ITIL Deep Dive | Match SLA clauses to OLAs and KPIs; calculate downtime from availability targets; approve, defer, or reject change requests based on risk, rollback, affected CIs, and business timing. |
| 3. DevOps/DORA | Calculate DORA metrics from pipeline events; identify the weak stage in a CI/CD run; decide what to automate next after a failed release. |
| 4. RCA | Reconstruct an incident timeline; convert blameful wording into system-focused causes; choose corrective action versus Kaizen improvement; rank action items. |
| 5. CRM/Vendor | Map buying committee roles; spot sales promises that create operational obligations; select vendor risk mitigations; connect CRM stage changes to ITIL handoffs. |
| 6. Small-Biz IT | Prioritise a 30/60/90 roadmap under budget; identify shadow IT and data exposure risks; choose minimum viable controls for identity, devices, backup, support, vendor risk, and data location. |
| 7. OSS/Data Sovereignty | Choose licence or access tier; identify who has authority over reuse; distinguish CARE/FAIR tensions; reject unsafe "just make it open" answers. |
| 8. Capstone | Read a proposal extract and identify missing evidence: support model, change process, data authority, year-three cost, vendor assumptions, and panel-defence readiness. |

SCORM can report coarse score and completion status. The simulators should keep richer internal scoring than SCORM 1.2 can expose, so a later xAPI or cmi5 upgrade does not require redesigning the learning logic.

## Tool Ideas

### 1. Incident Triage Simulator

Highest-value first tool.

Students process five tickets, classify them, set priority, assign ownership, and write or select customer-facing updates. This maps directly to the Part 1 practice artefact and A1 role-mapping assessment.

This should be the one simulator folded into the first SCORM pilot.

### 2. Major Incident War Room

A timed branching scenario with alerts, executive pressure, duplicate reports, incomplete information, and communication demands. It scores escalation discipline, evidence use, role clarity, and communication.

Useful, but probably not before the first revenue signal.

### 3. CAB/Change Simulator

Students review a change record, CMDB dependencies, rollback plan, test evidence, and business calendar. Output is approve, defer, emergency, standard, or reject with rationale.

This is a strong second-wave tool after the Part 1 pilot.

### 4. DORA Metrics Lab

Feed students synthetic GitHub Actions runs and incident records. They calculate deployment frequency, lead time, change failure rate, and MTTR, then choose an improvement.

This is relatively buildable because the data can be synthetic and deterministic.

### 5. Postmortem Builder

A timeline editor plus blame-language detector. It pushes students away from "human error" and toward missing guardrail, weak alert, brittle deploy step, unclear handoff, undocumented assumption, or overloaded person.

This would be valuable in a corporate workshop version.

### 6. Vendor/CRM Handoff Mapper

Students drag buying roles, sales promises, support obligations, SLA risks, renewal signals, and ITIL records onto one pursuit timeline.

This would help make Part 5 feel more operational and less like sales vocabulary.

### 7. Startup IT Cost/Risk Calculator

Students build a small-organisation stack, see monthly cost and risk exposure, then generate a 30/60/90 remediation plan.

This has strong workshop and downloadable-template value.

### 8. Data Stewardship Memo Tool

A guided memo for access tier, authority, licence or agreement, benefit return, and review process.

For Indigenous data, this tool must not pretend to make the decision. It should force students to identify whose authority is required, what review process applies, and how the decision will be recorded.

## ServiceNow Versus Native Simulation

Build the ITIL simulation, but do not build a ServiceNow clone.

Use native course simulations for:

- Repeatable SCORM assessment.
- Offline or no-login learner paths.
- Stable grading.
- Scenario customisation per buyer.
- Concepts that transfer across ITSM platforms.

Use ServiceNow PDIs for:

- Real interface familiarity.
- Platform literacy.
- Optional confirmation labs.
- Screenshot or field-value evidence where access is available.

Do not make ServiceNow load-bearing for SCORM completion. PDI availability, hibernation, one-instance limits, interface changes, and account provisioning make that too brittle for a buyer-ready course.

The right sequence is:

1. Learn the concept in the native simulator.
2. Optionally reproduce the flow in ServiceNow.
3. Submit screenshots or field values as evidence.

## Claude Fable 5 Review Notes

The Claude Fable 5 critique agrees with the core simulation-versus-ServiceNow decision, but pushes harder on sequencing and commercial validation.

The strongest points from that review:

- Assessment is the sellable layer, not the content.
- The course needs one buyer-ready pilot more than it needs several tools.
- Build only the incident triage simulator before seeking revenue signals.
- Put that simulator inside a Part 1 SCORM pilot and validate it in Moodle.
- Build the war-room and CAB simulators after someone has paid or a pilot customer has committed.
- A landing page, terms statement, sample lessons, and SCORM pilot should come before more writing.
- Indigenous data sovereignty content needs paid Indigenous review before being marketed as a differentiator.
- Accessibility is a procurement gate, especially for universities and government.
- Volatile claims need a `last-verified` discipline, not just a plan.
- The course map currently looks imbalanced because Parts 5 and 6 are much larger than the earlier parts.
- A completion payoff matters: even a self-issued certificate or Open Badge changes learner incentives.
- A missing licence or terms statement is especially awkward for a course that teaches licensing.

## Commercial Priority

The likely fastest path is not an individual self-paced product. The stronger beachhead is MSPs, consultancies, graduate programs, and possibly RTO or university partners.

MSPs are especially plausible because they constantly onboard juniors into customer-facing work and often lack mature internal learning design. The course mix of ITIL, vendor management, small-business IT, CRM/customer handoffs, RCA, and support judgement is close to their operating reality.

The broad positioning should lean into the 2026 problem:

> AI can write more code, but early-career technologists still need professional judgement: incidents, changes, vendors, customers, governance, and data authority.

## Next Five Moves

1. Build a landing page with a clear course promise, buyer options, sample lesson links, and an explicit terms/licensing statement.
2. Polish three sample lessons with audio and worksheets. Strong candidates: Part 3 DORA, Part 4 RCA, and Part 6 startup IT assessment.
3. Build a Part 1 SCORM pilot with quiz interactions plus the incident triage simulator. Validate it in Moodle.
4. Do direct outreach to five MSPs and two graduate-program or institutional contacts using the pilot.
5. Commission Indigenous review before selling Part 7 as a differentiator.

## Do Not Build Yet

- A full ServiceNow clone.
- Three or more simulators before the first pilot.
- A full individual self-paced sales funnel before the institutional/cohort offer is tested.
- More Part 7 marketing without Indigenous review.
- More content expansion that delays packaging.

## Near-Term Implementation Notes

- Keep scenarios as structured data files so client-specific custom builds can swap names, organisations, tickets, and policy details without rewriting the simulator.
- Generate quiz/runtime output from source files rather than hand-maintaining LMS pages.
- Keep SCORM 1.2 as the compatibility target unless a buyer specifically asks for something newer.
- Preserve richer internal simulator scoring for future xAPI/cmi5 reporting.
- Add `last-verified` metadata to volatile topics and market/pricing notes.
- Add accessibility checks to the product definition: keyboard navigation, transcript availability, alt text, contrast, and non-dead audio controls when audio is missing.
- Add an explicit licence/terms page before public commercial outreach.

