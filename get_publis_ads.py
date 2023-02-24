import os
import requests
import json
import datetime
import argparse

"""
Create a tex-friendly publication list for a resume.
The publications are queried from custom NASA ADS libraries.

Creates
-------
- cv.bib: a bibtex file with all my publications
- section_publis.tex: a tex file citing all publications
    in categories

Options
-------
--keepbib: if you don't want to overwrite the .bib
--fr: if you want the added text to be in French
"""

parser = argparse.ArgumentParser()
parser.add_argument(
    "--keepbib",
    default=False,
    help="Don't overwrite the existing cv.bib file",
    action="store_true",
)
parser.add_argument(
    "--fr",
    default=False,
    help="Make the text French",
    action="store_true",
)
args = parser.parse_args()
path = "./contents_FR" if args.fr else "./contents_EN"

token = os.environ["ADS_DEV_KEY"]
secu_header = {"Authorization": f"Bearer {token}"}


def get_lib_contents(lib_suffix):
    headers = {**secu_header}
    req = requests.get(
        f"https://api.adsabs.harvard.edu/v1/biblib/libraries/{lib_suffix}",
        headers=headers,
        params={"rows": 2000},
    )
    return req.json()


def bibcode_to_bibtex(bibcodes):
    headers = {**secu_header, "Content-Type": "application/json"}
    req = requests.post(
        "https://api.adsabs.harvard.edu/v1/export/bibtex",
        headers=headers,
        data=json.dumps({"bibcode": bibcodes}),
    )
    return req.json()


def get_article_metadata(bibcode):
    headers = {**secu_header, "Content-Type": "application/json"}
    req = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?q=bibcode%3A"
        + bibcode.replace("&", "%26")
        + "&fl=author&rows=1",
        headers=headers,
    )
    return req.json()


# Get the juice
my_lib_suffixes = {
    "all": "nRvPlljgQNeGQ_oIrz9xJQ",
    "fa_papers": "ZuQy1squRhGoEy1UH3Rmzw",
    "fa_procs": "v5q90osZRHeZGRRr9u5IuQ",
    "co_papers": "gY6xFfpeTKydtilcHY0qZQ",
    "co_procs": "AoCYUV5QTAm3NjEIKVLMCg",
}
my_pubs = get_lib_contents(my_lib_suffixes["all"])
my_bibcodes = {
    k: get_lib_contents(v)["documents"] for k, v in my_lib_suffixes.items()
}

# Write .bib file
my_bibtexs_all = bibcode_to_bibtex(my_pubs["documents"])
if args.keepbib:
    print("Conserving current bib file")
else:
    bib_file = f"{path}/cv.bib"
    print(f"Writing {bib_file}...")
    with open(bib_file, "w") as f:
        # Start with thesis entry, not in ADS
        f.write(
            """@PHDTHESIS{keruz2021,
    url = "http://www.theses.fr/2021GRALY050",
    title = "Cosmologie à partir des observations Sunyaev-Zeldovich d'amas de galaxies avec NIKA2",
    author = "Kéruzoré, Florian",
    year = "2021",
    note = "Thèse de doctorat dirigée par Mayet, Frédéric Physique subatomique et astroparticules Université Grenoble Alpes 2021",
    note = "2021GRALY050",
    url = "http://www.theses.fr/2021GRALY050/document",
    }"""
        )
        f.write("\n\n")
        f.write(my_bibtexs_all["export"])

# Write .tex file
tex_file = f"{path}/section_publis.tex"
print(f"Writing {tex_file}...")
with open(tex_file, "w") as f:
    f.write("\\section{Publications}\n")
    n_papers = len(my_bibcodes["co_papers"]) + len(my_bibcodes["fa_papers"])
    n_procs = len(my_bibcodes["co_procs"]) + len(my_bibcodes["fa_procs"])

    print(
        f"{n_papers + n_procs} publications found:",
        f"{n_papers} papers, {n_procs} proceedings",
    )
    # Overhead: publication counts
    if args.fr:
        today = datetime.date.today().strftime("%d/%m/%Y")
        f.write(
            f"\\textbf{{{n_papers}}} "
            + "publications dans des revues à comité de lecture, "
            + f"\\textbf{{{n_procs}}} dans des actes de congrès "
            + f"({today}).\n"
        )
    else:
        today = datetime.date.today().strftime("%m-%d-%Y")
        f.write(
            f"\\textbf{{{n_papers}}} "
            + "publications in peer-reviewed journals, "
            + f"\\textbf{{{n_procs}}} conference proceedings "
            + f"({today}).\n"
        )

    # Papers
    if args.fr:
        f.write(
            "\n\\subsection{Articles dans des revues à comité de lecture}\n"
        )
    else:
        f.write("\n\\subsection{Peer-reviewed articles}\n")

    for bibcode in my_bibcodes["fa_papers"]:
        f.write("\n\\tabitem \\fullcite{" + bibcode + "}\n")
    for bibcode in my_bibcodes["co_papers"]:
        f.write("\n\\tabitem \\fullcite{" + bibcode + "}\n")

    # Proceedings
    if args.fr:
        f.write("\n\\subsection{Actes de conférence}")
    else:
        f.write("\n\\subsection{Conference proceedings}")

    for bibcode in my_bibcodes["fa_procs"]:
        f.write("\n\\tabitem \\fullcite{" + bibcode + "}\n")
    n_proc = len(my_bibcodes["co_procs"])
    if args.fr:
        f.write(
            f"\n$+$ \\textbf{{{n_proc}}} actes de conférences "
            + f"en tant que co-auteur ({today}).\n"
        )
    else:
        f.write(
            f"\n$+$ \\textbf{{{n_proc}}} conference proceedings as co-author "
            + f"({today}).\n"
        )

    # Thesis
    if args.fr:
        f.write("\n\\subsection{Thèse de Doctorat}\n")
        f.write("\\fullcite{keruz2021}, ")
        f.write(
            "\\href{https://raw.githubusercontent.com/fkeruzore/"
            + "PhDThesis-public/main/manuscrit.pdf}{Manuscrit}\n"
        )
    else:
        f.write("\n\\subsection{Doctorate thesis}\n")
        f.write("\\fullcite{keruz2021}, ")
        f.write(
            "\\href{https://raw.githubusercontent.com/fkeruzore/"
            + "PhDThesis-public/main/manuscrit.pdf}{Manuscript (in french)}\n"
        )
