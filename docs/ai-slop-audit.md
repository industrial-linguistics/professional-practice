# AI Slop Audit — Website and Course Content

Scan date: 2026-07-26. Surfaces checked: `website/`, `content/**/slides.html`,
`content/**/narratives/*.md`, `content/**/textbook.md`, `content/**/outline.md`
and `content/**/quiz.md`. Generated `textbook/chapters/*.tex` were excluded —
they inherit whatever the sources contain.

`_source_before_alignment/` directories (399 tracked files) were excluded from
counts. They are superseded drafts and repeat the same problems as the live
files.

## Headline

`scripts/validate_textbook_sources.py` already carries a `BANNED_PHRASES` list
and currently reports **zero** hits. That result is real but narrow: the
validator only reads `content/part-*/*/textbook.md` and
`content/part-*/textbook-intro.md`. The same list applied to the other
surfaces finds three more hits, and the surfaces it never sees contain the
worst material in the repository.

Ranked by how much they matter:

1. Templated narrative filler — 159 files, spoken aloud by the TTS pipeline.
2. Formulaic website part blurbs — 8 of 8 built from the same sentence frame.
3. A short tail of genuine cliché — roughly a dozen lines worth changing.

## 1. Templated narrative filler (highest priority)

**159 of 738 narrative files (22%), spanning 47 topics.**

`scripts/repair_narrative_alignment.py:78-98` synthesises narration when a
slide has no hand-written script. It emits fixed sentence frames:

| Template | Occurrences | Source |
| --- | --- | --- |
| `<Title> focuses attention on a concrete part of the work.` | 126 | `repair_narrative_alignment.py:96` |
| `In practice, ask who owns the work, what evidence proves it happened, and what handoff comes next.` | 126 | `repair_narrative_alignment.py:97` |
| `Use the supporting details as a checklist: …` | 114 | `repair_narrative_alignment.py:94` |
| `This section sets up <Title>. Treat it as the frame for…` | 27 | `repair_narrative_alignment.py:80` |
| `The practical question is simple: by the end, what should a junior IT professional…` | 27 | `repair_narrative_alignment.py:82` |
| `The key takeaway is this: …` | 6 | `repair_narrative_alignment.py:88` |
| `Use that takeaway to name the owner, evidence, and next action…` | 6 | `repair_narrative_alignment.py:89` |

