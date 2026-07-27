#!/usr/bin/env python3
"""Build the saleable Part 1 incident-triage module as a SCORM 1.2 package."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from build_elearning import build as build_elearning
from course_content import ROOT, Topic, load_course


ELEARNING = ROOT / "output" / "elearning"
SCORM_OUTPUT = ROOT / "output" / "scorm"
SCORM_SOURCE = ROOT / "scorm" / "incident-triage"
PACKAGE_NAME = "it-professional-practice-incident-triage.zip"
TITLE = "IT Professional Practice — Incident Triage Lab"
VERSION = "1.0.2"
PASS_SCORE = 70
PART_SLUG = "part-01"
TOPIC_ORDER = [
    "overview",
    "value-chain",
    "incident-vs-request",
    "escalation-tiers",
    "major-incident-drill",
    "servicenow-visual-guide",
    "job-roles-lifecycle",
]

MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="IL.PROFESSIONAL_PRACTICE.INCIDENT_TRIAGE" version="{version}"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                      http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="ORG-1">
    <organization identifier="ORG-1">
      <title>{title}</title>
      <item identifier="ITEM-1" identifierref="RES-1" isvisible="true">
        <title>{title}</title>
        <adlcp:masteryscore>{pass_score}</adlcp:masteryscore>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES-1" type="webcontent" adlcp:scormtype="sco" href="index.html">
{files}
    </resource>
  </resources>
</manifest>
"""


def ordered_topics() -> list[Topic]:
    parts = {part.slug: part for part in load_course()}
    if PART_SLUG not in parts:
        raise SystemExit(f"Course part not found: {PART_SLUG}")
    by_slug = {topic.slug: topic for topic in parts[PART_SLUG].topics}
    missing = [slug for slug in TOPIC_ORDER if slug not in by_slug]
    if missing:
        raise SystemExit(f"Part 1 topic(s) missing: {', '.join(missing)}")
    return [by_slug[slug] for slug in TOPIC_ORDER]


