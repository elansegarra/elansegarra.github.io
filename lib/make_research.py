####################################################
# Filename: make_research.py
# Description: This script generates the resaerch.md
#    file using the information found in the papers
#    table.
# Input(s): papers.csv
# Output:   research.md
####################################################

import pandas as pd

path_to_papers = "lib/papers.csv"
output_path = "research.md"

# Open the papers table
all_papers = pd.read_csv(path_to_papers).fillna("")

# Separate the papers into their different statuses
highlights = all_papers[all_papers.highlight>0].copy()
working = all_papers[(all_papers.highlight==0) & (all_papers.status=="working_paper")].copy()
published = all_papers[(all_papers.highlight==0) & (all_papers.status=="published_paper")].copy()
in_progress = all_papers[(all_papers.highlight==0) & (all_papers.status=="work_in_progress")].copy()
# Check all fell into one of the groups
none_missing = (highlights.shape[0]+working.shape[0]+published.shape[0]+in_progress.shape[0]==all_papers.shape[0])
assert none_missing, "There might be papers that were not categorized properly"

# Personal webpages of coauthors
coauthor_links = {'Anton Babkin':"http://www.antonbabkin.com/",
            'Richard A. Dunn':"https://are.uconn.edu/person/richard-a-dunn-2/",
            'Brent Hueth':"https://www.ers.usda.gov/authors/ers-staff-directory/brent-hueth/",
            # 'Nicole Nestoriak':"",
            'Benjamin Raymond':"https://sites.google.com/site/benjaminwraymond/",
            'Felix Elwert':"https://sociology.wisc.edu/staff/elwert-felix-2/",
            'Diwakar Raisingh':"https://www.raisingh.com/"}

def format_paper_bib(doc_info, style="simple_title_coauthors", bold_title=False):
    # Returns a string of formatted document bib info
    bib = ""
    bold = "**" if bold_title else ""

    if style == "simple_title_coauthors":
        # Prints title and coauthors on first line and rest of bib (if there) on next
        if doc_info['title_link']!="":
            bib += f'{bold}[{doc_info["title"]}]({doc_info["title_link"]}){bold}'
        else:
            bib += f'{bold}{doc_info["title"]}{bold}'
        if doc_info['coauthors']!="":
            bib += f" (with {', '.join(doc_info['coauthors'].split(';'))})"
        if doc_info['status']=="published_paper":
            bib += "\n"
            if doc_info['doc_type']=="article":
                bib+= f"*{doc_info['journal']}*"
                if doc_info['volume']!="": bib+=f", {doc_info['volume']:.0f}({doc_info['issue']:.0f})"
                bib+= f", {doc_info['year']:.0f}."
            elif doc_info['doc_type']=="book_chapter":
                bib += f"In *{doc_info['book_title']}*"
                if doc_info['editors']!="":   bib+= f", {doc_info['editors']} (Eds.)."
                if doc_info['publisher']!="": bib+=f" {doc_info['publisher']}"
                bib+= f", {doc_info['year']:.0f}."
            else:
                raise NotImplementedError(f"Have not implemented bib entry for {doc_info['doc_type']}")
    elif style == "":
        pass
    else:
        raise NotImplementedError(f"Have not implemented style {style}")

    # Adding coauthor links to websites if found
    for coauthor, link in coauthor_links.items():
        bib = bib.replace(coauthor, f"[{coauthor}]({link})")

    return bib

def format_other_links(doc_info):
    res = ""

    for link_key in ['link_1', 'link_2', 'link_3']:
        if doc_info[link_key] != "":
            link_name, link = doc_info[link_key].split(";")
            res += f"[{link_name}]({link})"
    
    return res

# Open and start writing the markdown file with the header
f = open(output_path, "w")
f.write("""---
layout: page
title: Research
sidebar_link: true
sidebar_sort_order: 1
---
""")

# Write the highlights section
f.write("\n### Recent Papers\n")
for ind, paper in highlights.iterrows():
    f.write("\n")
    # Write the main bib info
    main_bib = format_paper_bib(paper, bold_title=True)
    links = format_other_links(paper)
    f.write(main_bib+' '+links if links!="" else main_bib)
    f.write("\n\n")
    # Display a picture is supplied
    if paper['image']!= "":
        f.write(f'<img src="{paper["image"]}" align="left" id="docimg2"/>\n')
    # Display the abstract (must be supplied to be a highlight)
    f.write(f'<p id=docabstract2>Abstract: {paper["abstract"]}</p>\n')

# Write the working papers section
f.write("\n### Working Papers\n")
for ind, paper in working.iterrows():
    f.write("\n")
    # Write the main bib info
    main_bib = format_paper_bib(paper)
    links = format_other_links(paper)
    f.write(main_bib+' '+links if links!="" else main_bib)
    f.write("\n")
    
# Write the published papers section
f.write("\n### Published Papers\n")
for ind, paper in published.iterrows():
    f.write("\n")
    # Write the main bib info
    main_bib = format_paper_bib(paper)
    links = format_other_links(paper)
    f.write(main_bib+' '+links if links!="" else main_bib)
    f.write("\n")

# Write the works in progress section
f.write("\n### Work In Progress\n")
for ind, paper in in_progress.iterrows():
    f.write("\n")
    # Write the main bib info
    f.write(format_paper_bib(paper))
    f.write("\n")

f.close()