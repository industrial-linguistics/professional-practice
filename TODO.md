# To-do 

### General

- [x] Clean up the tables and dot points in the README so that they are in proper markdown format. They are in a mixture of lines, unicode dotpoints, tab separated texts and so on

- [x] Create a separate to-do list file with everything that was in the README.md file (and remove it from README.md)

- [x] Create an `envsetup.sh` file with the necessary software that we will use for the pipeline
- [x] Update `index.html` whenever the pipeline produces new artifacts

**NOTE:** Each part should highlight relevant job roles, typical seniority levels, entry pathways, suitable personality traits, proportions of such roles in organisations and likely career progressions.

### Content to be created

Each part of the course requires its own learning objectives, slides,
narratives and quiz questions. The overall workflow for a part is:

1. Outline topics and objectives.
2. Create to-do list items for each topic to draft slides and write narratives.
3. Prepare quiz questions.

Use the checklist below to track progress for each part.

#### Part 1 – ITIL Foundations
- [x] Outline objectives and key topics
- [x] Create to-do list items for each topic to draft slides and write narratives
- [x] Draft slides and narrative: Overview of ITIL 4 and why it matters
- [x] Draft slides and narrative: Service value chain and continual improvement
- [x] Draft slides and narrative: Incident vs request fulfilment workflows
- [x] Draft slides and narrative: Escalation paths and support tiers (L1/L2/L3)
- [x] Draft slides and narrative: Major incident management drill
- [x] Draft slides and narrative: ServiceNow as an ITIL visual guide
- [x] Draft slides and narrative: Job roles across the service lifecycle
- [x] Create quiz questions

#### Part 2 – ITIL Deep Dive
- [x] Outline objectives and key topics
- [x] Create to-do list items for each topic to draft slides and write narratives
- [x] Draft slides and narrative: Service level agreements, OLAs and KPIs
- [x] Draft slides and narrative: Change enablement vs release management
- [x] Draft slides and narrative: Problem management techniques for root cause analysis
- [x] Draft slides and narrative: Building and maintaining a configuration management database (CMDB)
- [x] Draft slides and narrative: Continual improvement frameworks and maturity assessments
- [x] Draft slides and narrative: Metrics and reporting dashboards for process performance
- [x] Create quiz questions

#### Part 3 – High-Velocity Delivery
- [x] Outline objectives and key topics
- [x] Create to-do list items for each topic to draft slides and write narratives
 - [x] Draft slides and narrative: DORA metrics and DevOps performance measurement
 - [x] Draft slides and narrative: Trunk-based development vs feature branching strategies
 - [x] Draft slides and narrative: CI/CD pipeline design principles and implementation
- [ ] Draft slides and narrative: SRE error budgets and service level objectives
- [ ] Draft slides and narrative: GitHub Actions workflows and automation
- [ ] Draft slides and narrative: DevOps, SRE and platform engineering career paths
- [ ] Create quiz questions

#### Part 4 – Blameless RCA & Continuous Improvement
- [ ] Outline objectives and key topics
- [ ] Create to-do list items for each topic to draft slides and write narratives
- [ ] Create quiz questions

#### Part 5 – Vendor/MSP & CRM Lifecycle
- [ ] Outline objectives and key topics
- [ ] Create to-do list items for each topic to draft slides and write narratives
- [ ] Create quiz questions

#### Part 6 – Start-ups & Small-Biz IT
- [ ] Outline objectives and key topics
- [ ] Create to-do list items for each topic to draft slides and write narratives
- [ ] Create quiz questions

#### Part 7 – Open-Source & Indigenous Digital Sovereignty
- [x] Outline objectives and key topics
- [ ] Create to-do list items for each topic to draft slides and write narratives
- [ ] Create quiz questions

#### Part 8 – Project Studio and Presentations
- [ ] Outline objectives and key topics
- [ ] Create to-do list items for each topic to draft slides and write narratives
- [ ] Create quiz questions


### Legislation

There are a few things that IT people need to know about Australian legislation.
	
- Aus. Privacy Act 1988 (especially APP 11 on security)
- Critical Infrastructure Act 2018 – SLAs can hinge on it for some clients
- EU GDPR
- China's PIPL
These need to go into week 5 when talking about contract SLAs I guess. Unless they need a separate week?

### Rendering pipeline

Each part is rendered separately. We should have intelligent GitHub workflows so that we can automate the whole process, but only do the minimal amount of audio re-rendering (and consequential other re-rendering) when things change.

- [ ] **Set up automation workflow**
  - Configure GitHub Actions to trigger the build process.
  - Ensure minimal re-rendering by checking for changes in source content before rebuilding assets.
- [ ] **Narration to audio**
  - For each slide, send the text to ElevenLabs (include preceding/following sentences for context).
  - Save the generated audio file using a checksum of `(normalized text, context, voice ID)`.
- [ ] **Audio caching**
  - Use the checksum as an S3 path and skip rendering when the file already exists.
- [ ] **Slide rendering**
  - Convert slide decks to PNG images using Marp.
- [ ] **Timing file generation**
  - Determine audio length for each slide.
  - Produce `slides.txt` entries (e.g., `file 'slide-01.png'`, `duration 5`).
- [ ] **Silent video creation**
  - Combine PNG slides into a silent video following `slides.txt`.
- [ ] **Audio concatenation**
  - Merge all slide audio segments into one track.
- [ ] **Video/audio merge**
  - Combine the silent video and the concatenated audio into the final video.
- [ ] **Upload step**
  - Upload the final video to S3 and the chosen hosting platform.
- [ ] **Question format conversion**
  - Transform quiz questions into the required format for the learning platform.
- [ ] **E-learning package generation**
  - Package the videos and questions into SCORM or another e-learning format.
- [ ] **Automated test suite**
  - Build tests that transcribe the rendered audio and verify it matches the text source.
- [ ] **E-book generation**
  - Compile all parts into a single e-book (PDF and EPUB).
