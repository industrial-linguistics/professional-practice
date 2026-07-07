#!/usr/bin/env python3
"""Build the LaTeX textbook project from course HTML slides and narratives."""

from __future__ import annotations

import html
import re
import shutil
import subprocess
from pathlib import Path

from course_content import ROOT, Part, Slide, Topic, load_course, narrative_files


TEXTBOOK = ROOT / "textbook"
CHAPTERS = TEXTBOOK / "chapters"
FIGURES = TEXTBOOK / "figures"
AUDIT = TEXTBOOK / "audit"


INDEX_TERMS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("access control", ("access control", "attribute-based access control", "ABAC")),
    ("account executive", ("account executive",)),
    ("action items", ("action item", "action items")),
    ("AGPL", ("AGPL", "Affero GPL")),
    ("alert correlation", ("alert correlation", "correlate alerts", "correlated alerts")),
    ("Apache License", ("Apache 2.0", "Apache licence", "Apache license")),
    ("API", ("API", "APIs")),
    ("ARR", ("ARR", "annual recurring revenue")),
    ("asset inventory", ("asset inventory", "asset register")),
    ("audit trail", ("audit trail", "audit trails")),
    ("AWS", ("AWS", "Amazon Web Services")),
    ("AWS Lambda", ("AWS Lambda", "Lambda")),
    ("back-out plan", ("back-out plan", "backout plan", "rollback procedure")),
    ("backups", ("backup", "backups")),
    ("BANT", ("BANT",)),
    ("BDFL", ("BDFL", "benevolent dictator")),
    ("blameless post-mortems", ("blameless", "blameless post-mortem", "blameless post-mortems")),
    ("blue team", ("blue team", "blue-team")),
    ("BSD License", ("BSD", "BSD licence", "BSD license")),
    ("burn rate", ("burn rate",)),
    ("business continuity", ("business continuity",)),
    ("buying committee", ("buying committee", "buying committees")),
    ("BYOD", ("BYOD", "bring your own device")),
    ("CAB", ("CAB", "change advisory board")),
    ("CAC", ("CAC", "customer acquisition cost")),
    ("capstone", ("capstone",)),
    ("CARE principles", ("CARE", "CARE principles")),
    ("CASB", ("CASB", "cloud access security broker")),
    ("CDN", ("CDN", "content delivery network")),
    ("change enablement", ("change enablement",)),
    ("change failure rate", ("change failure rate",)),
    ("change management", ("change management", "change manager")),
    ("change record", ("change record", "change records")),
    ("change window", ("change window", "change windows")),
    ("churn", ("churn",)),
    ("CI/CD", ("CI/CD", "continuous integration", "continuous delivery")),
    ("CIO", ("CIO", "chief information officer")),
    ("CISO", ("CISO", "chief information security officer")),
    ("CLA", ("CLA", "contributor licence agreement", "contributor license agreement")),
    ("cloud credits", ("cloud credits", "credits cliff")),
    ("CMDB", ("CMDB", "configuration management database")),
    ("community governance", ("community governance", "governance model", "governance structures")),
    ("community manager", ("community manager", "community managers")),
    ("community tech lead", ("community tech-lead", "community tech lead", "tech-lead")),
    ("configuration item", ("configuration item", "configuration items")),
    ("consent", ("consent", "consent capture")),
    ("containers", ("container", "containers")),
    ("continual improvement", ("continual improvement", "continuous improvement")),
    ("copyleft", ("copyleft",)),
    ("corrective actions", ("corrective action", "corrective actions")),
    ("CRM", ("CRM", "customer relationship management")),
    ("CRM!account", ("account record", "account records")),
    ("CRM!contact", ("contact record", "contact records")),
    ("CRM!lead", ("lead record", "lead records", "qualified lead", "sales lead")),
    ("CRM!milestones", ("CRM milestone", "CRM milestones")),
    ("CRM!opportunity", ("opportunity record", "opportunity records", "opportunity stage", "opportunity stages", "opportunity progression")),
    ("CSAT", ("CSAT", "customer satisfaction")),
    ("CSM", ("CSM", "customer success manager")),
    ("cultural safety", ("cultural safety",)),
    ("customer success", ("customer success",)),
    ("data minimisation", ("data minimisation", "data minimization")),
    ("data protection impact assessment", ("DPIA", "data protection impact assessment")),
    ("data room", ("data room", "data rooms")),
    ("data sovereignty", ("data sovereignty", "Indigenous data sovereignty")),
    ("data steward", ("data steward", "data stewards")),
    ("DCO", ("DCO", "developer certificate of origin")),
    ("de-escalation", ("de-escalation", "de-escalate", "de-escalating")),
    ("DevOps", ("DevOps",)),
    ("DevOps engineer", ("DevOps engineer", "DevOps engineers")),
    ("disaster recovery", ("disaster recovery",)),
    ("discovery call", ("discovery call", "discovery calls")),
    ("distributed tracing", ("distributed tracing", "tracing")),
    ("DKIM", ("DKIM",)),
    ("DNS", ("DNS", "domain name system")),
    ("DORA metrics", ("DORA", "DORA metrics")),
    ("DORA metrics!change failure rate", ("change failure rate",)),
    ("DORA metrics!deployment frequency", ("deployment frequency",)),
    ("DORA metrics!lead time for changes", ("lead time for changes",)),
    ("DORA metrics!MTTR", ("mean time to restore", "MTTR")),
    ("EDR", ("EDR", "endpoint detection and response")),
    ("Elastic Stack", ("Elastic Stack", "Elasticsearch")),
    ("error budget", ("error budget", "error budgets")),
    ("escalation path", ("escalation path", "escalation paths")),
    ("FAIR principles", ("FAIR", "FAIR principles")),
    ("feature branching", ("feature branch", "feature branches", "feature branching")),
    ("feature flags", ("feature flag", "feature flags")),
    ("FinOps", ("FinOps",)),
    ("fishbone diagram", ("fishbone", "fishbone diagram", "fishbone diagrams")),
    ("five whys", ("five whys", "5 whys")),
    ("FOSS", ("FOSS", "free and open source")),
    ("fractional CTO", ("fractional CTO", "fractional CTOs")),
    ("GDPR", ("GDPR", "General Data Protection Regulation")),
    ("GitHub Actions", ("GitHub Actions",)),
    ("GitHub issues", ("GitHub issue", "GitHub issues")),
    ("git blame", ("git blame",)),
    ("Google Workspace", ("Google Workspace",)),
    ("GPL", ("GPL", "GNU GPL")),
    ("grep", ("grep",)),
    ("health score", ("health score", "health scores")),
    ("HIPAA", ("HIPAA",)),
    ("HubSpot", ("HubSpot",)),
    ("identity provider", ("identity provider", "identity providers")),
    ("incident commander", ("incident commander", "IC")),
    ("incident management", ("incident management",)),
    ("incident metrics", ("incident metrics",)),
    ("Indigenous data sovereignty", ("Indigenous data sovereignty", "data sovereignty")),
    ("ISO 27001", ("ISO 27001",)),
    ("ITIL", ("ITIL", "ITIL 4")),
    ("ITIL!change enablement", ("change enablement",)),
    ("ITIL!continual improvement", ("continual improvement",)),
    ("ITIL!incident management", ("incident management",)),
    ("ITIL!problem management", ("problem management",)),
    ("ITIL!service value chain", ("service value chain",)),
    ("ITSM", ("ITSM", "IT service management")),
    ("iwi", ("iwi",)),
    ("Jira Service Management", ("Jira Service Management", "JSM")),
    ("JSON logs", ("JSON logs", "JSON logging")),
    ("Kaizen", ("Kaizen",)),
    ("kaitiakitanga", ("kaitiakitanga",)),
    ("kaupapa Maori", ("kaupapa Maori", "kaupapa Māori")),
    ("KPI", ("KPI", "KPIs", "key performance indicator", "key performance indicators")),
    ("Kubernetes", ("Kubernetes",)),
    ("lead scoring", ("lead scoring",)),
    ("LGPL", ("LGPL",)),
    ("licence", ("licence", "licences", "license", "licenses")),
    ("localisation", ("localisation", "localization")),
    ("log aggregation", ("log aggregation", "log aggregator", "log aggregators")),
    ("low-code", ("low-code", "low code")),
    ("LTV", ("LTV", "lifetime value")),
    ("maintainer", ("maintainer", "maintainers")),
    ("major incident", ("major incident", "major incidents")),
    ("mana motuhake", ("mana motuhake",)),
    ("Maori", ("Maori", "Māori")),
    ("MDM", ("MDM", "mobile device management")),
    ("MEDDIC", ("MEDDIC",)),
    ("MFA", ("MFA", "multi-factor authentication")),
    ("Microsoft 365", ("Microsoft 365", "Microsoft 365 Business")),
    ("MIT License", ("MIT", "MIT licence", "MIT license")),
    ("MRR", ("MRR", "monthly recurring revenue")),
    ("MSP", ("MSP", "MSPs", "managed service provider", "managed service providers")),
    ("MTTR", ("MTTR", "mean time to restore", "mean time to recovery")),
    ("Net Promoter Score", ("NPS", "Net Promoter Score", "Net Promoter Scores")),
    ("no-code", ("no-code", "no code")),
    ("NRR", ("NRR", "net revenue retention")),
    ("OCAP", ("OCAP", "OCAP principles")),
    ("Okta", ("Okta",)),
    ("OLA", ("OLA", "OLAs", "operational level agreement", "operational level agreements")),
    ("open source", ("open source", "open-source")),
    ("Open Source Program Office", ("OSPO", "Open Source Program Office")),
    ("PCI DSS", ("PCI DSS",)),
    ("PDCA", ("PDCA", "Plan-Do-Check-Act")),
    ("permissive licence", ("permissive licence", "permissive licences", "permissive license", "permissive licenses")),
    ("PII", ("PII", "personally identifiable information")),
    ("Pipedrive", ("Pipedrive",)),
    ("platform engineering", ("platform engineering", "platform engineer", "platform engineers")),
    ("POC", ("POC", "proof of concept", "proof-of-concept")),
    ("post-mortem", ("post-mortem", "post-mortems", "postmortem", "postmortems")),
    ("Privacy Act", ("Privacy Act", "Australian Privacy Act")),
    ("problem management", ("problem management", "problem record", "problem records")),
    ("psychological safety", ("psychological safety",)),
    ("RACI", ("RACI",)),
    ("RCA", ("RCA", "root cause analysis")),
    ("RDS", ("RDS", "Relational Database Service")),
    ("red team", ("red team", "red-team")),
    ("release management", ("release management",)),
    ("remediation roadmap", ("remediation roadmap", "remediation backlog")),
    ("renewal", ("renewal", "renewals")),
    ("request ID", ("request ID", "request IDs", "correlation ID", "correlation IDs")),
    ("request fulfilment", ("request fulfilment", "service request", "service requests")),
    ("retention", ("retention",)),
    ("RFC", ("RFC", "request for change")),
    ("RFC process", ("RFC process", "RFCs")),
    ("RFP", ("RFP", "request for proposal")),
    ("risk register", ("risk register", "risk registers")),
    ("ROI", ("ROI", "return on investment")),
    ("RPO", ("RPO", "recovery point objective")),
    ("RTO", ("RTO", "recovery time objective")),
    ("runbook", ("runbook", "runbooks")),
    ("runway", ("runway",)),
    ("SaaS", ("SaaS", "software as a service")),
    ("Salesforce", ("Salesforce",)),
    ("sales engineer", ("sales engineer", "sales engineering")),
    ("SBOM", ("SBOM", "software bill of materials")),
    ("security baseline", ("security baseline", "security baselines")),
    ("Series A", ("Series A",)),
    ("Series B", ("Series B",)),
    ("serverless", ("serverless",)),
    ("service catalogue", ("service catalogue", "service catalog")),
    ("service credit", ("service credit", "service credits")),
    ("service desk", ("service desk",)),
    ("service level agreement", ("SLA", "SLAs", "service level agreement", "service level agreements")),
    ("ServiceNow", ("ServiceNow",)),
    ("shadow IT", ("shadow IT",)),
    ("SIEM", ("SIEM", "security information and event management")),
    ("SLO", ("SLO", "SLOs", "service level objective", "service level objectives")),
    ("solution engineer", ("solution engineer", "solution engineering")),
    ("SOCI Act", ("SOCI Act", "SOCI")),
    ("SOC 2", ("SOC 2", "SOC 2 Type II", "SOC Type II")),
    ("SPF", ("SPF",)),
    ("Splunk", ("Splunk",)),
    ("SRE", ("SRE", "site reliability engineering")),
    ("SRE engineer", ("SRE engineer", "site reliability engineer", "site reliability engineers")),
    ("SSO", ("SSO", "single sign-on", "single sign on")),
    ("support tiers", ("support tier", "support tiers", "L1", "L2", "L3")),
    ("taonga", ("taonga",)),
    ("te reo Maori", ("te reo Maori", "te reo Māori")),
    ("Te Hiku Media", ("Te Hiku", "Te Hiku Media")),
    ("technical success manager", ("technical success manager", "technical success managers")),
    ("tikanga", ("tikanga",)),
    ("Traditional Knowledge", ("Traditional Knowledge",)),
    ("trunk-based development", ("trunk-based development", "trunk based development")),
    ("UNDRIP", ("UNDRIP",)),
    ("usage-based pricing", ("usage-based pricing", "usage based pricing")),
    ("vendor evaluation", ("vendor evaluation", "vendor assessment", "vendor assessments")),
    ("vendor management", ("vendor management",)),
    ("virtual CIO", ("virtual CIO", "vCIO")),
    ("VPN", ("VPN",)),
    ("watermarking", ("watermarking",)),
    ("whakapapa", ("whakapapa",)),
    ("workflow", ("workflow", "workflows")),
    ("YAML", ("YAML",)),
)


