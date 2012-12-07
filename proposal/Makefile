.PHONY: open clean

ASSIGN      = proposal

PARTS       = 

MAIN_TEX	= ${ASSIGN}.tex

PARTS_TEX	= ${addsuffix .tex,${PARTS}} 

PDF     	= ${ASSIGN}.pdf

FIGURES 	=

BIBFILES 	= refs.bib

TEX     	= pdflatex
TEXOPTS 	= -halt-on-error

BIBTEX  	= bibtex

open: ${PDF}
	open $< || gnome-open $<

${PDF}: ${MAIN_TEX} ${PARTS_TEX} ${FIGURES} ${BIBFILES}

%.pdf:	%.tex
	${TEX} ${TEXOPTS} $(basename $<)
	${BIBTEX} $(basename $<)
	${TEX} ${TEXOPTS} $(basename $<)
	${TEX} ${TEXOPTS} $(basename $<)

clean:
	rm -f *.log *.aux *.dvi ${PDF}
