---
marp: true
title: Cloud vs On-Premise Decisions
---

# Cloud vs On-Premise Decisions
*Finding the right fit from day zero to scale*

---

## What this decision really covers
- Application hosting, data storage, networking and identity services—each can live in SaaS, managed cloud or your own racks.
- Early-stage teams juggle credit offers, compliance expectations and the talent they can actually hire to run the stack.
- The "on-prem" option today often means co-lo racks or edge appliances managed by vendors, not a server closet you wire yourself.

---

## Glossary: terms you'll hear
- **SaaS / PaaS / IaaS:** Software, Platform and Infrastructure as a Service—progressively more control, but also more responsibility.
- **SRE (Site Reliability Engineering):** The discipline focused on keeping services available and reliable through automation and operations rigor.
- **Colocation vs on-premise:** Colocation rents space and power in a professional data centre; on-premise means hardware lives in your own facility.
- **Reserved instances vs pay-as-you-go:** Commit to long-term usage for discounts, or pay on-demand for flexibility.

---

## Startup runway vs operational overhead
- **Months 0–12:** Prioritise velocity, keep the team shipping features and leverage managed services with generous free tiers.
- **Year 2:** As usage grows, weigh predictable reserved cloud spend against the fixed costs of leased hardware and support staff.
- **Year 3+:** Hybrid patterns emerge—latency-sensitive workloads or data residency demands may justify colocated gear, while the rest stays cloud-native.

---

## Serverless first: when it shines
- No infrastructure patching, and scaling is automatic—perfect for small teams without SRE coverage.
- Pay-per-use keeps experimentation cheap while you iterate on product-market fit; a food delivery beta with ~100 users might run $50/month.
- Lock-in risk is mitigated by designing around open APIs, exporting data regularly and scripting data replays into alternative services.

---

## Managed cloud services: middle ground
- That serverless approach we just discussed? Managed services are the nearby cousin when you outgrow simple functions but still want rapid delivery.
- Managed Kubernetes, database services and VDI stacks offload maintenance but still offer configuration control when paired with infrastructure as code.
- Factor in support plans and runbooks; the first pager still belongs to your team even if the provider handles hardware, network and backups.

---

## Decision helper
```
Start here → Need usable prototype in <5 minutes?
        │               ├─ Yes → Stay serverless / SaaS
        │               └─ No
        ↓
Team smaller than 3 engineers?
        │               ├─ Yes → Lean on managed services
        │               └─ No
        ↓
Strict compliance / data residency?
        │               ├─ Yes → Plan hybrid / colocation footprint
        │               └─ No → Keep optimising cloud setup
```

---

## Containers: deceptively complex
- Containers demand observability, image pipelines, security scanning and registry hygiene—skills many pre-Series A teams lack.
- Treat the platform as a product: budget time for cluster upgrades, policy automation and chaos testing.
- It's like deciding to brew your own coffee when you haven't figured out how to work the office coffee machine yet.

---

## Self-managed infrastructure: read the fine print
- Self-hosting can cut per-unit costs once workloads stabilise, but only if utilisation stays high and change frequency slows.
- Budget for redundant hardware, spares, remote hands at the data centre and compliance audits before declaring savings.
- Document shared responsibility: your team now owns patching, access reviews, backups and capacity upgrades end-to-end.

---

## Free tiers and startup credits
- AWS Activate, Azure for Startups and Google Cloud credits can cover six figures of spend—plan workloads to maximise the runway.
- Track expiry dates and graduation thresholds; AWS Activate credits, for example, expire after two years or when you raise a Series A—whichever comes first.
- Mix in SaaS with generous free tiers (Cloudflare's free CDN, Auth0's 7,000-user tier, Notion's unlimited personal plan) to avoid burning credits on commodity services.
- Sudden bills post-credit are a common failure mode—also known as the "Oh no, we forgot we're not still in free tier" moment that ruins a founder's Tuesday.

---

## Questions before jumping to containers
- Do we have repeatable CI/CD with automated tests and security scanning in place?
- Can we monitor, patch and respond to incidents 24/7 without burning out a three-person engineering team?
- Are there regulatory or customer requirements that truly block managed services?
- Spoiler alert: if your "on-call rotation" is just Sarah checking her phone during dinner, the answer is no.

---

## Risk management across models
- Define backup cadences: serverless databases still need export jobs, managed services benefit from cross-region replicas, and co-lo gear needs off-site copies.
- Plan vendor exit ramps beyond raw data dumps—capture infrastructure as code, schema migrations and replacement service benchmarks.
- Clarify shared responsibility matrices so you know who owns identity, patching, incident response and security testing in each model.

---

## Decision checkpoints
- Reassess architecture at each funding milestone—seed, Series A, Series B—to confirm the stack matches burn rate and talent.
- Run total cost of ownership models that include people, tooling, vendor support and opportunity cost of slower delivery.
- Prototype exit ramps: document how to move a workload between serverless, managed and self-hosted so switching is a deliberate move, not a panic.

---

## Common mistakes to avoid
- Over-engineering early architecture with bespoke Kubernetes before validating demand.
- Ignoring data transfer and egress costs between regions or providers when forecasting spend.
- Assuming "cloud = infinite scale" without designing guardrails, budgets and auto-scaling limits.

---

## Case study snapshot
- "Company X" launched on serverless functions with a 3-person team, reaching 1M users before adopting managed Kubernetes for steady workloads.
- By year four and 10M users, they added edge servers in two colocated facilities to meet latency SLAs while keeping the rest in cloud services.
- Headcount grew from 3 to 15 engineers, and tooling spend shifted from credits to negotiated enterprise contracts.

---

## Practical next steps
- Experiment with AWS, Azure and GCP pricing calculators to model 12–24 month costs under different growth assumptions.
- Set up billing alerts and anomaly detection on day one so credits and budgets are visible to engineering and finance.
- Document current architecture assumptions, RACI charts and exit criteria before you scale into the next operating model.

---
