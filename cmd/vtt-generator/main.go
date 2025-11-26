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
	Path     string
	Text     string
	WordCount int
	Duration time.Duration
	StartTime time.Duration
	EndTime   time.Duration
}

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

	// Parse narratives
	narratives := make([]Narrative, 0, len(files))
	var cumulativeTime time.Duration = 0

	for _, file := range files {
		content, err := os.ReadFile(file)
		if err != nil {
			return fmt.Errorf("failed to read %s: %v", file, err)
		}

		text := string(content)
		text = cleanMarkdown(text)
		wordCount := countWords(text)

		// Calculate duration based on words per minute
		durationSeconds := float64(wordCount) / config.WordsPerMinute * 60.0
		duration := time.Duration(durationSeconds * float64(time.Second))

		narrative := Narrative{
			Path:      file,
			Text:      text,
			WordCount: wordCount,
			Duration:  duration,
			StartTime: cumulativeTime,
			EndTime:   cumulativeTime + duration,
		}

		narratives = append(narratives, narrative)
		cumulativeTime = narrative.EndTime
	}

	// Validate if requested
	if config.Validate {
		slidesFile := filepath.Join(config.ContentDir, "slides.md")
		if _, err := os.Stat(slidesFile); err == nil {
			slideCount, err := countMarpSlides(slidesFile)
			if err != nil {
				return fmt.Errorf("failed to count slides: %v", err)
			}

			if slideCount != len(narratives) {
				return fmt.Errorf("validation failed: %d slides but %d narratives", slideCount, len(narratives))
			}

			fmt.Printf("Validation passed: %d slides match %d narratives\n", slideCount, len(narratives))
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

func countWords(text string) int {
	// Split on whitespace and count
	fields := strings.Fields(text)
	return len(fields)
}

func countMarpSlides(slidesFile string) (int, error) {
	content, err := os.ReadFile(slidesFile)
	if err != nil {
		return 0, err
	}

	text := string(content)

	// Count slide separators (---) but exclude YAML front matter
	lines := strings.Split(text, "\n")
	slideCount := 0
	inFrontMatter := false
	frontMatterCount := 0

	for _, line := range lines {
		trimmed := strings.TrimSpace(line)

		if trimmed == "---" {
			if frontMatterCount < 2 {
				// This is part of YAML front matter
				frontMatterCount++
				if frontMatterCount == 1 {
					inFrontMatter = true
				} else if frontMatterCount == 2 {
					inFrontMatter = false
				}
			} else if !inFrontMatter {
				// This is a slide separator
				slideCount++
			}
		}
	}

	// Add 1 because if there are N separators, there are N+1 slides
	// But only if we actually found the file had content
	if slideCount > 0 || len(text) > 0 {
		slideCount++
	}

	return slideCount, nil
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
		// VTT entry number
		sb.WriteString(fmt.Sprintf("%d\n", i+1))

		// Timestamp
		sb.WriteString(fmt.Sprintf("%s --> %s\n",
			formatTimestamp(narrative.StartTime),
			formatTimestamp(narrative.EndTime)))

		// Text content
		sb.WriteString(narrative.Text)
		sb.WriteString("\n\n")
	}

	return os.WriteFile(outputFile, []byte(sb.String()), 0644)
}
