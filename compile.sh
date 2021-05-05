#!/usr/bin/env bash

LANGUAGE=(
  "en_US"
  "fr_FR"
)
LOCALE_DIR="locale"

pybabel compile -d ${LOCALE_DIR} -f

./main.py

cd tex || exit 1

for i_lang in "${LANGUAGE[@]}"
do
  lualatex resume.${i_lang}.tex
  pdfconvert_blackandwhite.sh resume.${i_lang}.pdf
  mv output.pdf resume.${i_lang}.bw.pdf
done
cd ../ || exit 1