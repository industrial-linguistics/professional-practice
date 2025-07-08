package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"

	"github.com/jung-kurt/gofpdf"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

func copyFont(src, dstDir string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()
	if err := os.MkdirAll(dstDir, 0755); err != nil {
		return err
	}
	outPath := filepath.Join(dstDir, filepath.Base(src))
	out, err := os.Create(outPath)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, in)
	return err
}

func findDejaVuDir() (string, bool) {
	env := os.Getenv("DEJAVU_FONT_DIR")
	var dirs []string
	if env != "" {
		dirs = append(dirs, env)
	}
	dirs = append(dirs,
		filepath.Join(string(os.PathSeparator), "usr", "share", "fonts", "truetype", "dejavu"),
		filepath.Join(os.Getenv("SystemRoot"), "Fonts"),
		filepath.Join(string(os.PathSeparator), "Library", "Fonts"),
	)
	for _, dir := range dirs {
		reg := filepath.Join(dir, "DejaVuSans.ttf")
		bold := filepath.Join(dir, "DejaVuSans-Bold.ttf")
		if _, err := os.Stat(reg); err == nil {
			if _, err := os.Stat(bold); err == nil {
				return dir, true
			}
		}
	}

	out, err := exec.Command("fc-list", "--format", "%{file}\n").Output()
	if err != nil {
		return "", false
	}
	scanner := bufio.NewScanner(bytes.NewReader(out))
	var regPath, boldPath string
	for scanner.Scan() {
		p := scanner.Text()
		base := filepath.Base(p)
		if base == "DejaVuSans.ttf" {
			regPath = filepath.Dir(p)
		} else if base == "DejaVuSans-Bold.ttf" {
			boldPath = filepath.Dir(p)
		}
	}
	if regPath != "" && regPath == boldPath {
		return regPath, true
	}
	return "", false
}

func addTopic(pdf *gofpdf.Fpdf, part string, topicPath string, baseFont string, imageRoot string) error {
	title := cases.Title(language.Und, cases.NoLower).String(strings.ReplaceAll(filepath.Base(topicPath), "-", " "))
	topic := title
	pdf.SetFont(baseFont, "B", 16)
	pdf.CellFormat(0, 10, topic, "", 1, "L", false, 0, "")

	imgDir := filepath.Join(imageRoot, part, filepath.Base(topicPath))
	images, err := filepath.Glob(filepath.Join(imgDir, "slide.*.png"))
	if err != nil {
		return err
	}
	sort.Strings(images)
	narratives, err := filepath.Glob(filepath.Join(topicPath, "narratives", "*.md"))
	if err != nil {
		return err
	}
	sort.Strings(narratives)

	for i, img := range images {
		pdf.ImageOptions(img, 15, pdf.GetY(), 180, 0, false, gofpdf.ImageOptions{ImageType: "PNG"}, 0, "")
		pdf.Ln(2)
		if i < len(narratives) {
			b, err := os.ReadFile(narratives[i])
			if err != nil {
				return err
			}
			text := strings.TrimSpace(string(b))
			pdf.SetFont(baseFont, "", 12)
			pdf.MultiCell(0, 5, text, "", "", false)
		}
		if i != len(images)-1 {
			pdf.AddPage()
		}
	}
	return nil
}

func main() {
	root, err := filepath.Abs(".")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	contentRoot := filepath.Join(root, "content")
	imageRoot := filepath.Join(root, "assets", "slide-images")
	outputDir := filepath.Join(root, "run-sheets")
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	baseFont := "Helvetica"
	localFontDir := filepath.Join(root, "assets", "fonts")
	useDejaVu := false
	if sysDir, ok := findDejaVuDir(); ok {
		fontRegular := filepath.Join(sysDir, "DejaVuSans.ttf")
		fontBold := filepath.Join(sysDir, "DejaVuSans-Bold.ttf")
		if err := copyFont(fontRegular, localFontDir); err == nil {
			if err := copyFont(fontBold, localFontDir); err == nil {
				useDejaVu = true
			}
		}
	}

	entries, err := os.ReadDir(contentRoot)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	sort.Slice(entries, func(i, j int) bool { return entries[i].Name() < entries[j].Name() })

	for _, entry := range entries {
		if entry.IsDir() {
			partPath := filepath.Join(contentRoot, entry.Name())
			pdf := gofpdf.New("P", "mm", "A4", localFontDir)
			pdf.SetAutoPageBreak(true, 15)
			currentFont := baseFont
			if useDejaVu {
				pdf.AddUTF8Font("DejaVu", "", "DejaVuSans.ttf")
				pdf.AddUTF8Font("DejaVu", "B", "DejaVuSans-Bold.ttf")
				currentFont = "DejaVu"
			}
			pdf.AddPage()
			pdf.SetFont(currentFont, "B", 20)
			pdf.CellFormat(0, 10, cases.Title(language.Und, cases.NoLower).String(strings.ReplaceAll(entry.Name(), "-", " ")), "", 1, "C", false, 0, "")

			topics, err := os.ReadDir(partPath)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(1)
			}
			sort.Slice(topics, func(i, j int) bool { return topics[i].Name() < topics[j].Name() })
			for _, t := range topics {
				if !t.IsDir() {
					continue
				}
				slides := filepath.Join(partPath, t.Name(), "slides.md")
				if _, err := os.Stat(slides); err != nil {
					if !os.IsNotExist(err) {
						fmt.Fprintln(os.Stderr, err)
						os.Exit(1)
					}
					continue
				}
				if err := addTopic(pdf, entry.Name(), filepath.Join(partPath, t.Name()), currentFont, imageRoot); err != nil {
					fmt.Fprintln(os.Stderr, err)
					os.Exit(1)
				}
				pdf.AddPage()
			}
			outFile := filepath.Join(outputDir, entry.Name()+".pdf")
			if err := pdf.OutputFileAndClose(outFile); err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(1)
			}
		}
	}
}
