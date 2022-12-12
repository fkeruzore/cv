#!/usr/bin/env bash
if [[ $1 == '--update-publis' ]]; then
    echo $1 'set: updating publication list...'
    ./get_publis_ads.py
else
    echo $1 'not set: keep publication list as is'
fi

latexmk -bibtex-cond -pdfxe -pv cv.tex
latexmk -bibtex-cond -pdfxe -c cv.tex

cp cv.pdf CV_Florian_Keruzore.pdf
