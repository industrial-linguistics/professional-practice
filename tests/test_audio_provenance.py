"""Keep a refreshed lesson's old audio out of the learner site."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import wave

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_elearning
from course_content import (
    load_topic, media_provenance, narration_fingerprint,
    topic_audio_filename, topic_media_files,
)


class AudioProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.topic = self.root / "part-01" / "roles"
        (self.topic / "narratives").mkdir(parents=True)
        (self.topic / "narratives" / "01.md").write_text("Speaker 1: Current narration.")
        (self.topic / "slides.html").write_text(
            '<section class="slide" data-slide="1" data-title="Roles"><h1>Roles</h1></section>'
        )
        (self.topic / "require-current-audio").touch()
        # An old MP3 may coexist with a newly generated authoritative WAV.
        (self.topic / "audio.mp3").write_bytes(b"old published take")
        with wave.open(str(self.topic / "audio.wav"), "wb") as audio:
            audio.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            audio.writeframes(b"\0\0" * 1600)
        (self.topic / "subtitles.vtt").write_text("WEBVTT\n\n00:00.000 --> 00:00.100\nCurrent narration.\n")

    def certify(self):
        metadata = media_provenance(
            self.topic, self.topic / "audio.wav", self.topic / "subtitles.vtt"
        )
        (self.topic / "audio-source.json").write_text(json.dumps(metadata))

    def test_uncertified_old_audio_is_not_published_or_advertised(self):
        self.assertEqual(topic_media_files(self.topic), (None, None))
        self.assertIsNone(topic_audio_filename(self.topic))
        with patch.object(build_elearning, "ELEARNING", self.root / "output"):
            self.assertEqual(
                build_elearning.copy_topic_media(load_topic("part-01", self.topic)),
                (None, None),
            )

    def test_script_audio_and_subtitle_changes_each_invalidate_take(self):
        for relative in ["narratives/01.md", "audio.wav", "subtitles.vtt"]:
            with self.subTest(relative=relative):
                self.certify()
                path = self.topic / relative
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                self.assertEqual(topic_media_files(self.topic), (None, None))
                path.write_bytes(original)

    def test_recording_refuses_a_script_changed_during_generation(self):
        fingerprint = narration_fingerprint(self.topic)
        (self.topic / "narratives" / "01.md").write_text("Changed during generation.")
        completed = subprocess.run(
            [sys.executable, str(Path(build_elearning.__file__).with_name("record_audio_source.py")),
             str(self.topic), "--expected-fingerprint", fingerprint],
            capture_output=True, text=True,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertFalse((self.topic / "audio-source.json").exists())

    def test_invalid_metadata_fails_closed(self):
        for data in ["{", "[]", '{"audio_file":"../outside.mp3"}']:
            with self.subTest(data=data):
                (self.topic / "audio-source.json").write_text(data)
                self.assertEqual(topic_media_files(self.topic), (None, None))

    def test_legacy_lesson_keeps_existing_media_behaviour(self):
        (self.topic / "require-current-audio").unlink()
        self.assertEqual(topic_audio_filename(self.topic), "audio.mp3")

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required for WAV publication")
    def test_fresh_master_is_transcoded_and_survives_published_media_sync(self):
        script = Path(build_elearning.__file__).with_name("record_audio_source.py")
        subprocess.run(
            [sys.executable, str(script), str(self.topic), "--expected-fingerprint",
             narration_fingerprint(self.topic)], check=True, capture_output=True,
        )
        self.assertEqual(topic_audio_filename(self.topic), "audio.wav")
        with patch.object(build_elearning, "ELEARNING", self.root / "output"):
            result = build_elearning.copy_topic_media(load_topic("part-01", self.topic))
        self.assertEqual(result, ("audio.mp3", "subtitles.vtt"))
        delivered = self.root / "output/media/part-01/roles"
        synced = self.root / "synced"
        shutil.copytree(self.topic, synced)
        (synced / "audio.wav").unlink()
        for filename in ["audio.mp3", "subtitles.vtt", "audio-source.json"]:
            shutil.copy2(delivered / filename, synced / filename)
        self.assertEqual(topic_audio_filename(synced), "audio.mp3")
        self.assertNotEqual((synced / "audio.mp3").read_bytes(), b"old published take")
        (synced / "audio.mp3").write_bytes(b"stale after sync")
        self.assertIsNone(topic_audio_filename(synced))


if __name__ == "__main__":
    unittest.main()
