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
    else
        python3 get_publis_ads.py --fr --keepbib
    fi
else
    echo '--fr not set: compiling in english'
    echo '\frenchfalse' > ./lang.tex
    if [[ $UPDATE == 1 ]]; then
        python3 get_publis_ads.py
    else
        python3 get_publis_ads.py --keepbib
    fi
fi

latexmk -bibtex-cond -pdfxe -pv cv.tex
latexmk -bibtex-cond -pdfxe -c cv.tex

cp cv.pdf CV_Florian_Keruzore.pdf
