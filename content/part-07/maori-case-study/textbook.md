The previous sections of this part have argued that openness is a spectrum and that governance decides who benefits. Te Hiku Media is the case study that shows what those ideas look like when a community actually builds on them — not as a data subject in someone else's research program, but as the owner and operator of its own machine-learning pipeline.

Te Hiku Media is an iwi-owned broadcaster headquartered in Kaitaia, in Aotearoa's Far North, with a mission to revitalise te reo Māori through digital storytelling. It began as an iwi radio network, and that history turned out to be its greatest technical asset: decades of community archiving, including recordings of kaumātua voices, produced language archives that Silicon Valley cannot replicate at any price. When the big technology companies noticed — offering compute credits in exchange for access to the language corpora, essentially asking for the data for free — Te Hiku pushed back. They wanted partnership, not extraction. Rather than chase the fastest growth on offer, they prioritised mana motuhake — self-determination — and sought funding instead from Māori trusts and philanthropies aligned with language revitalisation. That funding choice is easy to skim past, but it is the hinge of the whole story: it let Te Hiku set the terms before anyone touched the corpus.

The case matters for this course because it demonstrates that "open" does not have to mean "public domain". Te Hiku uses openness strategically — sharing with whānau, iwi partners and trusted researchers — while still protecting taonga. It is a concrete example of cultural protocols shaping a modern machine-learning program, rather than being retrofitted onto one.

## Kaupapa Māori foundations

The governance model is anchored by guidance from Te Hiku's kaumātua and by the Kaitiakitanga licence, which states that the data is a treasure held in trust for present and future iwi members. Data is treated as taonga, and consent is grounded in whakapapa obligations — this is not a terms-of-service checkbox, but a relationship with responsibilities running in both directions. Any partner has to demonstrate reciprocity and cultural safety before touching the language assets.

The structures backing that up are concrete. A governance board spans iwi leaders, technologists and legal advisors, so cultural authority, engineering judgement and legal capacity sit at the same table. Community hui confirm priorities before any technology is deployed: linguists, kaumātua and technologists review project proposals together, and if whānau are not convinced the outcomes will uplift communities, the project pauses until the concerns are resolved. Notice what that is, in project-management terms — a stakeholder veto that actually functions. The team describes the result as a blend of tikanga and agile delivery, and it is precisely that blend that keeps sovereignty intact while software still ships.

## Building the corpus on community terms

Speech recognition needs data, and Te Hiku collected more than 300,000 sentences through community recording campaigns. The 2019 recording sprint has become legendary: community members lined up to donate sentences in kura, marae and community centres, and every session was paired with kai and cultural briefings so people understood exactly where their voices would go. Compare that with the industry norm, where the provenance of training data is a question the vendor hopes you won't ask.

On top of the corpus the team built Papakupu (lexicon) resources and automated speech recognition models. Mainstream annotation platforms couldn't handle the dialect nuances, so the team built a custom labelling tool, and engineers co-designed prompts with linguists and cultural advisors to capture dialectal diversity rather than just a "standard" te reo. Two contractual details would be unheard of in most corporate datasets: contributors retain their rights, including moral rights, and can revoke their samples; and the licence explicitly restricts extractive reuse. Consent, in other words, is engineered into the dataset itself.

## The stack, the safeguards and the roles

Technically, Te Hiku was pragmatic rather than purist. The team forked Mozilla Common Voice to jump-start its infrastructure, then stripped out anything that conflicted with Māori governance. Storage sits in region-limited, AWS-hosted S3 buckets in Auckland zones, with encryption keys controlled by Te Hiku, and every data access is logged for auditing by the board. Alongside conventional security reviews, the organisation runs regular tikanga audits, checking the system against cultural obligations, not just technical ones.

The product team pairs ML engineers and data stewards with cultural advisors and privacy counsel. Most instructive for this course's career thread is the formalised "data kaitiaki" role: people fluent in te reo who also understand privacy law, who sign off on data queries and review model outputs for cultural harm. It is a genuine career path blending community leadership with product-management skills — and the pipeline is deliberate, with internships for rangatahi and upskilling programs that move iwi staff into data governance roles.

## Negotiating with external partners

Sovereignty gets tested at the negotiating table. Te Hiku declined offers from major cloud vendors that lacked cultural safeguards — walking away from resources most startups would take without reading the fine print. When partnerships did proceed, they ran on memoranda of understanding that detailed reciprocity: commitments to fund language revitalisation, keep infrastructure in Aotearoa, share revenue, and give Te Hiku a veto over secondary uses of the data and models.

The contracts also carried tikanga clauses with teeth. Partner staff had to attend cultural safety training, models could not be repurposed for surveillance, and Māori IP protections were written in. Every partnership was staged as a pilot with opt-out checkpoints and independent oversight, so the community could walk away if promises were broken. For anyone who has sat through vendor negotiations, the pattern is worth studying: these are ordinary contract mechanisms — MOUs, staged pilots, exit clauses — deployed in service of cultural authority.

## Outcomes, and what practitioners should copy

The results are tangible. Te Hiku delivered production-ready te reo speech-to-text with major reductions in word error rate — accuracy gains that came precisely because the models were trained on dialect-specific data the community had gathered on its own terms. Iwi radio partners now use the automation to archive oral histories, with transcription that takes hours instead of months, and whānau can search recordings for tīpuna names. The influence spread outwards: Te Mana Raraunga referenced Te Hiku's licensing approach when drafting national Māori data governance principles, setting a precedent for Indigenous data licences. And the people grew with the project — Māori technologists moved into senior data governance leadership, with alumni now working across government, iwi corporations and platform co-ops.

For your own practice, the source material distils four lessons:

1. **Embed cultural authority in every technical milestone.** Kaumātua, elders or cultural experts should be leading alongside engineers, not consulted after the sprint review.
2. **Budget for roles that bridge tech and tikanga** — and promote those people into product leadership, because bridging roles wither when they have no career path.
3. **Use Indigenous-led licences to operationalise consent and reciprocity.** Treat the licence as a living document that expresses the relationship, not legal fine print to be minimised.
4. **Measure success by community benefit and language vitality, not just model accuracy.** Optimise only the metrics engineers find comfortable and the technology drifts away from its purpose.

The Te Hiku story closes this part deliberately. The licensing, governance and cultural-safety machinery in the earlier sections can read as constraint — process standing between you and shipping. Te Hiku demonstrates the opposite reading: a community that set its terms first, and got better technology because of it.