def slug(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def tex_escape(value: str) -> str:
    value = (
        value.replace("\u00a0", " ")
        .replace("\u202f", " ")
        .replace("\u2009", " ")
        .replace("\u2011", "-")
        .replace("\ufe0f", "")
    )
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "≠": r"$\ne$",
        "≤": r"$\le$",
        "≥": r"$\ge$",
        "✅": r"[OK]",
        "⚠": r"[Warning]",
        "❌": r"[Fail]",
        "➜": r"$\rightarrow$",
        "↔": r"$\leftrightarrow$",
        "│": "|",
        "├": "|",
        "└": "`",
        "─": "-",
    }
    return "".join(replacements.get(ch, ch) for ch in value)


def smarten_double_quotes(value: str) -> str:
    """Convert prose double quotes to TeX opening/closing quote marks."""
    out: list[str] = []
    opening = True
    for ch in value:
        if ch == '"':
            out.append("``" if opening else "''")
            opening = not opening
        elif ch == "“":
            out.append("``")
            opening = False
        elif ch == "”":
            out.append("''")
            opening = True
        else:
            out.append(ch)
    return "".join(out)


def index_alias_pattern(alias: str) -> re.Pattern[str]:
    escaped = re.escape(alias)
    letters = [ch for ch in alias if ch.isalpha()]
    flags = 0 if letters and all(ch.isupper() for ch in letters) else re.IGNORECASE
    return re.compile(rf"(?<![\w/-]){escaped}(?![\w/-])", flags)


