# Image review quality gates

Use these gates before registering or publishing any image-review candidate. A candidate that fails a gate stays out of the review database.

## 1. Choose the right composition

Write a short **composition decision** in `prompt.txt` before producing the candidate.

- Use native slide HTML/CSS for tables, grids, checklists, comparisons, timelines, matrices, and text in boxes. Keep semantic text as text instead of baking it into a PNG.
- Use Graphviz for a directed network or dependency map with enough nodes or connectors that automatic node sizing and edge routing help.
- Use Mermaid for a small, simple flowchart or sequence whose generated SVG is easy to inspect. Do not use it for a dense label-heavy layout merely because it is convenient.
- Use a charting library for quantitative charts.
- Use TikZ only for mathematical or technical geometry where TeX is already the appropriate canonical source. It is not the default for this HTML-first course.
- Use a generated raster image for an illustrative scene, realistic object, or visual metaphor. Do not put essential instructional text into a generated raster image.
- Use no added visual when the existing semantic slide already communicates the point more clearly.

If the material contains two distinct learning jobs, split it into adjacent slides instead of shrinking both into one crowded composition. If reviewer feedback clearly calls for a source-level HTML correction, implement and render the source correction rather than forcing it through the PNG installer.

## 2. Preserve the lesson content

Before editing, inventory the current slide's title, claims, examples, bullets, labels, and callouts, then read its narrative. Compare that inventory with the proposed slide and narrative.

Every useful item must be one of:

- still visible on the proposed slide;
- deliberately moved to a named adjacent slide; or
- adequately covered by the matching narrative, with the move recorded in `prompt.txt`.

Do not silently replace a useful content slide with a diagram that contains less information. A visual may supplement the original material on a second slide.

## 3. Inspect rendered geometry

Render the candidate and the full proposed slide at their final dimensions. Inspect both at 100% scale and as a whole slide.

- Every text run intended to be inside a box must be fully inside it, with visible padding on all four sides. Text must not touch or cross a border.
- No box, badge, label, or illustration may obscure text outside that element.
- No two unrelated labels or shapes may overlap.
- Every connector must attach to the intended node. Arrowheads and tails must be fully visible, must not end in empty space, and must not cross unrelated boxes or labels.
- The complete title, body, visual, captions, and controls must fit inside the slide frame without clipping or requiring scrolling.
- Check spelling and ambiguous letterforms at full resolution.

For deterministic HTML or SVG, also inspect computed geometry in the browser: child text bounds must fit within their declared box bounds; boxes must not intersect external text; the page must have no horizontal or vertical overflow and no console errors. Annotate layout boxes and connectors in the source when needed to make this check reliable.

## 4. Record QA evidence

The candidate's `prompt.txt` must include these headings:

- `Composition decision`
- `Content preservation`
- `Layout QA`

Under `Layout QA`, record the candidate and proposed-slide dimensions and state that text containment, external-text occlusion, connector endpoints, full-slide fit, spelling, and browser overflow were checked. Do not register the candidate if any check is unresolved.

The review bundle still requires `candidate.png`, `current-slide.png`, `proposed-slide.png`, and the prompt/spec text. Source HTML, SVG, Mermaid, Graphviz, or chart code should also be retained in the bundle so a reviewer comment can be corrected without reconstructing the diagram.
