Six weeks into the hiring spree we watched in Part 6, one of Sarah's new developers needs to parse dates in three formats. He finds a tidy JavaScript helper on someone's blog, pastes it into the product, and moves on. There's no licence file and no attribution — which does not mean the code is free to use. With no permission, Sarah's company may be shipping code it has no right to reproduce or distribute. A copyleft notice would create a different analysis: the obligations depend on the licence, what has been modified or combined, and how the product is conveyed or made available. Either problem tends to surface at a bad moment, such as an automated scan during investor due diligence.

Free and open-source software (FOSS) licences make those permissions explicit. The Open Source Definition describes criteria including free redistribution, source-code availability and permission for derived works; individual licence texts then state the operative rights, conditions and disclaimers. Read the actual text and obtain legal advice for material risk. [@osi-definition]

## Permissive licences: MIT, BSD and Apache 2.0

Permissive licences generally grant broad rights to use, modify and redistribute code, including in closed-source products, while requiring preservation of notices or licence text. They commonly disclaim warranty and liability; the exact conditions differ, so do not substitute a category label for the licence.

MIT and BSD are the shortest and loosest. Apache 2.0 adds two things enterprise risk teams care about. First, an explicit patent grant: every contributor licenses any patents their contribution would otherwise infringe. Second, a retaliation clause: if you sue anyone claiming the project infringes your patents, your own patent licence to the project terminates. That combination is why large companies often prefer Apache 2.0 over MIT for anything patent-adjacent.

Because permissive licences allow proprietary derivatives, they're the default choice for start-ups building commercial services, vendor integration teams, and agencies embedding open libraries in client work. React.js is the canonical example: Facebook shipped it under MIT so that product teams anywhere could build proprietary apps on top without asking permission — and adoption exploded accordingly.

The trade-off is reciprocity. A permissive licence gives you no legal lever to force improvements back upstream. Sustaining the project then depends on community goodwill, healthy governance, or a parallel commercial offering. If you're a first-time maintainer staring at the fine print, choosealicense.com and GitHub's built-in licence picker will walk you through the options before you click "public".

## Copyleft: the GPL family

Copyleft licences (including GPLv2, GPLv3, LGPL and AGPL) attach source-code and licensing conditions to specified forms of copying, modification, conveying or network use. Whether those conditions extend to a combined work is a legal and technical question about the licence and the way components interact, not a rule that any nearby proprietary code automatically becomes open source. [@gnu-licenses]

The mechanics matter, so be precise about them:

- GPL source obligations are generally tied to conveying covered or modified work rather than purely private use. The form of delivery and the work actually conveyed matter.
- **LGPL** is the softer variant for libraries: you may link it into a proprietary application without relicensing your own code, provided users can swap in and relink updated versions of the library.
- **AGPL** adds a network-interaction provision: when users interact remotely with a modified covered programme, the licence requires an opportunity to receive the corresponding source. It does not simply redefine every network interaction as distribution.

The Linux kernel is GPLv2, which is why Android handset makers must publish their kernel modifications every time they release a firmware image — some learned this the hard way. Same story if you ship a router with modified GPL firmware: matching source must be made available. Copyleft rewards collaboration-heavy ecosystems — public-sector platforms, civic tech, and organisations like Signal, which keeps its core GPL precisely so its privacy claims stay independently inspectable.

## Mixing licences without getting burned

Real products combine dozens of dependencies, and not all licences coexist happily. The working rules of thumb:

- **MIT/BSD** combines with almost anything; just preserve attribution.
- **Apache 2.0** combines with MIT, other Apache code and GPLv3 — but not GPLv2, whose terms clash with Apache's patent provisions. (GPLv3 was written partly to fix this.)
- **GPLv3** code can absorb permissive code, but the combined binary you distribute must be GPL.
- **AGPL** requires special attention for modified covered programmes offered over a network; read the licence rather than relying on a compatibility slogan.

Use a maintained compatibility source and legal review for consequential combinations so nobody discovers a licence conflict at the eleventh hour.

Some projects deliberately run two licence streams. MySQL and Qt offer their code under the GPL for the community and sell commercial licences to companies that want proprietary terms — a model that funds development while protecting openness goals. It only works if the steward holds the rights to relicense (more on that below) and is transparent about which features sit under which stream. MongoDB's shift to the Server Side Public License (SSPL) shows the same lever pulled defensively: a licence change designed to protect a business model from cloud providers reselling the product.

At the other extreme, CC0 lets a rights-holder waive copyright and related rights to the extent legally possible and supplies a fallback public licence where the waiver is ineffective. That structure accounts for differences between jurisdictions; it is not a declaration that every kind of right can always be abandoned. [@cc0]

Copyright terms, moral rights, database rights, Crown copyright and patent scope differ across jurisdictions. Established licence texts reduce avoidable ambiguity, but OSI approval is not a substitute for jurisdiction-specific advice. Document the chosen licence, notices, provenance and any legal review.

## Contributor agreements and choosing for your context

Once outsiders contribute, rights may be held by multiple people or employers. Contributor Licence Agreements can grant a project specified rights in contributions; their scope varies and should be read. Distinguish individual from corporate agreements, and check that the signatory has authority. Some projects instead use the Developer Certificate of Origin, under which contributors certify statements about the origin of a contribution by adding a `Signed-off-by` line. A DCO is a certification mechanism, not a copyright assignment. [@dco]

Choosing a licence is a cross-functional decision, not a checkbox. Start from goals: are you optimising for adoption, reciprocity, revenue, or community trust? The quick flow — need maximum adoption, go permissive; need guaranteed sharing, pick copyleft; need revenue plus openness, explore dual licensing. A worked example: a government agency building a records platform wants vendor fixes funded by taxpayers to stay public, so its open-source program office (OSPO) recommends GPLv3, legal sets up DCO-plus-CLA contribution intake, and the comms team briefs suppliers on what they're signing up for. Documenting that rationale now prevents a heated argument three years later when a new contractor joins. Involve legal counsel, community tech-leads, security engineers and product managers early — a licence choice is like a roommate agreement, and if you skip the awkward conversation about chores and guests, you'll have it later, angrier, with the mess already on the floor.

## Staying compliant — and who gets paid to care

Compliance is a process, not an event. Maintain a software bill of materials (SBOM) so you can prove which licences are in your build, and wire licence scanners into CI so incompatible combinations fail fast rather than surface in an audit. Record every redistribution moment (shipped binaries, published container images, a SaaS endpoint incorporating AGPL code) and keep source archives, NOTICE files and third-party attributions ready to go. Tools like FOSSA, OSS Review Toolkit and GitHub's dependency review do the tedious parts once configured. Companies have paid real settlements for ignoring GPL notices, so treat "we'll fix the licensing post-launch" as the red flag it is.

> Licence compliance is like flossing: tedious, easy to skip while everything seems fine, and the neglect only announces itself as an expensive, painful audit.

This work is a career path as well as a responsibility distributed across engineering, legal, security and procurement. OSPO analysts may arrive from software engineering, developer relations, compliance or technology law. The work rewards careful evidence, diplomacy and the ability to translate legal nuance for technologists without flattening it. Senior roles coordinate licence strategy, contribution policy and ecosystem relationships across business units.

The takeaway: licence selection is a strategic lever, not paperwork. It signals how you invite collaboration, how you protect contributors, and (when projects touch cultural knowledge, as later sections of this part explore) how you honour data sovereignty commitments. Teams that understand reciprocity obligations, international quirks, CLAs and dual licensing can design contribution models that sustain trust with communities, customers and partners for the long haul.