INDEX_PATTERNS = tuple(
    (entry, tuple(index_alias_pattern(alias) for alias in aliases))
    for entry, aliases in INDEX_TERMS
)


def index_entries_for_text(text: str, seen: set[str]) -> list[str]:
    plain = re.sub(r"`([^`\n]+)`", r"\1", text)
    plain = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", plain)
    plain = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", plain)
    entries: list[str] = []
    for entry, patterns in INDEX_PATTERNS:
        if entry in seen:
            continue
        if any(pattern.search(plain) for pattern in patterns):
            seen.add(entry)
            entries.append(rf"\index{{{tex_escape(entry)}}}")
    return entries


def normalise_code(value: str) -> str:
    replacements = {
        "\u2502": "|",
        "\u251c": "|",
        "\u2514": "`",
        "\u2500": "-",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2194": "<->",
        "\u2193": "v",
        "\u2191": "^",
        "\u279c": "->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u2260": "!=",
    }
    return "".join(replacements.get(ch, ch) for ch in value)


def tex_heading(value: str) -> str:
    return tex_escape(smarten_double_quotes(re.sub(r"\s+", " ", value).strip()))


def clean_generated() -> None:
    TEXTBOOK.mkdir(exist_ok=True)
    for path in [CHAPTERS, FIGURES, AUDIT]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
    for stale in [TEXTBOOK / "index.html"]:
        if stale.exists():
            stale.unlink()


