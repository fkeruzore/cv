#!/bin/bash

for i in "$@"; do
  case $i in
    -u|--update)
      UPDATE=1
      shift # past argument with no value
      ;;
    -f|--fr)
      FRENCH=1
      shift # past argument with no value
      ;;
    -*|--*)
      echo "Unknown option $i"
      exit 1
      ;;
    *)
      ;;
  esac
done

if [[ $FRENCH == 1 ]]; then
    echo '--fr set: compiling in french'
    echo '\frenchtrue' > ./lang.tex
    if [[ $UPDATE == 1 ]]; then
        python3 get_publis_ads.py --fr
    fi
    sed -i '' 's/J\. -F\./J\.-F\./g' ./contents_FR/cv.bib
else
    echo '--fr not set: compiling in english'
    echo '\frenchfalse' > ./lang.tex
    if [[ $UPDATE == 1 ]]; then
        python3 get_publis_ads.py
    fi
    sed -i '' 's/J\. -F\./J\.-F\./g' ./contents_EN/cv.bib
fi

latexmk -bibtex-cond -pdfxe -pv cv.tex
latexmk -bibtex-cond -pdfxe -c cv.tex

if [[ $FRENCH == 1 ]]; then
    cp cv.pdf CV_Florian_Keruzore_FR.pdf
else
    cp cv.pdf CV_Florian_Keruzore.pdf
fi
