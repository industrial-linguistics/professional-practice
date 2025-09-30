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

## Startup runway vs operational overhead
- **Months 0–12:** Prioritise velocity, keep the team shipping features and leverage managed services with generous free tiers.
- **Year 2:** As usage grows, weigh predictable reserved cloud spend against the fixed costs of leased hardware and support staff.
- **Year 3+:** Hybrid patterns emerge—latency-sensitive workloads or data residency demands may justify colocated gear, while the rest stays cloud-native.

---

## Serverless first: when it shines
- No infrastructure patching, and scaling is automatic—perfect for small teams without SRE coverage.
- Pay-per-use keeps experimentation cheap while you iterate on product-market fit.
- Lock-in risk is mitigated by designing around open APIs and exporting data regularly.

---

## Managed cloud services: middle ground
- Managed Kubernetes, database services and VDI stacks offload maintenance but still offer configuration control.
- Use infrastructure as code to keep portability—document the baseline so you can recreate it elsewhere.
- Factor in support plans; the first pager still belongs to your team even if the provider handles hardware.

---

## Containers or self-managed: read the fine print
- Containers demand observability, image pipelines, security scanning and registry hygiene—skills many pre-Series A teams lack.
- Self-hosting can cut per-unit costs once workloads stabilise, but only if utilisation stays high and change frequency slows.
- Budget for redundant hardware, spares, remote hands at the data centre and compliance audits.

---

## Free tiers and startup credits
- AWS Activate, Azure for Startups and Google Cloud credits can cover six figures of spend—plan workloads to maximise the runway.
- Track expiry dates and graduation thresholds; sudden bills post-credit are a common failure mode.
- Mix in SaaS with generous free tiers (Cloudflare, Auth0, Notion) to avoid burning credits on commodity services.

---

## Questions before jumping to containers
- Do we have repeatable CI/CD with automated tests and security scanning in place?
- Can we monitor, patch and respond to incidents 24/7 without burning out a three-person engineering team?
- Are there regulatory or customer requirements that truly block managed services?

---

## Decision checkpoints
- Reassess architecture at each funding milestone—seed, Series A, Series B—to confirm the stack matches burn rate and talent.
- Run total cost of ownership models that include people, tooling, vendor support and opportunity cost of slower delivery.
- Prototype exit ramps: document how to move a workload between serverless, managed and self-hosted so switching is a deliberate move, not a panic.

---
