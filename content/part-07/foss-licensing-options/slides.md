---
marp: true
title: FOSS Licensing Options and Obligations
---

# FOSS Licensing Choices
*Licences: the Terms & Conditions developers actually need to read*

---

## Why licences matter
- Define how code can be used, shared and monetised
- Protect contributors and organisations from legal risk
- Shape community expectations and collaboration norms
- Without clarity, even a tiny JavaScript helper in your start-up could trigger a takedown notice
- Licences are like relationship agreements—agree upfront so you are not lawyering up later

---

## Permissive licences (MIT, Apache 2.0)
- Allow reuse with minimal obligations
- Require attribution and licence notice retention
- Favoured by start-ups, vendor platforms and integration partners
- Example: React.js ships under MIT, empowering Facebook and thousands of companies to build proprietary apps
- Apache 2.0 adds patent protection and retaliation clauses to calm enterprise risk teams

---

## Copyleft licences (GPL family)
- Derivative works must remain open-source
- Trigger "share alike" obligations on distribution of binaries
- Common in infrastructure maintained by foundations and public agencies
- Linux kernel's GPL ensures Android handset modifications were upstreamed for everyone
- Think of it as a viral clause—openness spreads to everything it touches once you distribute
- Scenario: ship a router with modified GPL firmware? You must publish matching source

---

## Compatibility cheat sheet
| You use… | Safe to combine with | Watch-outs |
| --- | --- | --- |
| MIT/BSD | Almost anything | Preserve attribution |
| Apache 2.0 | MIT, Apache, GPLv3 | Patent terms clash with GPLv2 only |
| GPLv3 | GPLv3 code | Permissive code ok, but binaries must be GPL |
| AGPL | AGPL projects | Network use counts as distribution |

---

## Dual & multi-licensing
- Projects like MySQL or Qt offer GPL for community and commercial licences for proprietary users
- Enables sustainable funding while protecting openness goals
- Be transparent about which features fall under each licence stream

---

## Public domain & CC0
- CC0 and Unlicense place work in public domain where legally possible
- Useful for data sets, code snippets and government artefacts
- Confirm local law recognition—some jurisdictions restrict abandoning copyright

---

## International considerations
- Copyright terms, moral rights and patent scope differ across jurisdictions
- EU database rights and Australian Crown copyright can complicate reuse
- Global teams rely on OSI-approved texts to minimise surprises—document governing law in NOTICE files

---

## Contributor Licence Agreements (CLAs)
- Clarify that maintainers can relicense, defend or dual-license contributions
- Individual vs corporate CLAs—ensure signatories have authority
- Coordinate with Developer Certificate of Origin (DCO) processes for audit trails

---

## Choosing for your context
- Align licence with business model, funding and compliance needs
- Consider third-party code compatibility and patent clauses
- Involve legal counsel, community tech-leads and product managers early
- Quick flow: need maximum adoption? go permissive. Need reciprocity? pick copyleft. Need revenue + openness? explore dual licence.
- Example: a government agency picks GPL to keep taxpayer-funded improvements public
- Choosing a licence is like a roommate agreement—get it wrong and the dishes (or obligations) pile up fast

---

## Staying compliant
- Maintain a bill of materials (SBOM) and automate scans
- Document when you redistribute binaries, SaaS services or containers
- Licence compliance is like flossing—tedious, but it avoids painful audits later
- Tooling: GitHub’s licence picker and choosealicense.com guide first-time maintainers
- Note cautionary tales—companies have paid settlements for ignoring GPL notices

---

## Career pathways & responsibilities
- Roles & ratios: OSPO managers, developer advocates and legal counsels (typically 1–2 OSPO staff per 50–80 engineers)
- Typical seniority: mid-level engineers/lawyers stepping into governance after 5–7 years experience
- Entry pathways: community contributors, compliance interns, dual STEM-law graduates and policy analysts rotating from procurement teams
- Personality traits: detail-obsessed, diplomatic, values-driven collaborators who can translate legal nuance for technologists
- Progression: OSPO analyst → manager → director/VP stewarding ecosystem strategy across the organisation
- Case study: Signal keeps its GPL core open to ensure privacy protections stay inspectable—driving demand for specialised compliance engineers

---

## Key takeaway
Intentional licence selection balances openness, obligations and long-term sustainability.

---
