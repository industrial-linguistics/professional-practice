package main

import (
	"fmt"
	"io/fs"
	"log"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
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

	err = filepath.WalkDir(content, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			return nil
		}
		if d.Name() != "slides.md" {
			return nil
		}
		rel, err := filepath.Rel(content, path)
		if err != nil {
			return err
		}
		parts := strings.Split(rel, string(os.PathSeparator))
		if len(parts) < 2 {
			log.Printf("skipping %s: unexpected path", path)
			return nil
		}
		part := parts[0]
		topic := parts[1]
		outDir := filepath.Join(outputRoot, part, topic)
		if err := os.MkdirAll(outDir, 0755); err != nil {
			return err
		}
		outPattern := filepath.Join(outDir, "slide.png")
		cmd := exec.Command("marp", "--images", "png", path, "-o", outPattern)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		fmt.Println("Running", strings.Join(cmd.Args, " "))
		return cmd.Run()
	})
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}
