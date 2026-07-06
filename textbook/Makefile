TEX=main.tex
AMAZON_TEX=main-amazon.tex
PDF=main.pdf
AMAZON_PDF=main-amazon.pdf
LATEXMK=latexmk -xelatex -quiet -e '$$max_repeat=10'
BASE=$(basename $(TEX))
AMAZON_BASE=$(basename $(AMAZON_TEX))
CHAPTERS=$(wildcard chapters/*.tex)
FIGURES=$(shell find figures -type f 2>/dev/null)

all: $(PDF) $(AMAZON_PDF)

$(PDF): $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(TEX)
	makeindex $(BASE) >/dev/null || true
	$(LATEXMK) $(TEX)

$(AMAZON_PDF): $(AMAZON_TEX) $(TEX) $(CHAPTERS) $(FIGURES)
	$(LATEXMK) $(AMAZON_TEX)
	makeindex $(AMAZON_BASE) >/dev/null || true
	$(LATEXMK) $(AMAZON_TEX)

free-pdf: $(PDF)

amazon-pdf: $(AMAZON_PDF)

clean:
	latexmk -C $(TEX) || true
	latexmk -C $(AMAZON_TEX) || true
	rm -f $(BASE).idx $(BASE).ind $(BASE).ilg $(AMAZON_BASE).idx $(AMAZON_BASE).ind $(AMAZON_BASE).ilg

.PHONY: all free-pdf amazon-pdf clean
