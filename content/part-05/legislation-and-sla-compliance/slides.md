---
marp: true
title: Legislation and SLA Compliance
---

# Legislation and SLA Compliance
*Building contracts that respect global privacy law*

---

## Why legislation matters in SLAs
Speaker A: Before we negotiate uptime percentages, let's talk about what happens when things go wrong...
Speaker B: We keep talking about "strong SLAs". Why drag privacy law into a commercial contract?
Speaker A: Because regulators do not care that a vendor missed its target. If personal data leaks, the customer of record is still on the hook.
Speaker B: So we use the contract to push legal obligations onto the vendor?
Speaker A: Exactly. SLAs need clauses that align with statutory duties, otherwise fines and breach notifications land on us.
Speaker B: Think of legislation as the non-negotiable baseline before we even discuss uptime numbers.

---

## Australia’s Privacy Act 1988 (APP 11)
Speaker A: What does APP 11 actually require from a SaaS provider?
Speaker B: It demands reasonable steps to secure personal information and to destroy or de-identify it once it is no longer needed.
Speaker A: Remember the Medibank hack—9.7 million records exposed. APP 11 "reasonable steps" failed and class actions north of $50M followed.
Speaker B: In an SLA we convert that into encryption standards, 30-day breach notifications and secure disposal guarantees.
Speaker A: We also need audit rights to prove those "reasonable steps" exist. Without evidence, we cannot defend ourselves to the OAIC.
Speaker B: Include joint incident response drills so vendors are not improvising when something goes wrong.

---

## Security of Critical Infrastructure Act 2018
Speaker A: Some clients insist on Critical Infrastructure Act coverage. What changes in the contract?
Speaker B: The Act mandates risk management programs, rapid reporting and government access for declared systems.
Speaker A: So SLAs must reference the customer’s critical asset register and specify how the vendor supports 12-hour incident notifications.
Speaker B: We also need clauses for mandatory cyber incident reports and cooperation with the Australian Signals Directorate.
Speaker A: 12-hour reporting to ASD? That's faster than most vendors respond to support tickets!
Speaker B: Welcome to critical infrastructure—where incident response moves at government speed.
Speaker A: If the vendor cannot meet those obligations, they are not a fit for essential services customers.

---

## EU General Data Protection Regulation (GDPR)
Speaker A: GDPR penalties can hit 4% of global turnover. How do we flow that risk down?
Speaker B: Add Data Processing Agreements that mirror Articles 28–32—lawful processing instructions, sub-processor approval, and technical safeguards.
Speaker A: British Airways paid £20M after the 2018 breach—originally a £183M fine. That’s why we need bulletproof DPAs and liability caps that reflect exposure.
Speaker B: Cross-border transfers require Standard Contractual Clauses or an adequacy mechanism baked into the SLA.
Speaker A: Breach notifications must go to regulators within 72 hours; include playbooks and contact trees that make that possible.
Speaker B: Right-to-audit clauses should explain cadence, scope and confidentiality so we can inspect controls without detonating the relationship.
Speaker A: Regular penetration tests and encryption at rest/in transit should be contractually required, not just "best effort" promises.

---

## China’s Personal Information Protection Law (PIPL)
Speaker A: PIPL feels similar to GDPR but with sharper edges. What do we contract for?
Speaker B: Explicit consent and data localisation are front and centre. Vendors hosting Chinese citizen data must keep it on approved infrastructure.
Speaker A: Didi was yanked from app stores after PIPL violations—cross-border data flows aren't theoretical anymore.
Speaker B: We negotiate onshore hosting commitments, security assessments for cross-border transfers, and clear data classification responsibilities.
Speaker A: Breach reporting is on a tight timeline, and regulators can pause exports, so vendors need contingency capacity inside China.
Speaker B: Without those assurances, we risk suspension of operations in the world’s largest market.

---

## Data residency & sovereign cloud obligations
Speaker A: Legislation keeps asking, "Where is the data?" How do we answer for government clients?
Speaker B: Australian sovereign cloud policies demand certified regions, ASD-assessed staff and local support footprints.
Speaker A: Bake in residency commitments, segregation models and evidence packages—think IRAP reports, hosting diagrams and data flow maps.
Speaker B: For multi-region SaaS, demand approval rights before any replication offshore and insist on exit plans for repatriating data if laws tighten.

---

## Practical checklist for vendor negotiations
Speaker A: How do we keep all these laws straight during negotiations?
Speaker B: Use a compliance matrix mapping each legislation to concrete contract clauses, evidence requirements and reporting SLAs.
Speaker A: Involve legal, security and privacy officers early so they can review the draft before procurement signs.
Speaker B: Require periodic attestations—SOC 2, ISO 27001, IRAP—as proof that controls are still operating.
Speaker A: So compliance is like uptime monitoring?
Speaker B: Exactly—except regulators don't accept 99.9% availability for your privacy controls!
Speaker A: Pro tip: Lead with compliance requirements, not pricing. Vendors who can't meet legal obligations will negotiate themselves out.
Speaker B: Update your playbooks annually; legislation evolves and so should the contracts.

---

## Liability, insurance and audit strategy
Speaker A: How do we balance risk between us and the vendor?
Speaker B: Set liability caps that reflect statutory fines, carve out uncapped indemnities for privacy breaches and mandate cyber insurance limits.
Speaker A: Pair those caps with clear audit rights—scheduled reviews, targeted evidence requests and third-party assessors when issues emerge.
Speaker B: Add remediation timelines and claw-back clauses so failures have tangible consequences, not just apologies.

---

## US and industry-specific obligations
Speaker A: Our clients keep asking about US privacy laws. What belongs in the SLA?
Speaker B: California’s CCPA/CPRA give consumers deletion and opt-out rights—mirror GDPR workflows and demand vendor cooperation within 45 days.
Speaker A: Regulated industries have their own rules: APRA CPS 234 wants strong security governance for banks, and the TGA polices clinical software.
Speaker B: Map those sector expectations into annexes—extra controls, breach notifications to regulators, and specialist assurance reports.

---

## Key takeaway
Speaker A: SLAs are not just promises between two companies.
Speaker B: They are the tools we use to comply with national and international privacy regimes.
Speaker A: Translate each law—Privacy Act, Critical Infrastructure, GDPR, PIPL, CCPA, sector regs—into precise obligations.
Speaker B: Demand evidence, joint response plans, localisation commitments and aligned insurance.
Speaker A: When regulators come knocking, the contract should show we planned for the worst.
Speaker B: Good compliance clauses protect the business just as much as any uptime guarantee.