def copy_topic_images(topic: Topic) -> None:
    src = topic.source_path / "images"
    if not src.exists():
        return
    dest = FIGURES / topic.part / topic.slug / "images"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def image_alt(slide: Slide, src: str) -> str:
    pattern = re.compile(
        rf"<img\b[^>]*src=[\"']{re.escape(src)}[\"'][^>]*>",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(slide.html)
    if not match:
        return slide.title
    alt_match = re.search(r"\balt=([\"'])(.*?)\1", match.group(0), re.DOTALL)
    if not alt_match:
        return slide.title
    return html.unescape(alt_match.group(2)).strip() or slide.title


def paragraph_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines()]


def tex_text_block(text: str) -> str:
    lines = paragraph_lines(text)
    out: list[str] = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            out.append(md_line(" ".join(paragraph)))
            out.append("")
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            out.append(r"\begin{itemize}[leftmargin=*]")
            out.extend(rf"\item {md_line(item)}" for item in bullets)
            out.append(r"\end{itemize}")
            out.append("")
            bullets.clear()

    for line in lines:
        if not line:
            flush_paragraph()
            flush_bullets()
            continue
        if line.startswith("- "):
            flush_paragraph()
            bullets.append(line[2:].strip())
        else:
            flush_bullets()
            paragraph.append(line)
    flush_paragraph()
    flush_bullets()
    return "\n".join(out).strip()


def is_title_slide(slide: Slide) -> bool:
    start = slide.html.split(">", 1)[0].lower()
    return 'data-kind="title"' in start or "data-kind='title'" in start or slide.n == 1


