---
marp: true
title: Vendor Risk Management
---

# Vendor Risk Management
*Protecting continuity and security*

---

## Why worry about vendor lock-in?

Vendor lock-in happens when switching away from a service becomes expensive or 
technically difficult. Imagine all your files saved in a format that only one
vendor's software understands. Changing providers might require costly data
conversions or lengthy downtime, so the vendor holds all the power. Real-world
examples range from custom Salesforce integrations that won't export cleanly to
cloud platforms with no easy migration path. Warning signs include contracts
with 12‑month notice periods, proprietary data formats, or ongoing integration
fees that grow over time. It's like dating someone who slowly moves all your
stuff to their place—leaving suddenly becomes a major project. Always ask,
"How do we get our data out if we need to leave?" up front and negotiate
reasonable exit clauses before signing anything.

---

## Safeguarding data security

Handing over data to a vendor is like giving someone the keys to your house.
You want to know their locks are strong and they actually monitor who comes and
goes. Ask about encryption both in transit and at rest, and check whether staff
undergo background checks before they can access your information. Find out
where servers are located because privacy laws differ around the world. Don't be
shy about their breach history—have they ever disclosed incidents and how long
did notification take? A reputable vendor will gladly provide documentation such
as SOC 2 or ISO 27001 certifications and will outline their incident response
process. If they dodge questions or claim "trust us," that's a red flag. Asking
about security shouldn't feel like interrogating a spy; if they're evasive,
that's your answer right there.

---

## Business continuity planning

Every vendor will claim they have backups, but have those backups ever been
restored in a real emergency? Ask to see test results or drills where the vendor
simulated a failure and recovered systems. Business continuity also means
thinking beyond a single provider. Maintain a secondary supplier or at least a
clear exit clause so you can pivot if their service goes dark. Map out
escalation paths for different severities—who do you call if the service is down
for an hour versus a day? Having a well‑practiced plan keeps you operating when
surprises strike, just like carrying an umbrella even when the forecast looks
sunny.

---

## Financial risk assessment

- Analyse licensing models carefully: is pricing based on users, data volume or something else entirely?
- Watch for per-seat pricing that looks cheap at 10 users but explodes to $50K at 500.
- Factor in currency swings and automatic renewal clauses that increase fees annually.
- Weigh the stability of startups versus established firms—one may cost less but carry higher risk.

- Case study: one firm spent $200K migrating from Oracle to PostgreSQL after licensing fees spiked.
- Thorough financial reviews early on prevent nasty surprises later.

---

## Operational dependencies

Relying on a single vendor can create a fragile chain of dependencies. If their service goes down, do your internal processes grind to a halt? Consider how long it would take staff to learn a replacement system or rebuild integrations. A real-world outage, like Slack's six-hour downtime in 2021, left many teams scrambling because chatbots and help desks all flowed through a single tool. Document alternative workflows—when Slack is down, teams might revert to email threads and phone trees—and build training time into your budget so switching providers doesn't paralyse your organisation.

---

## Legal and compliance considerations

Data sovereignty laws and industry regulations can dictate where and how vendor services operate. Ensure that contracts spell out who owns the data, how it may be used and what liability the vendor carries if they breach privacy or security requirements. Ask about compliance certifications relevant to your sector. For example, healthcare providers must verify HIPAA compliance before putting records in the cloud, while retailers may need PCI DSS for payment details. Some jurisdictions require your data to remain in-country, so confirm server locations and backup storage. Insurance coverage and indemnity clauses also play a role; they define who pays if things go wrong. Understanding these legal obligations up front reduces headaches later.

---

## Due diligence checklist

- Evaluate financial stability and customer references
- Review security certifications and audit reports
- Test data export options before signing

---

## Red flags during selection

- Evasive answers about pricing or compliance
- No references or vague case studies
- Unrealistic implementation timelines

---

## Exit strategy planning

- Negotiate clear termination clauses and notice periods
- Document data migration steps and associated costs
- Keep alternative vendors in mind in case you need to switch

---

 ## Key takeaway

 - Ask about data export options before signing
 - Verify security certifications and test backups
 - Schedule regular reviews to keep risks visible
 - Document who owns each vendor relationship internally
 - Hold a quarterly risk review to track emerging issues

---

