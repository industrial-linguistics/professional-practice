package main

import (
	"testing"
	"time"

	"github.com/asticode/go-astisub"
)

func TestExtractSubtitleTextAndSpeaker(t *testing.T) {
	item := &astisub.Item{
		Lines: []astisub.Line{
			{
				VoiceName: "Speaker 2",
				Items:     []astisub.LineItem{{Text: "ITIL keeps support work predictable."}},
			},
		},
	}

	text, speaker := extractSubtitleTextAndSpeaker(item)
	if speaker != "Speaker 2" {
		t.Fatalf("expected Speaker 2, got %q", speaker)
	}
	if text != "eye-till keeps support work predictable." {
		t.Fatalf("unexpected normalized text: %q", text)
	}
}

func TestBuildAudioSegmentsAssignsSpeakerVoices(t *testing.T) {
	t.Setenv("VOICER_SPEAKER_VOICES", "")
	t.Setenv("VOICER_SPEAKER_1_VOICE", "")
	t.Setenv("VOICER_SPEAKER_2_VOICE", "")

	subs := &astisub.Subtitles{
		Items: []*astisub.Item{
			{
				StartAt: 0,
				EndAt:   2 * time.Second,
				Lines: []astisub.Line{
					{VoiceName: "Speaker 1", Items: []astisub.LineItem{{Text: "First line."}}},
				},
			},
			{
				StartAt: 2 * time.Second,
				EndAt:   4 * time.Second,
				Lines: []astisub.Line{
					{VoiceName: "Speaker 2", Items: []astisub.LineItem{{Text: "Second line."}}},
				},
			},
		},
	}

	segments := buildAudioSegments(subs, Config{
		DefaultVoice: "Sophia",
		OutputFormat: "pcm_44100",
		TempDir:      t.TempDir(),
		Speed:        1.0,
	})

	if len(segments) != 2 {
		t.Fatalf("expected 2 segments, got %d", len(segments))
	}
	if segments[0].Voice != "Sophia" {
		t.Fatalf("expected Speaker 1 to use Sophia, got %q", segments[0].Voice)
	}
	if segments[1].Voice != "Greg" {
		t.Fatalf("expected Speaker 2 to use Greg, got %q", segments[1].Voice)
	}
	if segments[1].PrevText != "First line." {
		t.Fatalf("expected previous text to be assigned, got %q", segments[1].PrevText)
	}
}
