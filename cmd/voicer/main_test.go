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
	clearGregVoiceSettingsEnv(t)

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
		DefaultVoice: "Anna",
		OutputFormat: "pcm_44100",
		TempDir:      t.TempDir(),
		Speed:        1.0,
	})

	if len(segments) != 2 {
		t.Fatalf("expected 2 segments, got %d", len(segments))
	}
	if segments[0].Voice != "Anna" {
		t.Fatalf("expected Speaker 1 to use Anna, got %q", segments[0].Voice)
	}
	if segments[1].Voice != "Greg" {
		t.Fatalf("expected Speaker 2 to use Greg, got %q", segments[1].Voice)
	}
	if segments[1].PrevText != "First line." {
		t.Fatalf("expected previous text to be assigned, got %q", segments[1].PrevText)
	}
}

func TestBuildAudioSegmentsUsesRobopastorGregVoiceSettings(t *testing.T) {
	t.Setenv("VOICER_SPEAKER_VOICES", "")
	t.Setenv("VOICER_SPEAKER_2_VOICE", "")
	clearGregVoiceSettingsEnv(t)

	subs := &astisub.Subtitles{
		Items: []*astisub.Item{
			{
				StartAt: 0,
				EndAt:   2 * time.Second,
				Lines: []astisub.Line{
					{VoiceName: "Speaker 2", Items: []astisub.LineItem{{Text: "Second line."}}},
				},
			},
		},
	}

	segments := buildAudioSegments(subs, Config{
		DefaultVoice: "Anna",
		OutputFormat: "pcm_44100",
		TempDir:      t.TempDir(),
		Speed:        1.0,
	})

	if len(segments) != 1 {
		t.Fatalf("expected 1 segment, got %d", len(segments))
	}
	if getVoiceID(segments[0].Voice) != "vTdXuGkq3ozMNBhP2Hz7" {
		t.Fatalf("expected Greg to resolve to robopastor voice, got %q", getVoiceID(segments[0].Voice))
	}
	settings := segments[0].Settings
	assertFloatPtr(t, settings.Speed, 1.0, "speed")
	assertFloatPtr(t, settings.Stability, 0.50, "stability")
	assertFloatPtr(t, settings.SimilarityBoost, 0.75, "similarity_boost")
	assertFloatPtr(t, settings.Style, 0.0, "style")
	if settings.UseSpeakerBoost == nil || !*settings.UseSpeakerBoost {
		t.Fatalf("expected speaker boost to be true, got %#v", settings.UseSpeakerBoost)
	}
	if segments[0].Speed != 1.0 {
		t.Fatalf("expected segment speed 1.0, got %.2f", segments[0].Speed)
	}
}

func TestChecksumChangesWithVoiceSettings(t *testing.T) {
	base := VoiceSettings{
		Speed: floatPtr(1.0),
	}
	stable := VoiceSettings{
		Stability:       floatPtr(0.50),
		SimilarityBoost: floatPtr(0.75),
		Style:           floatPtr(0.0),
		UseSpeakerBoost: boolPtr(true),
		Speed:           floatPtr(1.0),
	}

	baseChecksum := calculateChecksum("text", "prev", "next", voiceIDMap["Greg"], base)
	stableChecksum := calculateChecksum("text", "prev", "next", voiceIDMap["Greg"], stable)

	if baseChecksum == stableChecksum {
		t.Fatal("expected voice setting changes to change the checksum")
	}
}

func clearGregVoiceSettingsEnv(t *testing.T) {
	t.Helper()
	t.Setenv("VOICER_GREG_SPEED", "")
	t.Setenv("VOICER_GREG_STABILITY", "")
	t.Setenv("VOICER_GREG_SIMILARITY", "")
	t.Setenv("VOICER_GREG_SIMILARITY_BOOST", "")
	t.Setenv("VOICER_GREG_STYLE", "")
	t.Setenv("VOICER_GREG_SPEAKER_BOOST", "")
}

func assertFloatPtr(t *testing.T, got *float64, want float64, label string) {
	t.Helper()
	if got == nil {
		t.Fatalf("expected %s to be %.2f, got nil", label, want)
	}
	if *got != want {
		t.Fatalf("expected %s %.2f, got %.2f", label, want, *got)
	}
}
