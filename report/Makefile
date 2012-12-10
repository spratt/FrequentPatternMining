######################################################################
# LatexTemplate Makefile
# By Simon Pratt
# November 10, 2010
######################################################################

ASSIGN      = assignment

REFERENCES 	= references

PARTS       = 

FIGURES 	=

STYLES      = Assignment \
			  CGAlgorithms \
			  HeaderStuff \
			  QuestionAnswer \
			  TheoremStuff

######################################################################
# Modify the following at your own risk
######################################################################

.PHONY: open clean

MAIN_TEX	= ${ASSIGN}.tex

PARTS_TEX	= ${addsuffix .tex,${PARTS}}

BIBFILES	= ${addsuffix .bib,${REFERENCES}}

STYLES_STY  = ${addsuffix .sty,${STYLES}}

PDF     	= ${ASSIGN}.pdf

TEX     	= pdflatex
TEXOPTS 	= -halt-on-error

BIBTEX  	= bibtex

# if your open prorgram isn't listed, OR (||) it to the end
open: ${PDF}
	open $< || gnome-open $<

${PDF}: ${MAIN_TEX} ${PARTS_TEX} ${FIGURES} ${BIBFILES} ${STYLES_STY}

# should probably use a tool like rubber, but this works
%.pdf:	%.tex
	${TEX} ${TEXOPTS} $(basename $<)
	${BIBTEX} $(basename $<) || ${TEX} ${TEXOPTS} $(basename $<)
	${TEX} ${TEXOPTS} $(basename $<)
	${TEX} ${TEXOPTS} $(basename $<)

# add stuff to delete here
clean:
	rm -f *.log *.aux *.dvi *.blg *.bbl ${PDF}