def narrative_to_book_prose(text: str) -> str:
    text = re.sub(r"(?im)^\s*Speaker\s+\d+:\s*", "", text)
    text = re.sub(r"\[[^\]]+\]\s*", "", text)
    text = re.sub(r"\bWelcome to\b", "This section begins with", text, flags=re.IGNORECASE)
    text = re.sub(r"\btoday\b", "this section", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""

    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs: list[str] = []
    current: list[str] = []
    for sentence in sentences:
        if not sentence:
            continue
        current.append(sentence)
        if len(" ".join(current)) >= 360:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return "\n\n".join(paragraphs)


def slide_key_points(slide: Slide) -> list[str]:
    points: list[str] = []
    seen: set[str] = set()
    title = re.sub(r"\s+", " ", slide.title).strip().lower()
    for raw in slide.text.splitlines():
        line = re.sub(r"\s+", " ", raw).strip(" -\t")
        if not line:
            continue
        if line.lower() == title:
            continue
        if line.startswith("Image:"):
            continue
        if len(line) > 170:
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        points.append(line)
    return points[:6]


def tex_itemize(items: list[str]) -> str:
    if not items:
        return ""
    lines = [r"\begin{itemize}[leftmargin=*]"]
    lines.extend(rf"\item {md_line(item)}" for item in items)
    lines.append(r"\end{itemize}")
    return "\n".join(lines)


def md_inline(text: str) -> str:
    """Convert inline markdown markers on already-TeX-escaped text."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\\emph{\1}", text)
    return text


def md_line(text: str) -> str:
    code_spans: list[str] = []

    def protect_code(match: re.Match[str]) -> str:
        code_spans.append(rf"\texttt{{{tex_escape(match.group(1))}}}")
        return f"@@CODESPAN{len(code_spans) - 1}@@"

    protected = re.sub(r"`([^`\n]+)`", protect_code, text)
    rendered = md_inline(tex_escape(smarten_double_quotes(protected)))
    for i, code in enumerate(code_spans):
        rendered = rendered.replace(f"@@CODESPAN{i}@@", code)
    return rendered


MD_IMAGE_RE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$")
MD_ORDERED_RE = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
MD_BULLET_RE = re.compile(r"^(\s*)[-*]\s+(.*)$")


def md_figure(alt: str, src: str, topic: Topic | None) -> str:
    if topic is None:
        return ""
    source = topic.source_path / src
    if re.match(r"^[a-z]+:", src) or src.startswith("/") or not source.exists():
        return ""
    rel = Path("figures") / topic.part / topic.slug / src
    return "\n".join(
        [
            r"\begin{figure}[htbp]",
            r"\centering",
            rf"\includegraphics[width=0.86\linewidth]{{{rel.as_posix()}}}",
            rf"\caption{{{tex_heading(alt or topic.title)}}}",
            r"\end{figure}",
        ]
    )


def markdown_to_tex(
    md: str,
    topic: Topic | None = None,
    seen_index_terms: set[str] | None = None,
) -> str:
    """Convert the authored-textbook markdown subset to LaTeX.

    Supported: ##/### headings, paragraphs, - and 1. lists (one nesting
    level), > asides, fenced code blocks, images, **bold**, *italic*,
    `code`. Anything fancier belongs in the generator, not the sources.
    """
    out: list[str] = []
    paragraph: list[str] = []
    quote: list[str] = []
    code: list[str] = []
    in_code = False
    # Each stack entry is (indent, environment name).
    list_stack: list[tuple[int, str]] = []
    seen = seen_index_terms if seen_index_terms is not None else set()

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(paragraph)
            out.extend(index_entries_for_text(text, seen))
            out.append(md_line(text))
            out.append("")
            paragraph.clear()

    def flush_quote() -> None:
        if quote:
            text = " ".join(quote)
            out.extend(index_entries_for_text(text, seen))
            out.append(r"\begin{quote}\small")
            out.append(md_line(text))
            out.append(r"\end{quote}")
            out.append("")
            quote.clear()

    def close_lists(indent: int = -1) -> None:
        while list_stack and list_stack[-1][0] >= indent >= 0 or (indent < 0 and list_stack):
            _, env = list_stack.pop()
            out.append(rf"\end{{{env}}}")
        if not list_stack:
            out.append("")

    def open_list(indent: int, env: str) -> None:
        options = "[leftmargin=*]" if not list_stack else ""
        out.append(rf"\begin{{{env}}}{options}")
        list_stack.append((indent, env))

    def handle_item(indent: int, env: str, item: str) -> None:
        flush_paragraph()
        flush_quote()
        while list_stack and list_stack[-1][0] > indent:
            _, closed = list_stack.pop()
            out.append(rf"\end{{{closed}}}")
        if list_stack and list_stack[-1][0] == indent and list_stack[-1][1] != env:
            _, closed = list_stack.pop()
            out.append(rf"\end{{{closed}}}")
        if not list_stack or list_stack[-1][0] < indent:
            open_list(indent, env)
        out.extend(index_entries_for_text(item, seen))
        out.append(rf"\item {md_line(item)}")

    for raw in md.splitlines():
        line = raw.rstrip()
        stripped = line.strip()

        if in_code:
            if stripped.startswith("```"):
                in_code = False
                out.append(r"\begin{CodeBlock}")
                out.append(normalise_code("\n".join(code)))
                out.append(r"\end{CodeBlock}")
                out.append("")
                code.clear()
            else:
                code.append(raw)
            continue

        if stripped.startswith("```"):
            flush_paragraph()
            flush_quote()
            close_lists()
            in_code = True
            continue

        if not stripped:
            flush_paragraph()
            flush_quote()
            close_lists()
            continue

        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            flush_paragraph()
            flush_quote()
            close_lists()
            level = len(heading.group(1))
            title = tex_heading(heading.group(2))
            command = "subsection" if level <= 2 else "subsubsection"
            out.append(rf"\{command}{{{title}}}")
            out.extend(index_entries_for_text(heading.group(2), seen))
            out.append("")
            continue

        image = MD_IMAGE_RE.match(stripped)
        if image:
            flush_paragraph()
            flush_quote()
            close_lists()
            figure = md_figure(image.group(1), image.group(2), topic)
            if figure:
                out.append(figure)
                out.append("")
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            close_lists()
            quote.append(stripped.lstrip("> ").strip())
            continue

        bullet = MD_BULLET_RE.match(line)
        if bullet:
            handle_item(len(bullet.group(1)), "itemize", bullet.group(2))
            continue
        ordered = MD_ORDERED_RE.match(line)
        if ordered:
            handle_item(len(ordered.group(1)), "enumerate", ordered.group(2))
            continue

        if list_stack:
            # Continuation line inside a list item.
            out.extend(index_entries_for_text(stripped, seen))
            out.append(md_line(stripped))
            continue

        flush_quote()
        paragraph.append(stripped)

    flush_paragraph()
    flush_quote()
    close_lists()
    if in_code and code:
        out.append(r"\begin{CodeBlock}")
        out.append(normalise_code("\n".join(code)))
        out.append(r"\end{CodeBlock}")
    return "\n".join(out).strip()


def pre_blocks(slide: Slide) -> list[str]:
    blocks = []
    for match in re.finditer(
        r"<pre><code(?:\s+[^>]*)?>(.*?)</code></pre>",
        slide.html,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        blocks.append(html.unescape(match.group(1)).strip("\n"))
    return blocks


def render_slide(
    topic: Topic,
    slide: Slide,
    *,
    include_heading: bool = True,
    seen_index_terms: set[str] | None = None,
) -> str:
    parts: list[str] = []
    seen = seen_index_terms if seen_index_terms is not None else set()
    if include_heading:
        parts.append(rf"\subsection{{{tex_heading(slide.title)}}}")
        parts.extend(index_entries_for_text(slide.title, seen))

    if slide.narration:
        prose = narrative_to_book_prose(slide.narration)
        if prose:
            parts.extend(index_entries_for_text(prose, seen))
            parts.append(tex_text_block(prose))
    else:
        points = slide_key_points(slide)
        if points:
            parts.append(tex_text_block("This section should be expanded from the following practice points."))
            for point in points:
                parts.extend(index_entries_for_text(point, seen))
            parts.append(tex_itemize(points))

    for src in slide.image_paths:
        if re.match(r"^[a-z]+:", src) or src.startswith("/"):
            continue
        source = topic.source_path / src
        if not source.exists():
            continue
        rel = Path("figures") / topic.part / topic.slug / src
        caption = image_alt(slide, src)
        parts.append(
            "\n".join(
                [
                    r"\begin{figure}[htbp]",
                    r"\centering",
                    rf"\includegraphics[width=0.86\linewidth]{{{rel.as_posix()}}}",
                    rf"\caption{{{tex_heading(caption)}}}",
                    r"\end{figure}",
                ]
            )
        )

    code_blocks = pre_blocks(slide)
    if code_blocks:
        parts.append(r"\paragraph{Example artifact.}")
        for code in code_blocks:
            parts.append(r"\begin{CodeBlock}")
            parts.append(normalise_code(code))
            parts.append(r"\end{CodeBlock}")
    else:
        points = slide_key_points(slide)
        if points and not is_title_slide(slide):
            parts.append(r"\paragraph{Practice checkpoints.}")
            for point in points:
                parts.extend(index_entries_for_text(point, seen))
            parts.append(tex_itemize(points))

    return "\n\n".join(part for part in parts if part.strip())


def render_topic(topic: Topic) -> str:
    copy_topic_images(topic)
    seen: set[str] = set()
    lines = [
        rf"\section{{{tex_heading(topic.title)}}}",
    ]
    lines.extend(index_entries_for_text(topic.title, seen))
    authored = topic.source_path / "textbook.md"
    if authored.exists():
        lines.append(markdown_to_tex(authored.read_text(encoding="utf-8"), topic, seen))
        return "\n".join(lines)
    slides = topic.slides
    if slides and is_title_slide(slides[0]):
        opener = render_slide(topic, slides[0], include_heading=False, seen_index_terms=seen)
        if opener:
            lines.extend([opener, ""])
        slides = slides[1:]
    elif topic.summary:
        lines.extend(index_entries_for_text(topic.summary, seen))
        lines.extend([tex_text_block(topic.summary), ""])

    for slide in slides:
        lines.append(render_slide(topic, slide, seen_index_terms=seen))
        lines.append("")
    return "\n".join(lines)


def render_part(part: Part) -> str:
    seen: set[str] = set()
    body = [
        "% Generated by scripts/build_textbook.py; edit content/ and rebuild.",
        rf"\chapter{{{tex_heading(part.title)}}}",
    ]
    body.extend(index_entries_for_text(part.title, seen))
    intro = ROOT / "content" / part.slug / "textbook-intro.md"
    if intro.exists():
        body.append(markdown_to_tex(intro.read_text(encoding="utf-8"), seen_index_terms=seen))
    elif part.summary:
        body.extend(index_entries_for_text(part.summary, seen))
        body.append(tex_text_block(part.summary))
    for topic in part.topics:
        body.append(render_topic(topic))
    return "\n\n".join(body).strip() + "\n"


def write_main(parts: list[Part]) -> None:
    includes = "\n".join(
        rf"\include{{chapters/{part.slug}-{slug(part.title)}}}" for part in parts
    )
    (TEXTBOOK / "main.tex").write_text(MAIN_TEX.replace("@@INCLUDES@@", includes), encoding="utf-8")
    (TEXTBOOK / "main-amazon.tex").write_text(
        "\\def\\amazontrimsize{}\n\\def\\omitcoverpage{}\n\\input{main.tex}\n",
        encoding="utf-8",
    )
    (TEXTBOOK / "Makefile").write_text(MAKEFILE, encoding="utf-8")
    (TEXTBOOK / "README.md").write_text(README, encoding="utf-8")


def write_chapters(parts: list[Part]) -> None:
    for part in parts:
        path = CHAPTERS / f"{part.slug}-{slug(part.title)}.tex"
        path.write_text(render_part(part), encoding="utf-8")


def write_audit(parts: list[Part]) -> None:
    topics = sum(len(part.topics) for part in parts)
    slides = sum(len(topic.slides) for part in parts for topic in part.topics)
    authored = sum(
        1
        for part in parts
        for topic in part.topics
        if (topic.source_path / "textbook.md").exists()
    )
    mismatches = []
    for part in parts:
        for topic in part.topics:
            narratives = narrative_files(topic.source_path)
            if len(narratives) != len(topic.slides):
                mismatches.append((topic, len(narratives)))
    (AUDIT / "open-issues.md").write_text(
        "# Textbook Open Issues\n\n"
        f"- Generated from {len(parts)} parts, {topics} topics and {slides} slides.\n"
        f"- {authored} of {topics} topics have authored `textbook.md` prose; the rest fall back to narration-derived text with practice checkpoints.\n"
        f"- {len(mismatches)} topics currently have slide/narrative count mismatches; "
        "see `docs/narrative-mismatch-audit.md`.\n"
        "- Authoring guidelines live in `docs/textbook-authoring-guidelines.md`.\n",
        encoding="utf-8",
    )
    (AUDIT / "style-notes.md").write_text(
        "# Style Notes\n\n"
        "- Preserve the practical, professional-practice teaching voice from the existing narratives.\n"
        "- Later passes should convert slide-fragment pacing into smoother chapter prose where useful.\n",
        encoding="utf-8",
    )
    (AUDIT / "slop-patterns.md").write_text(
        "# Slop Patterns\n\n"
        "- Avoid generic motivational bridge prose when expanding the slide-derived chapters.\n"
        "- Watch for service-marketing adjectives such as \"seamless\", \"holistic\" and \"transformative\"; replace them with the actual handoff, control or workflow.\n"
        "- Avoid \"journey\" unless it names a specific artefact such as a journey map; prefer request path, workflow, handoff or lifecycle.\n"
        "- Meta-openers like \"this chapter explores\" or \"it is important to note\" should become a concrete workplace problem or decision.\n",
        encoding="utf-8",
    )
    (AUDIT / "index-notes.md").write_text(
        "# Index Notes\n\n"
        f"- The generated index uses {len(INDEX_TERMS)} curated lookup terms and aliases.\n"
        "- Chapter, topic and subsection headings are not indexed automatically; headings are indexed only when they contain a curated lookup term.\n"
        "- The term list prioritises beginner lookup needs: acronyms, ITIL/DevOps/CRM practices, tools, roles, compliance frameworks, and culturally specific vocabulary.\n",
        encoding="utf-8",
    )


def build_pdf() -> None:
    subprocess.run(["make", "-C", str(TEXTBOOK)], check=True)


def build() -> None:
    clean_generated()
    parts = load_course()
    write_chapters(parts)
    write_main(parts)
    write_audit(parts)
    build_pdf()
    topics = sum(len(part.topics) for part in parts)
    slides = sum(len(topic.slides) for part in parts for topic in part.topics)
    print(f"Built LaTeX textbook with {topics} topics and {slides} slides")


MAIN_TEX = r"""\documentclass[11pt,openany]{book}
\ifdefined\amazontrimsize
  \usepackage[paperwidth=6in,paperheight=9in,margin=0.72in]{geometry}
