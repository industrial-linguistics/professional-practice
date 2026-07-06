package main

import (
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strings"
	"time"

	"github.com/spf13/cobra"
)

type Config struct {
	ContentDir     string
	WordsPerMinute float64
	OutputFile     string
	Validate       bool
}

type Narrative struct {
	Path       string
	SlideIndex int
	TurnIndex  int
	Speaker    string
	Text       string
	WordCount  int
	Duration   time.Duration
	StartTime  time.Duration
	EndTime    time.Duration
}

var speakerPrefixRe = regexp.MustCompile(`(?i)^\s*(Speaker\s+\d+)\s*:\s*(.*)$`)

func main() {
	var config Config

	rootCmd := &cobra.Command{
		Use:   "vtt-generator [topic-path]",
		Short: "Generate VTT subtitle files from narrative markdown files",
		Args:  cobra.MinimumNArgs(1),
		RunE: func(cmd *cobra.Command, args []string) error {
			config.ContentDir = args[0]
			return run(config)
		},
	}

	rootCmd.Flags().Float64VarP(&config.WordsPerMinute, "wpm", "w", 150.0, "Words per minute for speech timing")
	rootCmd.Flags().StringVarP(&config.OutputFile, "output", "o", "", "Output VTT file (default: <topic-path>/subtitles.vtt)")
	rootCmd.Flags().BoolVarP(&config.Validate, "validate", "v", true, "Validate narrative count matches slide count")

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func run(config Config) error {
	// Find narratives directory
	narrativesDir := filepath.Join(config.ContentDir, "narratives")
	if _, err := os.Stat(narrativesDir); os.IsNotExist(err) {
		return fmt.Errorf("narratives directory not found: %s", narrativesDir)
	}

	// Read all narrative files
	files, err := filepath.Glob(filepath.Join(narrativesDir, "*.md"))
	if err != nil {
		return fmt.Errorf("failed to read narratives: %v", err)
	}

	if len(files) == 0 {
		return fmt.Errorf("no narrative files found in %s", narrativesDir)
	}

	sort.Strings(files)
	filteredFiles := make([]string, 0, len(files))
	for _, file := range files {
		base := strings.ToLower(filepath.Base(file))
		if base == "outline.md" || base == "readme.md" {
			continue
		}
		filteredFiles = append(filteredFiles, file)
	}
	files = filteredFiles

	// Parse narratives
	narratives := make([]Narrative, 0, len(files))
	var cumulativeTime time.Duration = 0

	for fileIndex, file := range files {
		content, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read %s: %v", file, err)
		}

		text := cleanMarkdown(string(content))
		turns := splitSpeakerTurns(file, text)
		fileWordCount := 0
		for _, turn := range turns {
			fileWordCount += turn.WordCount
		}
		if fileWordCount == 0 {
			fileWordCount = 1
		}

		// Preserve one slide-sized timing block per narrative file, but emit
		// separate WebVTT cues for each speaker turn inside that block.
		durationSeconds := float64(fileWordCount) / config.WordsPerMinute * 60.0
		fileDuration := time.Duration(durationSeconds * float64(time.Second))
		fileStart := cumulativeTime
		fileEnd := fileStart + fileDuration
		turnStart := fileStart

		for i, turn := range turns {
			turnDuration := time.Duration(float64(fileDuration) * float64(turn.WordCount) / float64(fileWordCount))
			turnEnd := turnStart + turnDuration
			if i == len(turns)-1 {
				turnEnd = fileEnd
				turnDuration = turnEnd - turnStart
			}
			turn.SlideIndex = fileIndex + 1
			turn.TurnIndex = i + 1
			turn.StartTime = turnStart
			turn.EndTime = turnEnd
			turn.Duration = turnDuration
			narratives = append(narratives, turn)
			turnStart = turnEnd
		}

		cumulativeTime = fileEnd
	}

	// Validate if requested
	if config.Validate {
		slidesFile := filepath.Join(config.ContentDir, "slides.html")
		if _, err := os.Stat(slidesFile); err == nil {
			slideCount, err := countHTMLSlides(slidesFile)
			if err != nil {
				return fmt.Errorf("failed to count slides: %v", err)
			}

			if slideCount != len(files) {
				return fmt.Errorf("validation failed: %d slides but %d narratives", slideCount, len(files))
			}

			fmt.Printf("Validation passed: %d slides match %d narratives\n", slideCount, len(files))
		}
	}

	// Generate VTT
	outputFile := config.OutputFile
	if outputFile == "" {
		outputFile = filepath.Join(config.ContentDir, "subtitles.vtt")
	}

	if err := generateVTT(narratives, outputFile); err != nil {
		return fmt.Errorf("failed to generate VTT: %v", err)
	}

	totalDuration := narratives[len(narratives)-1].EndTime
	fmt.Printf("Generated %s with %d entries (total duration: %v)\n",
		outputFile, len(narratives), totalDuration)

	return nil
}

