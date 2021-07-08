#!/usr/bin/env bash

LANGUAGE=(
  "en_US"
  "fr_FR"
)
CFG="babel.cfg"
LOCALE_DIR="locale"
MESSAGE="${LOCALE_DIR}/messages.pot"

pybabel extract --omit-header -F "${CFG}" -o "${MESSAGE}" .

for i_lang in "${LANGUAGE[@]}"
do
  if ! [[ -d "${LOCALE_DIR}/${i_lang}" ]]
  then
    pybabel init -i "${MESSAGE}" -l "${i_lang}" -d "${LOCALE_DIR}"
  fi
done

# Update the PO template
pybabel extract --omit-header -F "${CFG}" -o "${MESSAGE}" .

# Update the associated PO catalogs
for i_lang in "${LANGUAGE[@]}"
do
  pybabel update --omit-header -i "${MESSAGE}" -l "${i_lang}" -d "${LOCALE_DIR}"
done

