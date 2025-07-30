---
marp: true
title: Contract Negotiation Basics
---

# Contract Negotiation Basics
*Setting terms that protect everyone*

---

## Why negotiate carefully
Speaker A: We have all seen boilerplate vendor contracts. Why not just accept them?
Speaker B: Remember the Black Friday payment system outage we mentioned earlier? If you sign standard terms, you might find those "industry standard" uptime guarantees are worthless.
Speaker A: So we press for clear uptime commitments, detailed service levels, and the ability to exit if things go south.
Speaker B: Exactly. A well-negotiated contract tells the vendor how quickly they must respond, how they'll compensate you, and what recourse you have if service fails.
Speaker A: It also locks in pricing so you don't face huge renewal hikes.
Speaker B: Negotiation sounds tedious, but think of it as building a safety net before you walk the tightrope.

---

## Typical SLA terms
Speaker A: Uptime numbers look impressive, but let's translate them into real impact. 99.9% uptime allows about 8.7 hours of downtime a year; 99.99% cuts that to under an hour.
Speaker B: Picture your ecommerce store offline for a full business day during peak season. That's more than an inconvenience—it's lost revenue.
Speaker A: Good SLAs also clarify incident notification and escalation paths.
Speaker B: Plus, penalties or credits if the vendor misses targets. "Best effort" or "reasonable attempts" is code for "we'll try, maybe."
Speaker A: Security and data handling should meet your compliance needs. If customer information leaks, you may face fines before the vendor even apologizes.
Speaker B: Strong SLAs keep daily operations running smoothly and give you leverage when they don't.

---

## Pricing models
Speaker A: Let's talk money. Vendors offer flat fees, per-user pricing, or pay-as-you-go models.
Speaker B: The last one can be surprising. One startup projected $500 a month on AWS but got a $5,000 bill during a holiday rush.
Speaker A: Compare that with a fixed $2,000 a month hosting plan—expensive on quiet days, but stable during busy times.
Speaker B: Ask about volume discounts, yearly increases, and onboarding fees.
Speaker A: And watch out for seemingly minor charges, like mandatory training or premium support.
Speaker B: It's like buying a cheap printer and discovering the ink costs a fortune. Do the math for best and worst-case scenarios so you know what you're signing up for.

---

## Exit and renewal options
Speaker A: Ever heard of a company stuck in a contract for six months after service went downhill?
Speaker B: Unfortunately yes, because they needed 180 days' notice to terminate. Always read the exit clause.
Speaker A: Look for data portability promises too. When vendor X went bankrupt, company Y lost three months of data because extraction wasn't covered.
Speaker B: Renewal terms deserve equal attention. Automatic price increases can sneak up on you if you don't have time to renegotiate.
Speaker A: Treat the exit plan like a fire drill. You hope you never need it, but you'll be glad it's there in a crisis.
Speaker B: A clear renewal calendar and exit path keep you in control rather than locked in.

---

## Risk assessment frameworks
Speaker A: How do you know if a vendor is risky? Start by checking financial stability—are they profitable or bleeding cash?
Speaker B: Then examine security posture. When was their last penetration test and how quickly do they patch?
Speaker A: Frameworks like NIST's vendor risk assessment or the SIG questionnaire provide structured questions.
Speaker B: Score areas such as finance, security, and support history. If they fall below your threshold, reconsider.
Speaker A: This process isn't just bureaucracy. Think of it as weather forecasting before a hike; you want to know if a storm is coming.
Speaker B: Document the results and revisit them annually. Circumstances change, and so should your risk profile.

---

## Regulatory and legal considerations
Speaker A: When should lawyers join the negotiation?
Speaker B: Early—especially for industries like healthcare or finance.
Speaker A: Violating HIPAA can cost over $50,000 per incident, while ignoring PCI-DSS might halt your ability to process payments.
Speaker B: International deals complicate matters further. Data sovereignty laws may forbid storing customer data outside certain regions.
Speaker A: Also consider time zones and jurisdiction in case of disputes. Which court will hear them?
Speaker B: Legal review clarifies intellectual property rights and liability caps so you don't pay for the vendor's mistakes. It might feel tedious, but skipping it could be expensive.

---