This is worse than cliché vocabulary. The sentences carry no information about
the topic — the same two lines are spoken over 126 different slides. It
contradicts `docs/textbook-authoring-guidelines.md` ("The same transition
twice") and `textbook/audit/slop-patterns.md` ("Avoid generic motivational
bridge prose"), and unlike prose slop it reaches students as audio.

Worst-affected topics:

| Topic | Templated narratives |
| --- | --- |
| `content/part-06/investor-due-diligence-prep` | 12 |
| `content/part-05/contract-negotiation-basics` | 12 |
| `content/part-06/vendor-management-rhythms` | 11 |
| `content/part-06/cloud-vs-on-premise-decisions` | 10 |
| `content/part-05/legislation-and-sla-compliance` | 9 |
| `content/part-07/foss-licensing-options` | 6 |
| `content/part-05/risk-management` | 6 |

### Garbled sub-case

13 of these files interpolate a slide **table** into the template, producing
text that is unreadable and unspeakable. From
`content/part-07/foss-licensing-options/narratives/05-compatibility-cheat-sheet.md:1`:

> Speaker 1: Compatibility cheat sheet focuses attention on a concrete part of
> the work. You use…Safe to combine withWatch-outs, MIT/BSDAlmost anythingPreserve
> attribution, and Apache 2.0MIT, Apache, GPLv3Patent terms clash with GPLv2 only.

Affected files:

- `content/part-04/rca-servicenow-github/narratives/06-common-pitfalls.md`
- `content/part-05/lead-scoring-opportunity-progression-renewal-alerts/narratives/06-integration-challenges.md`
- `content/part-05/linking-crm-milestones/narratives/04-when-the-alignment-breaks.md`
- `content/part-05/linking-crm-milestones/narratives/08-integration-pitfalls-to-watch.md`
- `content/part-06/fractional-cto-and-msps/narratives/13-industry-geography-and-scaling-considerations.md`
- `content/part-06/investor-due-diligence-prep/narratives/03-core-workstreams-to-coordinate.md`
- `content/part-06/investor-due-diligence-prep/narratives/05-security-questionnaire-watch-outs.md`
- `content/part-06/investor-due-diligence-prep/narratives/09-roles-traits-and-progression.md`
- `content/part-06/investor-due-diligence-prep/narratives/12-case-study-nimbuspay-series-a.md`
- `content/part-06/scaling-support-processes/narratives/10-budget-justification-toolkit.md`
- `content/part-06/security-baselines-shoestring/narratives/03-security-jargon-decoder-for-new-it-pros.md`
- `content/part-07/foss-licensing-options/narratives/11-staying-compliant.md`
- `content/part-07/foss-licensing-options/narratives/05-compatibility-cheat-sheet.md`

### Recommendation

Hand-write these 159 narratives against the slides, working down the
worst-affected topics. Fixing the generator does not fix the committed files;
it only stops the next batch. If the generator is kept as a scaffold, it should
mark its output (front-matter flag or `TODO` line) so unrewritten stubs cannot
reach the audio build unnoticed, and it should skip table slides rather than
flatten them.

## 2. Website copy

`website/index.html` is generated by `scripts/generate_website_index.sh`; the
per-part blurbs come from line 3 of each `content/part-*/outline.md`, so fixes
belong in the outlines, not the HTML.

All eight blurbs use the same frame — "This part introduces / builds on /
introduces / focuses on / demystifies / highlights / explores", then "This
capstone brings". Read down the page it scans as a generated catalogue. Varying
the openers is a cheap, high-visibility improvement, since this is the only
public-facing prose in the repository.

Specific lines:

| Location | Text | Issue |
| --- | --- | --- |
| `content/part-05/outline.md:3` | "demystifies how vendors… the customer journey from first outreach to renewal" | "demystifies" is marketing register; "customer journey" is defensible as CRM terminology |
| `content/part-07/outline.md:3` | "evaluate open-source solutions through an ethical lens" | "through an … lens" is stock filler; name the actual judgement |
| `content/part-03/outline.md:3` | "modern DevOps practices… enable organizations to deliver software rapidly while maintaining reliability and quality" | Generic vendor-brochure sentence; also US "organizations" (see §5) |
| `content/part-04/outline.md:3` | "establishing a culture of learning… using structured approaches to drive service improvements" | "structured approaches" is a placeholder for the thing itself |
| `website/index.html:15` | "while the generated e-learning and textbook surfaces mature" | Hedge about incomplete work, visible to prospective students |

The hero copy ("The missing professional-practice course for technical
graduates") is deliberate positioning rather than slop, and the `For / About /
Output` block is concrete. Neither needs changing.

## 3. Genuine cliché hits

Small tail. Each verified in context.

| Location | Text | Verdict |
| --- | --- | --- |
| `content/part-05/linking-crm-milestones/slides.html:188` | "customers experience seamless transitions from promise to production stability" | **Fix.** Hits the project's own banned list; pure service-marketing adjective. Name the handoff. |
| `content/part-02/metrics-reporting-dashboards/slides.html:6` | "Turning raw data into actionable insight" | **Fix.** Stock dashboard-vendor subtitle. |
| `content/part-06/scaling-support-processes/slides.html:44-45`, `textbook.md:19` | "Knowledge base as force multiplier" | **Fix.** Consultant register in a slide title and a heading; "deflection" or "what the KB absorbs" is more precise. |
| `content/part-06/shadow-it-low-code-experimentation/slides.html:6` | "Empower creativity without losing control" | **Fix.** Slide subtitle in motivational register. |
| `content/part-03/sre-error-budgets/slides.html:42` | "Foster data-driven reliability conversations" | **Fix.** Bullet built from stock verbs. |
| `content/part-04/post-mortem-culture/slides.html:6` | "Fostering open discussion and avoiding finger-pointing" | **Borderline.** "Fostering" is limp but the second half is concrete. |
| `content/part-06/quiz.md:134` | "Leverage the remote logistics playbook by…" | **Fix.** Verb "leverage" where "use" works. |
| `content/part-05/customer-success-teams/slides.html:99` | "leverages API know-how" | **Fix.** Same. |
| `content/part-06/cloud-vs-on-premise-decisions/slides.html:38` | "leverage managed services with generous free tiers" | **Fix.** Same. |
| `content/part-02/continual-improvement/narratives/07-measuring-improvement-success.md:7` | "Employee engagement levels are crucial but often overlooked… Do they feel empowered" | **Fix.** Two flagged words plus a hollow claim. |
| `content/part-05/key-economics/narratives/07-land-and-expand-strategy.md:3` | "Customer success plays a key role by…" | **Fix.** "plays a key role" as filler. |
| `content/part-06/legal-compliance-reality-check/textbook.md:5` | "## The milestones, demystified" | **Borderline.** Heading register; the section itself is concrete. |

### Not slop — leave alone

Flagged by keyword search but correct in context. Recorded here so a future
pass does not "fix" them:

- **"leverage" as a noun** in Part 5/6 negotiation material
  (`vendor-management-rhythms/textbook.md:5,46`,
  `performance-monitoring/textbook.md:11`,
  `day-zero-assessment-checklist/textbook.md:30`,
  `problem-management-rca/textbook.md:41`) — this is the correct commercial
  term and the passages are among the strongest prose in the book.
- **"seamless integration"** at `fractional-cto-and-msps/slides.html:119` and
  `narratives/09-the-vendor-promise-vs-delivery-gap.md:5` — quoted vendor
  marketing, immediately mocked. Deliberate and effective.
- **"facilitator"** throughout Part 4 — the RCA role, not the verb.
- **"Vitally"** in Part 6 SaaS tables — a product name.
- **"language vitality"** in Part 7 — the standard term in Indigenous language
  revitalisation.
- **"state of the art"** at `dora-metrics/textbook.md:3` — used historically
  ("for most of the industry's history, that *was* the state of the art"), not
  as praise.
- **"Key takeaway"** as a slide heading (66 decks) — a deliberate deck
  convention, applied consistently. Formulaic by design, not accidental.
- **Em-dash density** — peaks at 4 per file; no file is an outlier. Not a
  problem here.

## 4. Validator coverage gap

`scripts/validate_textbook_sources.py` never sees slides, narratives, quizzes
or outlines. Extending the same `BANNED_PHRASES` check to those surfaces would
have caught §3 automatically, and adding the templated sentences from §1 as
banned strings would keep generator stubs from reaching a build.

Phrases worth adding to the list, all evidenced above:

`actionable insight`, `force multiplier`, `through an ethical lens`,
`plays a key role`, `plays a crucial role`, `empower` (as motivational verb),
`foster` (as motivational verb), plus the seven narrative templates from §1.

## 5. Adjacent finding — spelling inconsistency

Not slop, but it surfaced during the scan and points the same way. Content is
predominantly British/Australian, with a US minority:

| | British | US |
| --- | --- | --- |
| organis/organiz | 149 | 26 |
| prioritis/prioritiz | 43 | 10 |
| optimis/optimiz | 44 | 5 |
| recognis/recogniz | 15 | 2 |

The US spellings cluster in generated and blurb text, including
`content/part-03/outline.md:3`, which is on the public website. A spelling
check belongs in the same validator pass as the phrase check.
