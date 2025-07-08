package main

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"

	"github.com/jung-kurt/gofpdf"
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

func addTopic(pdf *gofpdf.Fpdf, part string, topicPath string, baseFont string, imageRoot string) error {
	topic := strings.Title(strings.ReplaceAll(filepath.Base(topicPath), "-", " "))
	pdf.SetFont(baseFont, "B", 16)
	pdf.CellFormat(0, 10, topic, "", 1, "L", false, 0, "")

	imgDir := filepath.Join(imageRoot, part, filepath.Base(topicPath))
	images, _ := filepath.Glob(filepath.Join(imgDir, "slide.*.png"))
	sort.Strings(images)
	narratives, _ := filepath.Glob(filepath.Join(topicPath, "narratives", "*.md"))
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

func buildPart(partPath string, imageRoot string, outputDir string, baseFont, fontDir string) error {
	part := filepath.Base(partPath)
	pdf := gofpdf.New("P", "mm", "A4", fontDir)
	pdf.SetAutoPageBreak(true, 15)
	pdf.AddPage()
	pdf.SetFont(baseFont, "B", 20)
	pdf.CellFormat(0, 10, strings.Title(strings.ReplaceAll(part, "-", " ")), "", 1, "C", false, 0, "")

	entries, err := os.ReadDir(partPath)
	if err != nil {
		return err
	}
	sort.Slice(entries, func(i, j int) bool { return entries[i].Name() < entries[j].Name() })

	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}
		slides := filepath.Join(partPath, entry.Name(), "slides.md")
		if _, err := os.Stat(slides); err == nil {
			if err := addTopic(pdf, part, filepath.Join(partPath, entry.Name()), baseFont, imageRoot); err != nil {
				return err
			}
			pdf.AddPage()
		}
	}
	outFile := filepath.Join(outputDir, part+".pdf")
	return pdf.OutputFileAndClose(outFile)
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
	systemFontDir := filepath.Join(string(os.PathSeparator), "usr", "share", "fonts", "truetype", "dejavu")
	fontRegular := filepath.Join(systemFontDir, "DejaVuSans.ttf")
	fontBold := filepath.Join(systemFontDir, "DejaVuSans-Bold.ttf")
	localFontDir := filepath.Join(root, "assets", "fonts")

	useDejaVu := false
	if _, err := os.Stat(fontRegular); err == nil {
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
			if useDejaVu {
				pdf.AddUTF8Font("DejaVu", "", "DejaVuSans.ttf")
				pdf.AddUTF8Font("DejaVu", "B", "DejaVuSans-Bold.ttf")
				baseFont = "DejaVu"
			}
			pdf.AddPage()
			pdf.SetFont(baseFont, "B", 20)
			pdf.CellFormat(0, 10, strings.Title(strings.ReplaceAll(entry.Name(), "-", " ")), "", 1, "C", false, 0, "")

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
				if _, err := os.Stat(slides); err == nil {
					if err := addTopic(pdf, entry.Name(), filepath.Join(partPath, t.Name()), baseFont, imageRoot); err != nil {
						fmt.Fprintln(os.Stderr, err)
						os.Exit(1)
					}
					pdf.AddPage()
				}
			}
			outFile := filepath.Join(outputDir, entry.Name()+".pdf")
			if err := pdf.OutputFileAndClose(outFile); err != nil {
				fmt.Fprintln(os.Stderr, err)
				os.Exit(1)
			}
		}
	}
}
