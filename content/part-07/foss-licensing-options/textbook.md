Six weeks into the hiring spree we watched in Part 6, one of Sarah's new developers needs to parse dates in three formats. He finds a tidy JavaScript helper on someone's blog, pastes it into the product, and moves on. There's no licence file and no attribution — which does not mean the code is free to use. It means the opposite. With no licence, the author keeps all rights, and Sarah's company is now shipping code it has no permission to ship. Had the helper quietly carried a GPL notice instead, the risk changes shape: not a cease-and-desist, but a demand to publish the source of everything it was combined with. Either way, the discovery tends to happen at the worst possible moment — an automated scan during investor due diligence, eighteen months later.

Free and open-source software (FOSS) licences exist to prevent exactly this. A licence translates community values into legally enforceable rules: it defines how code can be used, shared and monetised, protects contributors and adopters from liability claims, and sets expectations for how the community collaborates. Without licences, open source would run on vague goodwill; with them, an organisation can adopt community-built code knowing precisely which obligations it is accepting, and a developer gets a real say in whether their work can be folded into proprietary platforms. Most licence disputes settle quietly, but the legal fees, disruption and damaged trust are real. Think of a licence as both a legal instrument and a social contract — like a relationship agreement, the point is to agree upfront so you're not lawyering up later.

## Permissive licences: MIT, BSD and Apache 2.0

Permissive licences grant broad rights to use, modify and redistribute code — including inside closed-source products — with minimal strings attached. The non-negotiables are small: preserve the copyright notice, include the licence text, and don't sue the authors when something breaks (every FOSS licence disclaims warranty).

MIT and BSD are the shortest and loosest. Apache 2.0 adds two things enterprise risk teams care about. First, an explicit patent grant: every contributor licenses any patents their contribution would otherwise infringe. Second, a retaliation clause: if you sue anyone claiming the project infringes your patents, your own patent licence to the project terminates. That combination is why large companies often prefer Apache 2.0 over MIT for anything patent-adjacent.

Because permissive licences allow proprietary derivatives, they're the default choice for start-ups building commercial services, vendor integration teams, and agencies embedding open libraries in client work. React.js is the canonical example: Facebook shipped it under MIT so that product teams anywhere could build proprietary apps on top without asking permission — and adoption exploded accordingly.

The trade-off is reciprocity. A permissive licence gives you no legal lever to force improvements back upstream. Sustaining the project then depends on community goodwill, healthy governance, or a parallel commercial offering. If you're a first-time maintainer staring at the fine print, choosealicense.com and GitHub's built-in licence picker will walk you through the options before you click "public".

## Copyleft: the GPL family

Copyleft licences — GPLv2, GPLv3, LGPL and AGPL — flip the deal. You get the same broad rights, but if you distribute a derivative work, it must be released under the same licence, source included. This "share alike" obligation is deliberate: it keeps improvements flowing back to the commons. The common metaphor is a viral clause — once your shipped product incorporates GPL code, the openness obligation spreads to the whole bundle you distribute.

The mechanics matter, so be precise about them:

- Obligations trigger on **distribution**, not use. You can modify GPL code internally forever without publishing anything. Ship it to a customer — as a binary, a device, a container image — and the source obligation lands.
- **LGPL** is the softer variant for libraries: you may link it into a proprietary application without relicensing your own code, provided users can swap in and relink updated versions of the library.
- **AGPL** closes the software-as-a-service loophole: letting users interact with the software over a network counts as distribution, so a SaaS product built on AGPL code owes its users the source.

The Linux kernel is GPLv2, which is why Android handset makers must publish their kernel modifications every time they release a firmware image — some learned this the hard way. Same story if you ship a router with modified GPL firmware: matching source must be made available. Copyleft rewards collaboration-heavy ecosystems — public-sector platforms, civic tech, and organisations like Signal, which keeps its core GPL precisely so its privacy claims stay independently inspectable.

## Mixing licences without getting burned

Real products combine dozens of dependencies, and not all licences coexist happily. The working rules of thumb:

- **MIT/BSD** combines with almost anything; just preserve attribution.
- **Apache 2.0** combines with MIT, other Apache code and GPLv3 — but not GPLv2, whose terms clash with Apache's patent provisions. (GPLv3 was written partly to fix this.)
- **GPLv3** code can absorb permissive code, but the combined binary you distribute must be GPL.
- **AGPL** combines with AGPL, and remember: network use counts as distribution.

