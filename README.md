# IT Pofessional Practice

All the things you need to know to get started in your IT career. This
started as a plan for a university-level subject (which didn't go
ahead for other reasons).

You can browse through everything here for free to see if you like
it. If you are wanting to embed this into your corporate training (for
example, as part of a graduate entry program), I would encourage you
to talk to Greg (gregb@industrial-linguistics.com) about paying to get
a custom build done for your organisation -- this helps pay for the
development work for everyone.

# Learning objectives

LO#	Outcome (Bloom level unchanged)
1	Map and explain the operational, governance, sales and community roles that keep IT services humming.
2	Design and run a lightweight continuous‑delivery pipeline + blameless post‑incident review.
3	Compare and critique innovation & commercialisation pathways—corporate, open‑source, start‑up, social‑impact.
4	Evaluate and justify service‑management and delivery frameworks (ITIL 4, DevOps/SRE, SaaS, OSS, CRM).
5	Create an IT proposal that embeds ethics, sustainability and Indigenous data‑sovereignty principles end‑to‑end.


⸻

Part	Topic & Focus	Hands‑on / Evidence piece	LOs
1	ITIL 4 Foundations: service value chain, incident vs request, L1/L2/L3 roles, major‑incident drill. ServiceNow sandbox introduced purely as a visualiser of ITIL concepts (raise, escalate, close).	Log a P1 incident in the sandbox and annotate each role’s action.	1,4
2	ITIL 4 Deep Dive: change, problem, CMDB, SLA/SLO & reporting. Introduce ServiceNow change module + simple CMDB demo.	Draft a change‑request & walk it through CAB simulation; match each field to ITIL artefacts.	1,4
3	High‑Velocity Delivery: DORA metrics, trunk‑based DevOps, SRE error budgets. GitHub Actions 3‑step pipeline.	Build “hello‑world” pipeline → inject failure → collect lead‑time/MTTR baseline.	2,4
4	Blameless RCA & Continuous Improvement: post‑mortem culture, five‑whys, Kaizen vs corrective actions, linking RCA tickets back into ServiceNow & GitHub.	Run an RCA on the week‑3 failure; publish an action item & re‑run pipeline to show improvement.	2,4
5	Vendor/MSP & CRM Lifecycle: SDR → AE → CSM roles, Challenger Sales, renewals & churn, SLA hand‑off to ITSM. Salesforce Trailhead “CRM fundamentals” badge.	Map a six‑month pursuit in Salesforce (dummy org) and show touch‑points with ITIL change & incident.	1,3,4
6	Start‑ups & Small‑Biz IT: shoestring stacks, GenAI helpers, zero‑ops hosting, security trade‑offs.	Mini‑consult: audit a local café’s tech stack; recommend one practical change & justify with DORA/ITIL lens.	3,4
7	Open‑Source & Indigenous Digital Sovereignty: licensing, governance models, Maori case study, “community tech‑lead wearing many hats.”	Fork & re‑license a tiny OSS repo; draft a data‑sharing MoU for a First‑Nations NGO.	3,5
8	Project Studio and Presentations: teams finalise capstone; viva with panel of SRE, ServiceNow architect, Salesforce AE, and Indigenous digital‑inclusion advocate.	Capstone delivery & defence.	1‑5


⸻

# Assessment

A1: Role‑Mapping Reflection (individual)
20 %
Wk 4
Analyse a simulated major incident; identify every role you interacted with, what mattered and why. (ULO 1, 5)
A2: Tiny Pipeline + RCA (pairs)
30 %
Wk 8
Build the 3‑step GitHub Actions pipeline, trigger a forced failure, run a blameless post‑mortem, improve the metric. (ULO 2, 4)
A3: Capstone Proposal & Pitch (teams 4‑5)
50 %
Report Wk 12, viva Wk 13
Design an IT service for a real community org (indigenous or social‑impact). Must justify framework choices, innovation pathway, long‑term ethics & sustainability. Includes 10‑min board‑style pitch + questioning. (ULO 1‑5)


Task	Notes
A1 Role‑Mapping Reflection (20 %)	Now draws on ITIL weeks 1‑2 and CRM week 5.
A2 Tiny Pipeline + RCA (30 %)	Unchanged (weeks 3‑4 feed it).
A3 Capstone Proposal & Pitch (50 %)	Keep structure; students may optionally integrate Salesforce or ServiceNow elements to strengthen justification under ULO 4–5.

----

Key Resources
	•	ITIL 4 Foundation 
	•	Forsgren, Humble & Kim – Accelerate (e‑book)
	•	Salesforce Trailhead modules (CRM) – free
	•	GitHub Education Pack – CI/CD minutes
	•	ServiceNow “Student Path” sandbox
	•	Moodle book of short OSS & Indigenous data‑rights readings curated with community partners


# Slide Rendering Pipeline

Currently, none of the steps required to take this content and turn it into watchable video content or e-learning SCORM
files exists yet.

# Raw material

- `cmd/voicer/main.go` was pulled in from another project, and shows how to call the ElevenLabs API 

- `raw-notes.txt` some text that I wrote that is relevant to a few topics

# To-do 

### General

- [ ] Clean up the tables and dot points in the README so that they are in proper markdown format. They are in a mixture of lines, unicode dotpoints, tab separated texts and so on

- [ ] Create a separate to-do list file with everything that was in the README.md file (and remove it from README.md)

- [ ] Create an `envsetup.sh` file with the necessary software that we will use for the pipeline

### Content to be created

We need to create overviews and plans for each of the parts. What are
the lesson objectives? What sections will we have? What topics do we
need to cover? We then need to create to-do list items for each topic
that we need to create, including to-do items for creating
presentations, narratives and quiz questions.

- [ ] Part 1

- [ ] Part 2

- [ ] Part 3

- [ ] Part 4

- [ ] Part 5

- [ ] Part 6

- [ ] Part 7

- [ ] Part 8


### Legislation

There are a few things that IT people need to know about Australian legislation.
	•	Aus. Privacy Act 1988 (especially APP 11 on security)
	•	Critical Infrastructure Act 2018 – SLAs can hinge on it for some clients
	- EU GDPR
	- China's PIPL
	
These need to go into week 5 when talking about contract SLAs I guess. Unless they need a separate week?

### Rendering pipeline

Each part is rendered separately. We should have intelligent github workflows so that we can automate the whole process, but
only do the minimal amount of audio re-rendering (and consequential other re-rendering) when things change.

Tech we need:

- Render the narrative for each slide to audio sentence-by-sentence through ElevenLabs (with preceeding and following sentences as context). The secret `ELEVENLABS_API_KEY` is in place in github.

- Calculate the checksum of the tuple (the text-normalised version of the sentence, the context, the voice ID). Store the resulting audio in an s3 bucket. The secret `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are in place in github. If there's already an audio file in s3 at that path, don't render the audio, use the one that is already in s3.

- Render the slides with Marp to PNG

- For each slide, work out how long the audio is going to be, and then create `slides.txt` like this for each part:

```
file 'slide-01.png'
duration 5
file 'slide-02.png'
duration 7
file 'slide-03.png'
duration 4
```

- Generate a silent video from the slides

- Concatenate the audio

- Combine the video and audio

- Upload that render to s3 and some video hosting site (possibly just a static website)

- Convert questions into a suitable format

- Generate SCORM or equivalent e-learning format files from the videos and the quiz questions

- A test suite that takes the audio from the generated videos, transcribes it and confirms that it accurately reflects what we wrote

- Generation of an e-book (in PDF and EPUB formats) from all the parts combined
