# To-do 

### General

- [x] Clean up the tables and dot points in the README so that they are in proper markdown format. They are in a mixture of lines, unicode dotpoints, tab separated texts and so on

- [x] Create a separate to-do list file with everything that was in the README.md file (and remove it from README.md)

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
	
- Aus. Privacy Act 1988 (especially APP 11 on security)
- Critical Infrastructure Act 2018 – SLAs can hinge on it for some clients
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

