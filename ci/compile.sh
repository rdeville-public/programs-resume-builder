#!/usr/bin/env bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TEXPATH="${SCRIPTPATH}/../output/tex/"

cd "${TEXPATH}"
for i_lang in *_*/
do
  latexmk -verbose -pdflatex=lualatex -pdf "${i_lang}resume.tex"
  cp resume.pdf "${i_lang}/Romain_Deville_resume.pdf"
  gs \
    -sOutputFile=${i_lang}/Romain_Deville_resume.bw.pdf\
    -sDEVICE=pdfwrite\
    -sColorConversionStrategy=Gray\
    -dProcessColorModel=/DeviceGray\
    -dCompatibilityLevel=1.4\
    -dNOPAUSE\
    -dBATCH\
    ${i_lang}/Romain_Deville_resume.pdf
  rm -vf \
    *.aux \
    *.bbl \
    *.blg \
    *.log \
    *.out \
    *.idx \
    *.ilg \
    *.ind \
    *.toc \
    *.d \
    *.pdf \
    *.fls \
    *.fdb_latexmk
done