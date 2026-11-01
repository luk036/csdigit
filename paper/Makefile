# Build the csd-tutorial paper.
#
# The title, author, and abstract are in the YAML header of csd-tutorial.md,
# and body headings start at level 1, so no --shift-heading-level-by is needed.
# Pandoc ships its default CSL, so --citeproc needs no network access.
#
# -F pandoc-crossref : resolve @sec:, @eq:, and @tbl: references
# --citeproc         : render citations from references.bib
# -s -t latex        : standalone LaTeX; pandoc invokes the PDF engine
# -N                 : number sections
# --reference-links  : use reference-style links in the generated source
# --pdf-engine       : explicit engine; MiKTeX provides pdflatex

PAPER = csd-tutorial
TALK = csd-tutorial-talk

.PHONY: all paper talk clean

all: paper

paper: $(PAPER).pdf

$(PAPER).pdf: $(PAPER).md references.bib
	pandoc -F pandoc-crossref --citeproc -s -t latex -N --reference-links \
	  --pdf-engine=pdflatex \
	  $(PAPER).md -o $(PAPER).pdf

# Talk: manual references only, so no citeproc or crossref filter is needed.
# --include-in-header is a CLI flag; a YAML header-includes value is ignored.
# Run lualatex twice so the Frankfurt section navigation is stable.
talk: $(TALK).pdf

$(TALK).tex: $(TALK).md beamer-preamble.tex
	pandoc -s -t beamer --include-in-header=beamer-preamble.tex \
	  $(TALK).md -o $(TALK).tex

$(TALK).pdf: $(TALK).tex
	lualatex -interaction=nonstopmode -halt-on-error $(TALK).tex
	lualatex -interaction=nonstopmode -halt-on-error $(TALK).tex

clean:
	$(RM) $(PAPER).pdf $(TALK).pdf $(TALK).tex $(TALK).aux $(TALK).log \
	  $(TALK).nav $(TALK).out $(TALK).snm $(TALK).toc