def replace_lesson_data(page: str, payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace(
        "</", "<\\/"
    )
    pattern = re.compile(
        r'(<script id="lesson-data" type="application/json">).*?(</script>)',
        re.DOTALL,
    )
    page, count = pattern.subn(
        lambda match: f"{match.group(1)}{encoded}{match.group(2)}",
        page,
        count=1,
    )
    if count != 1:
        raise RuntimeError("Could not replace lesson-data payload")
    return page


def patch_next_topic_link(page: str, href: str, label: str) -> str:
    pattern = re.compile(
        r'<a id="next-topic" class="next-topic-button" href="[^"]+" hidden>'
        r".*?</a>",
        re.DOTALL,
    )
    replacement = (
        '<a id="next-topic" class="next-topic-button" '
        f'href="{html.escape(href, quote=True)}" hidden>'
        f"Next: <span>{html.escape(label)}</span></a>"
    )
    page, count = pattern.subn(replacement, page, count=1)
    if count != 1:
        raise RuntimeError("Could not replace next-topic link")
    return page


def patch_lesson_page(
    source: Path,
    destination: Path,
    next_href: str,
    next_title: str,
) -> None:
    page = source.read_text(encoding="utf-8")
    match = re.search(
        r'<script id="lesson-data" type="application/json">(.*?)</script>',
        page,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError(f"Lesson data missing from {source}")
    payload = json.loads(match.group(1))
    payload["nextTopic"] = {
        "title": next_title,
        "href": next_href,
        "part": (
            "Assessment"
            if next_href == "../../incident-triage.html"
            else "ITIL 4 Foundations"
        ),
    }
    page = replace_lesson_data(page, payload)
    page = patch_next_topic_link(page, next_href, next_title)
    page = page.replace(
        "</body>",
        '<script src="../../assets/scorm-runtime.js"></script>\n</body>',
        1,
    )
    page = page.replace(
        '<body class="lesson-page">',
        f'<body class="lesson-page" data-scorm-page="lesson" '
        f'data-topic="{html.escape(str(payload["topicPath"]), quote=True)}">',
        1,
    )
    destination.write_text(page, encoding="utf-8")


def copy_lessons(stage: Path, topics: list[Topic]) -> None:
    for index, topic in enumerate(topics):
        source = ELEARNING / PART_SLUG / topic.slug
        destination = stage / PART_SLUG / topic.slug
        if not (source / "index.html").exists():
            raise SystemExit(f"Generated lesson not found: {source}")
        shutil.copytree(source, destination)
        if index + 1 < len(topics):
            next_topic = topics[index + 1]
            next_href = f"../{next_topic.slug}/index.html"
            next_title = next_topic.title
        else:
            next_href = "../../incident-triage.html"
            next_title = "Incident Triage Lab"
        patch_lesson_page(
            source / "index.html",
            destination / "index.html",
            next_href,
            next_title,
        )


def lesson_cards(topics: list[Topic]) -> str:
    cards: list[str] = []
    for index, topic in enumerate(topics, start=1):
        audio_label = "Narrated" if topic.audio else "Transcript included"
        cards.append(
            '<a class="module-card" '
            f'data-topic="{html.escape(f"{PART_SLUG}/{topic.slug}", quote=True)}" '
            f'href="{PART_SLUG}/{html.escape(topic.slug, quote=True)}/index.html">'
            f'<span class="module-number">{index:02d}</span>'
            '<span class="module-card-copy">'
            f"<strong>{html.escape(topic.title)}</strong>"
            f"<small>{len(topic.slides)} slides · {audio_label}</small>"
            "</span>"
            '<span class="module-status" aria-label="Not yet complete">○</span>'
            "</a>"
        )
    return "\n".join(cards)


def hub_page(topics: list[Topic]) -> str:
    slide_count = sum(len(topic.slides) for topic in topics)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A narrated SCORM module for practical IT incident triage and escalation judgement.">
  <title>{html.escape(TITLE)}</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="assets/course.css">
  <link rel="stylesheet" href="assets/module.css">
</head>
<body class="module-home" data-scorm-page="hub">
  <header class="module-hero">
    <p class="eyebrow">IT Professional Practice · SCORM 1.2</p>
    <h1>Handle the queue before the queue handles you.</h1>
    <p class="module-lead">Learn the service-practice concepts, then triage five ambiguous workplace records under operational pressure.</p>
    <div class="module-facts" aria-label="Module facts">
      <span><strong>7</strong> narrated lessons</span>
      <span><strong>{slide_count}</strong> learner slides</span>
      <span><strong>5</strong> ticket scenarios</span>
      <span><strong>{PASS_SCORE}%</strong> pass mark</span>
    </div>
    <a id="resume-link" class="primary-action" href="{PART_SLUG}/{topics[0].slug}/index.html">Start the module</a>
  </header>

  <main class="module-main">
    <section class="module-intro" aria-labelledby="outcome-heading">
      <div>
        <p class="eyebrow">Learner outcome</p>
        <h2 id="outcome-heading">Make defensible first-call decisions.</h2>
      </div>
      <p>By the end, graduates and junior technologists should be able to classify incoming work, set a defensible initial priority, choose the next owner and write a useful first update—because professional service work starts with judgement, not ticket vocabulary.</p>
    </section>

    <section aria-labelledby="lessons-heading">
      <div class="section-heading">
        <div>
          <p class="eyebrow">Learn</p>
          <h2 id="lessons-heading">Service practice in seven short lessons</h2>
        </div>
        <p id="lesson-progress">0 of 7 lessons completed</p>
      </div>
      <div class="module-grid">
        {lesson_cards(topics)}
      </div>
    </section>

    <section class="lab-callout" aria-labelledby="lab-heading">
      <div>
        <p class="eyebrow">Apply</p>
        <h2 id="lab-heading">Incident Triage Lab</h2>
        <p>Work through five records. For each one, decide the record type, priority, next owner and first customer-facing update. The LMS receives your score, completion status and resume point.</p>
      </div>
      <a class="primary-action inverse" href="incident-triage.html">Open the lab</a>
    </section>

    <section class="resource-row" aria-labelledby="resources-heading">
      <div>
        <p class="eyebrow">Take back to work</p>
        <h2 id="resources-heading">Run it with a team</h2>
      </div>
      <p>The printable intake sheet and facilitator guide turn the simulation into an onboarding exercise or a structured team debrief.</p>
      <div class="resource-links">
        <a href="resources/intake-and-escalation-sheet.html">Open worksheet</a>
        <a href="resources/facilitator-guide.html">Open facilitator guide</a>
      </div>
    </section>
    <p class="module-disclaimer">Narration uses an AI-generated voice. ITIL® is a registered trademark of the PeopleCert group. This independent professional-practice module is not accredited by or affiliated with PeopleCert and does not include certification or an exam voucher.</p>
  </main>

  <footer class="module-footer">
    <span>Industrial Linguistics</span>
    <span>Version {VERSION}</span>
    <a href="mailto:gregb@industrial-linguistics.com">Support</a>
  </footer>

  <script src="assets/scorm-runtime.js"></script>
</body>
</html>
"""


def assessment_page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Five-ticket IT incident triage simulation.">
  <title>Incident Triage Lab | IT Professional Practice</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="assets/course.css">
  <link rel="stylesheet" href="assets/module.css">
</head>
<body class="lab-page" data-scorm-page="assessment">
  <header class="lab-topbar">
    <a href="index.html">← Module home</a>
    <span>Incident Triage Lab</span>
    <span id="case-counter">Case 1 of 5</span>
  </header>
  <main class="lab-shell">
    <section class="lab-brief">
      <p class="eyebrow">Assessment</p>
      <h1>Triage the live queue.</h1>
      <p>Choose the most defensible first action from the information available. You can retry the lab; the LMS records your latest score.</p>
      <div class="score-panel" aria-live="polite">
        <span>Current score</span>
        <strong id="score-value">0 / 100</strong>
      </div>
    </section>
    <section id="case-stage" class="case-stage" aria-live="polite"></section>
    <section id="result-panel" class="result-panel" hidden aria-live="polite"></section>
  </main>
  <script src="assets/scorm-runtime.js"></script>
  <script src="assets/incident-triage.js"></script>
</body>
</html>
"""


def worksheet_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Intake and escalation sheet | IT Professional Practice</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="../assets/module.css">
</head>
<body class="worksheet-page">
  <main>
    <p class="eyebrow">IT Professional Practice</p>
    <h1>Intake and escalation sheet</h1>
    <p>For each incoming record, make the first-call decision and preserve the evidence behind it. The label is not enough: record the field or sentence that justified your choice and the handoff that should happen next.</p>
    <table>
      <thead>
        <tr>
          <th>Record</th>
          <th>Type and evidence</th>
          <th>Initial priority and why</th>
          <th>Next owner or escalation</th>
          <th>First customer update</th>
        </tr>
      </thead>
      <tbody>
        <tr><th>1</th><td></td><td></td><td></td><td></td></tr>
        <tr><th>2</th><td></td><td></td><td></td><td></td></tr>
        <tr><th>3</th><td></td><td></td><td></td><td></td></tr>
        <tr><th>4</th><td></td><td></td><td></td><td></td></tr>
        <tr><th>5</th><td></td><td></td><td></td><td></td></tr>
      </tbody>
    </table>
    <section class="worksheet-prompts">
      <h2>Debrief</h2>
      <p>Which record contained the weakest evidence? What would you ask next?</p>
      <p>Which handoff created the greatest risk of delay or lost context?</p>
      <p>At what point would an incident commander or another escalation path become necessary?</p>
    </section>
    <p><a href="../index.html">Return to the module</a></p>
  </main>
</body>
</html>
"""


def facilitator_guide_page() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Facilitator guide | {html.escape(TITLE)}</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="../assets/module.css">
</head>
<body class="guide-page">
  <main>
    <p class="eyebrow">IT Professional Practice</p>
    <h1>Incident Triage Lab facilitator guide</h1>
    <p class="guide-lead">Use this guide for graduate onboarding, service-desk induction or a professional-practice class. The module works individually, but the strongest discussion comes from comparing two defensible first calls before revealing the recommended response.</p>

    <section>
      <h2>Outcome</h2>
      <p>By the end, learners should be able to classify incoming work, assign an initial priority, choose the next owner and write a useful first update using the evidence available.</p>
    </section>

    <section class="guide-grid">
      <div>
        <h2>Individual path · 45–60 minutes</h2>
        <ol>
          <li>Complete the seven narrated lessons.</li>
          <li>Print or open the intake and escalation sheet.</li>
          <li>Complete the five-ticket lab without external notes.</li>
          <li>Review any missed decisions and retry if the score is below {PASS_SCORE}%.</li>
        </ol>
      </div>
      <div>
        <h2>Team path · 75 minutes</h2>
        <ol>
          <li>Assign the overview, incident/request and escalation lessons as pre-work.</li>
          <li>Run each ticket as a three-minute table decision.</li>
          <li>Ask one group to defend priority and another to defend the first update.</li>
          <li>Reveal the course response and record what local policy would change.</li>
        </ol>
      </div>
    </section>

    <section>
      <h2>Debrief prompts</h2>
      <ul>
        <li>Which fact changed your priority decision?</li>
        <li>Where did seniority or urgency tempt you to bypass a control?</li>
        <li>What information belongs in the first update even before the cause is known?</li>
        <li>When does restoring service stop being enough and a problem record become necessary?</li>
        <li>Which local escalation rule should be added to your organisation's onboarding material?</li>
      </ul>
    </section>

    <section>
      <h2>LMS setup</h2>
      <ul>
        <li>Import the inner SCORM ZIP, not the outer store delivery bundle.</li>
        <li>Use the package's reported status and raw score, with a {PASS_SCORE}% pass mark.</li>
        <li>Allow repeat attempts if the module is being used for formative onboarding.</li>
        <li>Test launch, resume, completion and score in a learner account before assigning a cohort.</li>
      </ul>
    </section>

    <section>
      <h2>Boundaries</h2>
      <p>This is independent professional-practice training, not ITIL certification preparation. Replace the recommended priorities and escalation roles only when a documented local policy makes the alternative explicit. Do not weaken identity checks or evidence capture to make a scenario easier.</p>
    </section>
    <p><a href="../index.html">Return to the module</a></p>
  </main>
</body>
</html>
"""


def part_one_corpus(topics: list[Topic]) -> dict[str, object]:
    corpus = json.loads(
        (ELEARNING / "course-corpus.json").read_text(encoding="utf-8")
    )
    topic_slugs = {topic.slug for topic in topics}
    corpus["topics"] = [
        item
        for item in corpus.get("topics", [])
        if item.get("part") == PART_SLUG and item.get("topic") in topic_slugs
    ]
    corpus["slides"] = [
        item
        for item in corpus.get("slides", [])
        if item.get("part") == PART_SLUG and item.get("topic") in topic_slugs
    ]
    corpus["course"] = TITLE
    corpus["version"] = VERSION
    return corpus


def build_stage(stage: Path, topics: list[Topic]) -> None:
    shutil.copytree(ELEARNING / "assets", stage / "assets")
    course_js_path = stage / "assets" / "course.js"
    course_js = course_js_path.read_text(encoding="utf-8")
    local_qa_call = "\n  maybeEnableLocalQa();\n"
    if local_qa_call not in course_js:
        raise RuntimeError("Could not locate the local Q&A startup call")
    course_js_path.write_text(
        course_js.replace(
            local_qa_call,
            "\n  // Local browser-model Q&A is disabled in the portable SCORM build.\n",
            1,
        ),
        encoding="utf-8",
    )
    shutil.copytree(SCORM_SOURCE, stage / "assets", dirs_exist_ok=True)
    media = ELEARNING / "media" / PART_SLUG
    if media.exists():
        shutil.copytree(media, stage / "media" / PART_SLUG)
    copy_lessons(stage, topics)
    (stage / "resources").mkdir(parents=True, exist_ok=True)
    (stage / "index.html").write_text(hub_page(topics), encoding="utf-8")
    (stage / "incident-triage.html").write_text(
        assessment_page(), encoding="utf-8"
    )
    (stage / "resources" / "intake-and-escalation-sheet.html").write_text(
        worksheet_page(), encoding="utf-8"
    )
    (stage / "resources" / "facilitator-guide.html").write_text(
        facilitator_guide_page(), encoding="utf-8"
    )
    (stage / "course-corpus.json").write_text(
        json.dumps(part_one_corpus(topics), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )


def package(stage: Path) -> Path:
    files = sorted(path for path in stage.rglob("*") if path.is_file())
    file_tags = "\n".join(
        f'      <file href="{html.escape(path.relative_to(stage).as_posix(), quote=True)}"/>'
        for path in files
    )
    manifest = MANIFEST.format(
        version=VERSION,
        title=html.escape(TITLE),
        pass_score=PASS_SCORE,
        files=file_tags,
    )
    SCORM_OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = SCORM_OUTPUT / PACKAGE_NAME
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("imsmanifest.xml", manifest)
        for path in files:
            archive.write(path, path.relative_to(stage).as_posix())
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-elearning-build",
        action="store_true",
        help="Package the existing generated learner output without rebuilding it.",
    )
    args = parser.parse_args()
    if not args.skip_elearning_build:
        build_elearning()
    topics = ordered_topics()
    with tempfile.TemporaryDirectory(prefix="professional-practice-scorm-") as tmp:
        stage = Path(tmp)
        build_stage(stage, topics)
        destination = package(stage)
    slide_count = sum(len(topic.slides) for topic in topics)
    print(
        f"Built {destination.relative_to(ROOT)} "
        f"({len(topics)} lessons, {slide_count} slides, version {VERSION})"
    )


if __name__ == "__main__":
    main()
