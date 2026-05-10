package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

func main() {
	if _, err := exec.LookPath("marp"); err != nil {
		log.Fatalf("marp CLI not found: %v", err)
	}

	root, err := filepath.Abs(".")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	content := filepath.Join(root, "content")
	outputRoot := filepath.Join(root, "assets", "slide-images")

	var slideFiles []string
	if len(os.Args) > 1 {
		for _, arg := range os.Args[1:] {
			path := arg
			if !filepath.IsAbs(path) {
				path = filepath.Join(root, path)
			}
			info, err := os.Stat(path)
			if err != nil {
				fmt.Fprintln(os.Stderr, "error:", err)
				os.Exit(1)
			}
			if info.IsDir() {
				path = filepath.Join(path, "slides.md")
			}
			slideFiles = append(slideFiles, path)
		}
	} else {
		err = filepath.WalkDir(content, func(path string, d os.DirEntry, err error) error {
			if err != nil {
				return err
			}
			if d.IsDir() || d.Name() != "slides.md" {
				return nil
			}
			slideFiles = append(slideFiles, path)
			return nil
		})
		if err != nil {
			fmt.Fprintln(os.Stderr, "error:", err)
			os.Exit(1)
		}
	}

	for _, path := range slideFiles {
		rel, err := filepath.Rel(content, path)
		if err != nil {
			fmt.Fprintln(os.Stderr, "error:", err)
			os.Exit(1)
		}
		parts := strings.Split(rel, string(os.PathSeparator))
		if len(parts) < 2 {
			log.Printf("skipping %s: unexpected path", path)
			continue
		}
		part := parts[0]
		topic := parts[1]
		outDir := filepath.Join(outputRoot, part, topic)
		if err := os.MkdirAll(outDir, 0755); err != nil {
			fmt.Fprintln(os.Stderr, "error:", err)
			os.Exit(1)
		}
		outPattern := filepath.Join(outDir, "slide.png")
		args := []string{"--images", "png", path, "-o", outPattern}
		if browserPath := os.Getenv("MARP_BROWSER_PATH"); browserPath != "" {
			args = append([]string{"--browser", "chrome", "--browser-path", browserPath}, args...)
		}
		cmd := exec.Command("marp", args...)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		cmd.Env = append(os.Environ(), "PUPPETEER_DANGEROUS_NO_SANDBOX=true")
		fmt.Println("Running", strings.Join(cmd.Args, " "))
		var lastErr error
		for attempt := 1; attempt <= 3; attempt++ {
			if err := cmd.Run(); err != nil {
				lastErr = err
				fmt.Fprintf(os.Stderr, "marp attempt %d failed: %v\n", attempt, err)
				if attempt < 3 {
					time.Sleep(time.Duration(attempt) * time.Second)
					cmd = exec.Command("marp", args...)
					cmd.Stdout = os.Stdout
					cmd.Stderr = os.Stderr
					cmd.Env = append(os.Environ(), "PUPPETEER_DANGEROUS_NO_SANDBOX=true")
				}
				continue
			}
			lastErr = nil
			break
		}
		if lastErr != nil {
			fmt.Fprintln(os.Stderr, "error:", lastErr)
			os.Exit(1)
		}
	}
}
