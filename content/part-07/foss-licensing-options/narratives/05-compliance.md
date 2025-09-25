# Staying compliant in practice

Maintaining compliance requires disciplined processes. Developer advocates teach engineers how to attribute dependencies within documentation and user interfaces. Build engineers automate software bill of materials (SBOM) generation to prove which licences are in use, then wire scanners into CI so incompatible combinations fail fast. Licence compliance is a bit like flossing—boring when everything seems fine, but skipping it leads to painful audits later.

Record every redistribution moment: shipping binaries, publishing container images, even offering a SaaS endpoint that incorporates AGPL code. Keep source archives ready, bundle NOTICE files and track third-party attributions in release notes. Several high-profile companies have paid settlements for overlooking these basics, so treat “we’ll fix it post-launch” as a red flag. Tools like FOSSA, OSS Review Toolkit or GitHub’s dependency review can save hours once configured.

Finally, coordinate legal artifacts. Store signed contributor licence agreements (CLAs), Developer Certificate of Origin (DCO) acknowledgements and export-control assessments alongside your SBOM. That unified paper trail makes due diligence for clients, investors or acquirers straightforward—and shows professional maturity in handling open-source obligations.