\else
  \usepackage[a4paper,margin=2.6cm]{geometry}
\fi
\usepackage{fontspec}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{makeidx}
\usepackage{setspace}
\usepackage[nopatch=footnote]{microtype}
\usepackage{fvextra}
\usepackage{xcolor}
\usepackage{float}
\DefineVerbatimEnvironment{CodeBlock}{Verbatim}{breaklines=true,breakanywhere=true,fontsize=\small}
\makeindex
\setstretch{1.14}
\setcounter{tocdepth}{1}
\setlength{\emergencystretch}{3em}
\sloppy
\pagestyle{plain}
\hypersetup{
  pdftitle={IT Professional Practice},
  pdfauthor={Greg Baker},
  hidelinks
}
\title{IT Professional Practice\\\large A Practical Course Reader}
\author{Greg Baker}
\date{Draft edition}
\newif\ifcoverpage
\coverpagetrue
\ifdefined\omitcoverpage
  \coverpagefalse
\fi

\begin{document}
\ifcoverpage
\begin{titlepage}
\thispagestyle{empty}
\vspace*{0.12\textheight}
{\Huge\bfseries IT Professional Practice\par}
\vspace{1.2em}
{\Large A Practical Course Reader\par}
\vfill
{\large Greg Baker\par}
{\large Draft edition\par}
\end{titlepage}
\fi

