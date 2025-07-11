# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an educational content repository for "IT Professional Practice" - a university-level course covering professional skills and practices in the IT industry. The project aims to create comprehensive learning materials including presentations, narratives, and assessment content.

## Architecture & Structure

This repository is in early development stages and currently contains:
- **README.md**: Main project documentation with learning objectives, course structure, and implementation plans
- **raw-notes.txt**: Academic correspondence and detailed course planning discussions
- Planning for 8 course parts covering ITIL, DevOps, CRM, open source, and indigenous perspectives

## Content Development Approach

The course is designed around practical, industry-relevant skills:
- **ITIL 4 Foundations**: Service management, incident handling, change management
- **DevOps & DORA metrics**: Continuous delivery, performance measurement
- **CRM & Sales processes**: Understanding tech sales roles and customer management
- **Open source & Indigenous perspectives**: Community-driven development and data sovereignty
- **Small business IT**: Practical considerations for resource-constrained environments

## Development Tasks (from README.md)

Key items that need to be completed:
1. Clean up markdown formatting in README.md tables and lists
2. Create separate todo list file and remove from README.md
3. `envsetup.sh` created with required development tools
4. Develop content plans for each of the 8 course parts
5. Build automated rendering pipeline for presentations and video content

## Technology Stack (Planned)

The rendering pipeline will use:
- **ElevenLabs**: Text-to-speech for narration
- **Marp**: Markdown-to-slide conversion
- **FFmpeg**: Video processing and assembly
- **AWS S3**: Content storage and caching
- **GitHub Actions**: CI/CD automation

## Course Assessment Structure

- **A1**: Role-mapping reflection (20%)
- **A2**: Pipeline implementation + RCA (30%)
- **A3**: Capstone proposal & pitch (50%)

## Key Learning Resources

- ITIL 4 Foundation materials
- "Accelerate" by Forsgren, Humble & Kim
- Salesforce Trailhead CRM modules
- ServiceNow student sandbox
- GitHub Education Pack for CI/CD

## Working with TODO.md

When asked to "do the next item on the todo list":
1. Check TODO.md for the next uncompleted item (marked with `- [ ]`)
2. Use TodoWrite to track the task in progress
3. Complete the work following existing content patterns and guidelines
4. Mark the item as completed in TODO.md with `- [x]`
5. Update the TodoWrite status to completed

## Content Creation Guidelines

### Slides and Narratives Structure
- Content lives in `content/part-XX/topic-name/`
- Each topic has a `slides.md` file and `narratives/` directory
- Narratives are numbered `01-intro.md`, `02-topic.md`, etc.
- Follow the two-speaker conversational format established in existing content
- Aim for ~100 words per narrative (1 minute of speech)
- Reference `docs/narrative-guidelines.md` for style requirements

### Git Workflow Preferences
- Commit Claude-generated content with proper attribution to Claude
- Use descriptive commit messages that explain what was added/changed
- Credit format: "Co-Authored-By: Claude <noreply@anthropic.com>"

## Notes

This is an academic project focused on IT professional development rather than software engineering. The content emphasizes practical industry skills, role understanding, and professional practices rather than technical implementation details.