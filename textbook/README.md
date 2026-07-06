# IT Professional Practice Textbook

This directory contains the generated LaTeX textbook project for the course.
It is generated from `content/part-*/topic/slides.html` and `narratives/` by
`scripts/build_textbook.py`.

Build both student-print and Amazon print-on-demand PDFs with:

```bash
make -C textbook
```

Outputs:

- `textbook/main.pdf`: A4 PDF for student printing.
- `textbook/main-amazon.pdf`: 6x9 inch PDF for Amazon KDP-style print-on-demand.

Do not edit generated chapter files directly; edit course source and rebuild.