## Vendor evaluation checklist
Speaker A: Before signing, what questions should we ask?
Speaker B: Start with references—call current customers and ask what went wrong and how issues were handled.
Speaker A: Verify security certifications such as SOC 2, then check financial health via credit ratings or public statements.
Speaker B: Try the support line before signing to measure response time. If they ignore a prospective client, imagine their attitude once you're locked in.
Speaker A: Finally, map requirements from your RFP directly to contract terms so sales promises don't vanish.
Speaker B: This checklist prevents nasty surprises after the ink dries.
Speaker A: Some teams even create a weighted scoring rubric so every vendor is judged fairly.
Speaker B: A quick search for past legal disputes also helps reveal hidden issues.


---

## Red flags and hidden costs
Speaker A: What warning signs should make you think twice?
Speaker B: Watch for vague language like "industry-standard pricing" with no actual numbers. That's often sales talk for "expensive."
Speaker A: Beware heavy reliance on proprietary tools that don't play nicely with others. If you can't move data or integrate systems, you're trapped.
Speaker B: Discounts that vanish after year one are another trap. I've seen a $50 per-user software fee jump to $100 once "promotional pricing" expired.
Speaker A: And check for unilateral change clauses where the vendor can update terms whenever they like.
Speaker B: If support levels are worse than what the sales team promised, push back. Otherwise you're locked into a bad deal.

---

## Post-contract relationship management
Speaker A: Negotiation doesn't end when the contract is signed.
Speaker B: Schedule quarterly service reviews to discuss performance metrics and upcoming changes.
Speaker A: Include training and documentation requirements so your team isn't left guessing how to use the platform.
Speaker B: Ongoing knowledge transfer keeps you independent rather than reliant on expensive vendor consultants.
Speaker A: Treat the relationship as a partnership, using SLA reports to justify renewals or call out issues early.
Speaker B: If problems pile up, escalate according to the contract and start planning that exit path.
Speaker A: Document lessons learned and update playbooks so mistakes do not repeat.
Speaker B: Celebrate successes too; recognizing good performance builds trust.

---

## Service delivery models
Speaker A: Not all services are delivered the same way. Are you outsourcing everything or sharing responsibilities?
Speaker B: You might use a hybrid model where some services stay in-house while others go to a managed provider.
Speaker A: Multi-vendor setups add complexity. If your CRM is hosted by one provider and your analytics by another, who takes the blame when integrations break?
Speaker B: Clear contracts specify responsibilities so you avoid finger-pointing later.
Speaker A: Matching the delivery model to your business needs ensures you get the right support without paying for unnecessary extras.
Speaker B: Consider how these models will evolve as the business scales.

---

## Integration requirements
Speaker A: Have you confirmed the vendor's system actually works with your existing tools?
Speaker B: Check API access, data exchange formats, and authentication methods.
Speaker A: A vendor might claim "it integrates with everything" only for you to learn that "everything" means their other paid products.
Speaker B: Clarify upfront whether you'll need custom development, middleware, or extra licenses.
Speaker A: Poor integration can turn a simple project into a costly headache, especially if data needs to flow in real time.
Speaker B: Document these requirements in the contract so there's no dispute later.
Speaker B: Don't forget about data format quirks; mismatched CSV headers can derail a migration.
Speaker A: Add integration testing milestones so problems surface well before go-live.

---

## Scalability and growth planning
Speaker A: What happens when your business triples in size?
Speaker B: Make sure the contract allows for scaling up—or down—without punitive fees.
Speaker A: Include options for additional capacity, more users, or even moving to a larger service tier.
Speaker B: I've seen companies caught off guard by data growth charges that skyrocketed after a successful marketing campaign.
Speaker A: Also plan for shrinking usage if business slows; you shouldn't pay for unused capacity.
Speaker B: Scalability clauses protect you from outgrowing the vendor or wasting money when demand drops.
Speaker A: Build forecast models to estimate resource needs and confirm pricing scales sensibly.
Speaker B: Some vendors offer burst capacity on demand—handy during seasonal spikes.

---

## Key takeaway
Speaker A: Negotiating a contract is about more than price.
Speaker B: A well-crafted agreement covers uptime, pricing, exit strategies, and how the service will grow with you.
Speaker A: Use structured risk assessments and thorough checklists to evaluate vendors.
Speaker B: Bring in legal expertise early, especially for international or regulated industries.
Speaker A: Keep the relationship healthy with regular reviews and training, and be ready to pivot if performance slides.
Speaker B: Good contracts form partnerships that survive growth, change, and the occasional curveball.
Speaker A: Remember the holiday outage scenario? Strong SLAs and careful integration planning could have prevented it.
Speaker B: Invest the time now for fewer sleepless nights later.