\frontmatter
\tableofcontents
\mainmatter
@@INCLUDES@@
\backmatter
\cleardoublepage
\phantomsection
\addcontentsline{toc}{chapter}{Index}
{\footnotesize\raggedright\printindex}
\end{document}
"""


MAKEFILE = r"""TEX=main.tex
AMAZON_TEX=main-amazon.tex
PDF=main.pdf
AMAZON_PDF=main-amazon.pdf
LATEXMK=latexmk -xelatex -quiet -e '$$max_repeat=10'
BASE=$(basename $(TEX))
AMAZON_BASE=$(basename $(AMAZON_TEX))
CHAPTERS=$(wildcard chapters/*.tex)
FIGURES=$(shell find figures -type f 2>/dev/null)

all: $(PDF) $(AMAZON_PDF)

$(PDF): $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(TEX)
	makeindex $(BASE) >/dev/null || true
	$(LATEXMK) $(TEX)

$(AMAZON_PDF): $(AMAZON_TEX) $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(AMAZON_TEX)
	makeindex $(AMAZON_BASE) >/dev/null || true
	$(LATEXMK) $(AMAZON_TEX)

free-pdf: $(PDF)

amazon-pdf: $(AMAZON_PDF)

clean:
	latexmk -C $(TEX) || true
	latexmk -C $(AMAZON_TEX) || true
	rm -f $(BASE).idx $(BASE).ind $(BASE).ilg $(AMAZON_BASE).idx $(AMAZON_BASE).ind $(AMAZON_BASE).ilg

.PHONY: all free-pdf amazon-pdf clean
"""


README = """# IT Professional Practice Textbook

This directory contains the generated LaTeX textbook project for the course.
It is generated by `scripts/build_textbook.py`. The preferred source for each
topic is an authored `content/part-*/topic/textbook.md` (see
`docs/textbook-authoring-guidelines.md`); topics without one fall back to
narration-derived prose from `slides.html` and `narratives/`. Part openers
come from `content/part-*/textbook-intro.md` when present. Do not edit the
`.tex` files here directly — they are regenerated on every build.

Build both student-print and Amazon print-on-demand PDFs with:

```bash
make -C textbook
```

Outputs:

- `textbook/main.pdf`: A4 PDF for student printing.
- `textbook/main-amazon.pdf`: 6x9 inch PDF for Amazon KDP-style print-on-demand.

Do not edit generated chapter files directly; edit course source and rebuild.
"""


if __name__ == "__main__":
    build()
