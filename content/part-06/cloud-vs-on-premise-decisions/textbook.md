"Should we be in the cloud or on-premise?" sounds like one decision. It is actually four: where your applications run, where your data lives, how your networking works and who provides identity — and the right answer can differ per layer. A startup might run its product on serverless functions, keep customer data in a managed database, and still end up with a rack of colocated hardware for one latency-sensitive workload. Note also that "on-premise" in 2026 rarely means a server closet you wire yourself; it usually means renting space and power in a professional data centre (colocation) or vendor-managed edge appliances. The decision facing Sarah's team is not a binary but a portfolio.

Before going further, four bits of vocabulary you will hear constantly. **SaaS, PaaS and IaaS** — software, platform and infrastructure as a service — offer progressively more control and, in exact proportion, more responsibility. **SRE** (site reliability engineering) is the discipline of keeping services available through automation and operational rigour; it matters here because most architectures quietly assume you employ some. **Colocation versus on-premise** is the rented-rack versus own-building distinction above. **Reserved instances versus pay-as-you-go** is the cloud pricing trade: commit to long-term usage for discounts, or pay on demand for flexibility.

## Runway sets the architecture

The honest driver of this decision at a startup is not technology preference but runway. In months zero to twelve, velocity beats everything: use managed services with generous free tiers, keep the team shipping features, and do not hire for infrastructure you don't have. A senior reliability specialist can cost more than an early startup's entire infrastructure budget before tooling and on-call loading, so choose architectures that do not need one yet. By year two, finance wants predictability, and the comparison between reserved cloud spend and the fixed costs of leased hardware becomes worth doing properly, informed by real utilisation curves. From year three onward, hybrid patterns emerge legitimately: latency SLAs or data-residency demands may justify colocated gear for specific workloads while everything else stays cloud-native.

## Serverless first, and when it shines

For a small team without SRE coverage, serverless is a gift: no patching, no capacity planning, automatic scaling, and a bill proportional to use. A food-delivery beta with a hundred testers might cost $50 a month in functions and storage, instead of thousands in idle servers sized for a launch that hasn't happened. That pricing keeps experimentation cheap precisely when you are still iterating toward product-market fit.

The trade-off is vendor coupling, and the mitigation is discipline rather than avoidance: design around open APIs, export your data on a schedule, and occasionally rehearse replaying it into an alternative service so the exit remains real rather than theoretical.

Managed cloud services are the nearby middle ground when you outgrow simple functions — managed Kubernetes, managed databases, even virtual desktops — offloading hardware, network and backup maintenance while leaving you configuration control, ideally expressed as infrastructure as code so the setup is reproducible. Read the shared-responsibility fine print, though: even with a support plan, the first pager for misconfigurations and application bugs still belongs to your team.

A rough decision helper for the impatient:

```
Need a usable prototype in under 5 minutes?
  yes → stay serverless / SaaS
Team smaller than 3 engineers?
  yes → lean on managed services
Strict compliance or data residency?
  yes → plan a hybrid / colocation footprint
  no  → keep optimising the cloud setup
```

## Containers: deceptively complex

Kubernetes deserves its own warning label. Containers promise cost control and portability, but the platform demands observability, image pipelines, vulnerability scanning, registry hygiene and a cluster-upgrade routine — skills most pre-Series A teams simply don't have. If you adopt it, treat the platform as a product: budget real time for upgrades, policy automation and failure testing. Otherwise you're not removing risk from AWS; you're relocating it into your own unfinished build pipeline. It's like deciding to roast your own coffee beans before you've worked out the office coffee machine.

Ask four questions before jumping. Do we have repeatable CI/CD with automated tests and security scanning? Can we monitor, patch and respond to incidents around the clock without burning out three engineers? Is there a regulatory or customer requirement that genuinely blocks managed services? And is the on-call plan real? If the "rotation" is Sarah glancing at her phone during dinner, the honest answer to all of the above is no.

Self-managed infrastructure gets the same scepticism with bigger numbers. Self-hosting can cut per-unit costs once workloads stabilise — but only if utilisation stays high and your rate of change slows down. Before declaring savings, price in redundant hardware, spares, remote-hands contracts at the data centre and the compliance audits you now host yourself. And document the new shared-responsibility reality: your team owns patching, access reviews, backups and capacity upgrades, end to end, forever.

## Free tiers and the credits cliff

Startup credit programs — AWS Activate, Azure for Startups, Google Cloud credits — can cover six figures of spend and materially shape this whole decision. Treat them as an asset with a maturity date: catalogue every credit, its expiry and its eligible workloads. AWS Activate credits, for instance, expire after two years *or* when you raise a Series A, whichever comes first. Mix in services with genuinely generous free tiers — Cloudflare's CDN, Auth0's 7,000-user tier, Notion's personal plan — so you're not burning credits on commodity plumbing.

> The classic failure mode is the "oh no, we're not in the free tier any more" invoice: credits lapse silently, the architecture was designed around free compute, and a five-figure bill ruins a founder's Tuesday. Set billing alerts and an expiry calendar on day one, not after the shock.

## Managing risk in every model

Whichever mix you land on, three disciplines travel with you. First, backups: serverless databases still need export jobs, managed services deserve cross-region replicas, and colocated gear needs off-site copies — "the provider handles it" is a hope, not a policy. Second, exit ramps: beyond raw data dumps, capture infrastructure as code, schema migrations and benchmarks of replacement services, so moving a workload between serverless, managed and self-hosted is a deliberate move rather than a panic. Third, a written shared-responsibility matrix per model, naming who owns identity, patching, incident response and security testing — because in every model it's somebody, and ambiguity is how gaps ship to production.

Reassess the whole portfolio at each funding milestone — seed, Series A, Series B — checking that the architecture still matches burn rate and the talent you can actually hire. Run total-cost-of-ownership models that include people, tooling, vendor support and the opportunity cost of slower delivery, not just the invoice. The recurring mistakes are well documented: over-engineering with bespoke Kubernetes before demand is validated, ignoring data-transfer and egress costs between regions, and assuming "cloud = infinite scale" without budgets, guardrails and auto-scaling limits.

## How it plays out

A composite case makes the trajectory concrete. Company X launched on serverless functions with three engineers and reached a million users before adopting managed Kubernetes for its steady-state workloads. By year four — ten million users — it added edge servers in two colocated facilities to meet latency SLAs, while everything else stayed in cloud services. Engineering headcount grew from three to fifteen, and tooling spend graduated from startup credits to negotiated enterprise contracts. No single "cloud versus on-prem" decision was ever made; the portfolio evolved as scale, money and skills allowed. That is what good looks like.

Your practical next steps mirror what a founding engineer would do this week: model 12–24 months of costs in the AWS, Azure and GCP pricing calculators under different growth assumptions; switch on billing alerts and anomaly detection so engineering and finance see the same numbers; and write down the current architecture assumptions, the responsibility matrix and the exit criteria for each workload. The document matters more than the diagram — it is what turns the next migration from an emergency into a checkpoint.
