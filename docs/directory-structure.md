# Project Directory Structure

This document describes the layout of the repository and the purpose of each directory.

```
/
├── cmd/               # Go command-line tools
├── content/           # Course modules and slide sources
│   ├── part-01/
│   ├── part-02/
│   ├── part-03/
│   ├── part-04/
│   ├── part-05/
│   ├── part-06/
│   ├── part-07/
│   └── part-08/
├── assets/            # Shared images, audio, and other static assets
├── scripts/           # Helper scripts for automation or local setup
├── textbook/          # Generated LaTeX textbook and PDFs from course source
├── docs/              # Design and planning documentation
├── internal/          # Non-exported Go packages
├── pkg/               # Reusable Go packages
├── envsetup.sh        # Development environment bootstrap script
├── README.md          # Project overview
└── ...                # GitHub workflows and other configuration
```

The `content` directory holds all learning material organised by part. HTML slide source, narratives and exercises for each part live under their respective subdirectory.

Generated learner output is written under `output/`, which is ignored by git. The LaTeX textbook project is generated into `textbook/` so the source and PDFs can be reviewed directly from the repository.

Use `assets` for images, audio files, and any other media shared across parts. Automation and utility scripts belong in `scripts`.

Go source code is split between `cmd` for command-line binaries, `pkg` for shared libraries, and `internal` for packages that should not be imported outside this repository.

All additional docs—including this file—live under `docs`.