Keep a compatibility matrix handy so nobody discovers a GPLv2 dependency sitting inside an Apache 2.0 codebase at the eleventh hour.

Some projects deliberately run two licence streams. MySQL and Qt offer their code under the GPL for the community and sell commercial licences to companies that want proprietary terms — a model that funds development while protecting openness goals. It only works if the steward holds the rights to relicense (more on that below) and is transparent about which features sit under which stream. MongoDB's shift to the Server Side Public License (SSPL) shows the same lever pulled defensively: a licence change designed to protect a business model from cloud providers reselling the product.

At the other extreme, CC0 and the Unlicense attempt to place work in the public domain, which suits datasets, code snippets and government artefacts where even attribution requirements create friction. "Attempt" is the honest word: some jurisdictions restrict abandoning copyright — moral rights, in particular, often can't be waived — so CC0 includes a fallback licence for exactly that reason.

Which leads to the international wrinkle generally: copyright terms, moral rights and patent scope differ across jurisdictions. EU database rights and Australian Crown copyright can both complicate reuse in ways a US-centric licence summary won't mention. This is why global teams stick to OSI-approved licence texts — they've been examined across many legal systems — and document governing law in their NOTICE files.

## Contributor agreements and choosing for your context

Once outsiders contribute, ownership fragments: every contributor holds copyright in their patch. Contributor Licence Agreements (CLAs) fix this by having contributors grant the maintainer rights to relicense, defend, or dual-license their contributions — which is what makes dual licensing and future licence changes legally possible at all. Distinguish individual from corporate CLAs, and check that the person signing a corporate CLA actually has authority to bind their employer. Many projects pair or replace CLAs with the lighter-weight Developer Certificate of Origin (DCO), a signed-off-by line certifying the contributor has the right to submit the code; either way, you want an audit trail.

Choosing a licence is a cross-functional decision, not a checkbox. Start from goals: are you optimising for adoption, reciprocity, revenue, or community trust? The quick flow — need maximum adoption, go permissive; need guaranteed sharing, pick copyleft; need revenue plus openness, explore dual licensing. A worked example: a government agency building a records platform wants vendor fixes funded by taxpayers to stay public, so its open-source program office (OSPO) recommends GPLv3, legal sets up DCO-plus-CLA contribution intake, and the comms team briefs suppliers on what they're signing up for. Documenting that rationale now prevents a heated argument three years later when a new contractor joins. Involve legal counsel, community tech-leads, security engineers and product managers early — a licence choice is like a roommate agreement, and if you skip the awkward conversation about chores and guests, you'll have it later, angrier, with the mess already on the floor.

## Staying compliant — and who gets paid to care

Compliance is a process, not an event. Maintain a software bill of materials (SBOM) so you can prove which licences are in your build, and wire licence scanners into CI so incompatible combinations fail fast rather than surface in an audit. Record every redistribution moment — shipped binaries, published container images, a SaaS endpoint incorporating AGPL code — and keep source archives, NOTICE files and third-party attributions ready to go. Tools like FOSSA, OSS Review Toolkit and GitHub's dependency review do the tedious parts once configured. Companies have paid real settlements for ignoring GPL notices, so treat "we'll fix the licensing post-launch" as the red flag it is.

> Licence compliance is like flossing: tedious, easy to skip while everything seems fine, and the neglect only announces itself as an expensive, painful audit.

This work is a genuine career path. OSPO analysts — typically one or two per 50–80 engineers in large organisations — usually arrive after five to seven years in software engineering, developer advocacy or technology law, which is what gives them credibility with both coders and lawyers. Entry routes include community contributors who've earned maintainer trust, compliance interns rotating through procurement, and dual STEM-law graduates hired into tech policy teams. The people who thrive are detail-obsessed, diplomatic and values-driven — able to translate legal nuance for technologists without flattening it. From analyst, the ladder runs to OSPO manager coordinating licence strategy across business units, then director or VP roles stewarding ecosystem partnerships.

The takeaway: licence selection is a strategic lever, not paperwork. It signals how you invite collaboration, how you protect contributors, and — when projects touch cultural knowledge, as later sections of this part explore — how you honour data sovereignty commitments. Teams that understand reciprocity obligations, international quirks, CLAs and dual licensing can design contribution models that sustain trust with communities, customers and partners for the long haul.