func cleanMarkdown(text string) string {
	// Remove markdown syntax but keep the content
	text = strings.TrimSpace(text)

	// Remove headers
	re := regexp.MustCompile(`(?m)^#+\s+`)
	text = re.ReplaceAllString(text, "")

	// Remove bold/italic markers
	text = strings.ReplaceAll(text, "**", "")
	text = strings.ReplaceAll(text, "*", "")
	text = strings.ReplaceAll(text, "__", "")
	text = strings.ReplaceAll(text, "_", "")

	// Remove links but keep text
	re = regexp.MustCompile(`\[([^\]]+)\]\([^\)]+\)`)
	text = re.ReplaceAllString(text, "$1")

	return strings.TrimSpace(text)
}

func splitSpeakerTurns(path string, text string) []Narrative {
	lines := strings.Split(text, "\n")
	turns := make([]Narrative, 0)
	var speaker string
	var textParts []string

	flush := func() {
		turnText := strings.TrimSpace(strings.Join(textParts, " "))
		if turnText == "" {
			textParts = nil
			return
		}
		turns = append(turns, Narrative{
			Path:      path,
			Speaker:   speaker,
			Text:      turnText,
			WordCount: countWords(turnText),
		})
		textParts = nil
	}

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		if match := speakerPrefixRe.FindStringSubmatch(line); match != nil {
			flush()
			speaker = canonicalSpeakerLabel(match[1])
			if strings.TrimSpace(match[2]) != "" {
				textParts = append(textParts, strings.TrimSpace(match[2]))
			}
			continue
		}
		textParts = append(textParts, line)
	}
	flush()

	if len(turns) == 0 && strings.TrimSpace(text) != "" {
		turns = append(turns, Narrative{
			Path:      path,
			Text:      strings.TrimSpace(text),
			WordCount: countWords(text),
		})
	}

	for i := range turns {
		if turns[i].WordCount == 0 {
			turns[i].WordCount = 1
		}
	}

	return turns
}

func canonicalSpeakerLabel(label string) string {
	fields := strings.Fields(strings.TrimSpace(label))
	if len(fields) == 0 {
		return ""
	}
	if strings.EqualFold(fields[0], "speaker") && len(fields) > 1 {
		return "Speaker " + fields[1]
	}
	return strings.Join(fields, " ")
}

func countWords(text string) int {
	// Split on whitespace and count
	fields := strings.Fields(text)
	return len(fields)
}

func countHTMLSlides(slidesFile string) (int, error) {
	content, err := os.ReadFile(slidesFile)
	if err != nil {
		return 0, err
	}

	re := regexp.MustCompile(`(?is)<section[^>]*class=["'][^"']*\bslide\b[^"']*["'][^>]*>`)
	return len(re.FindAll(content, -1)), nil
}

func formatTimestamp(d time.Duration) string {
	hours := int(d.Hours())
	minutes := int(d.Minutes()) % 60
	seconds := int(d.Seconds()) % 60
	milliseconds := int(d.Milliseconds()) % 1000

	return fmt.Sprintf("%02d:%02d:%02d.%03d", hours, minutes, seconds, milliseconds)
}

func generateVTT(narratives []Narrative, outputFile string) error {
	var sb strings.Builder

	sb.WriteString("WEBVTT\n\n")

	for i, narrative := range narratives {
		// VTT cue identifier. Speaker-turn cues retain their source slide
		// number so the video assembler can group them back onto one slide.
		if narrative.SlideIndex > 0 && narrative.TurnIndex > 0 {
			sb.WriteString(fmt.Sprintf("%d.%d\n", narrative.SlideIndex, narrative.TurnIndex))
		} else {
			sb.WriteString(fmt.Sprintf("%d\n", i+1))
		}

		// Timestamp
		sb.WriteString(fmt.Sprintf("%s --> %s\n",
			formatTimestamp(narrative.StartTime),
			formatTimestamp(narrative.EndTime)))

		// Text content. Use a WebVTT voice tag so captions and TTS can keep
		// speaker identity without speaking "Speaker 1" aloud.
		if narrative.Speaker != "" {
			sb.WriteString(fmt.Sprintf("<v %s>%s", narrative.Speaker, narrative.Text))
		} else {
			sb.WriteString(narrative.Text)
		}
		sb.WriteString("\n\n")
	}

	return os.WriteFile(outputFile, []byte(sb.String()), 0644)
}
