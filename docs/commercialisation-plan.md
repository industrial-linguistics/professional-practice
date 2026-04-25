# Commercialisation Plan

Last checked: 2026-04-25.

## Positioning

The strongest commercial angle is not "generic IT career course". It is:

> Practical IT professional practice for graduates, junior technologists and non-technical operators who need to understand how real IT organisations work.

The content is unusual because it connects ITIL, DevOps/SRE, RCA, vendor management, CRM, startup IT and Indigenous data sovereignty in one coherent professional-practice course. That is more valuable to employers than a narrow tool tutorial.

## Best-fit customers

1. Graduate programs in medium and large employers.
2. Universities, colleges and pathway providers needing employability-oriented IT material.
3. MSPs and consultancies onboarding junior staff into customer-facing work.
4. Startup accelerators that need a practical "how not to make terrible IT decisions" module.
5. Government and non-profit programs that care about digital governance, procurement and data sovereignty.

## Offer ladder

| Offer | Buyer | Format | Commercial reason |
| --- | --- | --- | --- |
| Free public preview | Individual learners | Web pages, sample videos, selected run sheets | Builds trust and search visibility. |
| Self-paced course | Individuals and small teams | Hosted course with videos, quizzes and downloadable worksheets | Creates low-touch revenue, but should not be the only business model. |
| Cohort workshop | Employers, accelerators, universities | 1-2 day facilitated version using the same assets | Higher margin and gives feedback for content improvement. |
| Licensed SCORM/Moodle pack | Universities and corporate L&D | SCORM 1.2 package plus PDFs and assessments | Fits existing LMS procurement habits. |
| Custom build | Corporate graduate programs | Branded examples, local policies, tool screenshots, assessment rubrics | Best commercial fit for the README promise. |
| Advisory add-on | Employers and startups | Review of current onboarding/professional-practice material | Turns course sales into consulting leads. |

## Platform strategy

Do not rely on a marketplace as the primary business.

- Udemy is useful as a discovery and proof channel, but Udemy's own instructor support page says instructor-promotion sales and marketplace sales have very different revenue shares. Use it for reach, not as the main economics.
- A direct site with Stripe checkout is better for margin and customer ownership once the course is credible.
- A hosted course platform can reduce admin work, but platform/payment fees need to be priced into the offer.
- SCORM/Moodle export matters for institutional buyers. Moodle's SCORM activity supports uploading SCORM/AICC packages, so a clean SCORM 1.2 package is a reasonable target for universities and corporate L&D.

Useful current references:

- ElevenLabs API pricing and metering: <https://elevenlabs.io/pricing/api/>
- ElevenLabs credit model overview: <https://elevenlabs.io/docs/overview/intro>
- Udemy instructor revenue share: <https://support.udemy.com/hc/en-us/articles/229605008-Instructor-revenue-share>
- Teachable fees: <https://support.teachable.com/en/articles/11682553-teachable-fees>
- Moodle SCORM activity: <https://docs.moodle.org/39/en/SCORM>

## Packaging

Minimum viable commercial package:

1. One polished landing page with the course promise, audience, module list, sample lesson and buyer options.
2. Three high-quality sample lessons:
   - Part 3 DORA metrics or GitHub Actions.
   - Part 4 blameless RCA.
   - Part 6 startup IT assessment.
3. Downloadable worksheets:
   - Incident/RCA template.
   - Vendor evaluation scorecard.
   - Startup day-zero IT checklist.
   - Capstone proposal rubric.
4. One SCORM-compatible pilot module.
5. A facilitator guide for running it as a workshop.

## Pricing shape

Avoid setting exact prices until the first three polished lessons exist and production costs are known. Use these pricing boundaries:

- Individuals: price low enough to compete with marketplace expectations, but only for self-paced access.
- Teams: price by seat or cohort, with a minimum that covers support.
- Institutions: annual licence or per-cohort licence, including LMS package updates.
- Custom builds: fixed-scope project fee plus annual maintenance if they want updates.

ElevenLabs cost is manageable if S3 caching is enforced. The current text-to-speech API is metered per character, and Flash/Turbo pricing is lower per character than Multilingual v2/v3 on the current ElevenLabs pricing page. Use high-quality voice settings for paid masters, but use the cheapest acceptable model for drafts.

## Marketing plan

### Core message

"Most early-career IT training teaches tools. This teaches how the work fits together: incidents, releases, vendors, customers, startups, governance and ethics."

### Proof assets

- A public course map showing all eight parts.
- A short video from each of the DevOps/RCA/startup tracks.
- Before/after examples of a bad incident response becoming a structured RCA.
- A sample Salesforce-to-ITIL handoff map.
- A startup IT checklist that is useful even without buying.

### Channels

1. LinkedIn posts aimed at IT managers, graduate program owners and university employability teams.
2. Blog posts for specific pain points:
   - "What junior IT staff need to know before their first incident call."
   - "Why DevOps metrics belong in professional-practice training."
   - "A startup IT checklist for non-technical founders."
3. Direct outreach to:
   - University course convenors.
   - Graduate program managers.
   - MSP owners.
   - Startup accelerators.
4. Conference/workshop proposals for ITSM, higher-ed teaching and startup community events.
5. A small Udemy or marketplace version only after the direct offer exists, using it as a funnel to the custom and cohort offerings.

## Product roadmap

1. Fix slide/narrative mismatches in the existing content.
2. Add the priority diagrams from `docs/media-and-diagram-plan.md`.
3. Build three polished sample lessons with audio, video, captions and worksheets.
4. Build a simple public website that can host samples and collect enquiries.
5. Package one module as SCORM and test in Moodle.
6. Run a pilot cohort with 5-10 learners and collect feedback.
7. Create a custom-build sales deck for institutional buyers.

## Risks

- The course is broad. The commercial story must keep the theme clear: professional practice across IT roles.
- Part 5 and Part 7 need extra care; CRM/vendor lifecycle and Indigenous data sovereignty are strong differentiators but weak polish will damage trust.
- Tool screenshots can date quickly. Prefer durable process diagrams and mockups unless the lesson is explicitly about navigating a tool.
- Audio generation must be throttled and cache-aware; otherwise iteration can burn shared credits without improving the product.
