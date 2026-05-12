package main

import (
	"os"
	"strings"
	"testing"
	"time"
)

func TestSplitSpeakerTurns(t *testing.T) {
	turns := splitSpeakerTurns("narratives/01.md", `Speaker 1: Welcome to ITIL.

Speaker 2: This is the reply.
It continues on the next line.`)

	if len(turns) != 2 {
		t.Fatalf("expected 2 turns, got %d", len(turns))
	}
	if turns[0].Speaker != "Speaker 1" {
		t.Fatalf("expected first speaker to be Speaker 1, got %q", turns[0].Speaker)
	}
	if turns[0].Text != "Welcome to ITIL." {
		t.Fatalf("unexpected first text: %q", turns[0].Text)
	}
	if turns[1].Speaker != "Speaker 2" {
		t.Fatalf("expected second speaker to be Speaker 2, got %q", turns[1].Speaker)
	}
	if !strings.Contains(turns[1].Text, "It continues") {
		t.Fatalf("expected continuation line in second turn, got %q", turns[1].Text)
	}
}

func TestGenerateVTTUsesVoiceTags(t *testing.T) {
	outputFile := t.TempDir() + "/subtitles.vtt"
	narratives := []Narrative{
		{
			SlideIndex: 1,
			TurnIndex:  1,
			Speaker:    "Speaker 1",
			Text:       "Welcome to ITIL.",
			StartTime:  0,
			EndTime:    2 * time.Second,
		},
		{
			SlideIndex: 1,
			TurnIndex:  2,
			Speaker:    "Speaker 2",
			Text:       "This is the reply.",
			StartTime:  2 * time.Second,
			EndTime:    4 * time.Second,
		},
	}

	if err := generateVTT(narratives, outputFile); err != nil {
		t.Fatal(err)
	}
	content, err := os.ReadFile(outputFile)
	if err != nil {
		t.Fatal(err)
	}
	text := string(content)
	if strings.Contains(text, "Speaker 1:") || strings.Contains(text, "Speaker 2:") {
		t.Fatalf("speaker labels should not be emitted as spoken text:\n%s", text)
	}
	if !strings.Contains(text, "<v Speaker 1>Welcome to ITIL.") {
		t.Fatalf("missing Speaker 1 voice tag:\n%s", text)
	}
	if !strings.Contains(text, "<v Speaker 2>This is the reply.") {
		t.Fatalf("missing Speaker 2 voice tag:\n%s", text)
	}
	if !strings.Contains(text, "1.1\n") || !strings.Contains(text, "1.2\n") {
		t.Fatalf("missing slide-aware cue identifiers:\n%s", text)
	}
}
