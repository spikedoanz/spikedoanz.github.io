#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import os
import gzip


HEADER="""
---
title: anime reviews
---

### [[index|supaiku dot com]]

<h1 href="" onclick="document.getElementById('darkmode-toggle').click(); return false;">
anime reviews
</h1>


---
> this page contains a compilation of my anime reviews. it is compiled from my [myanimelist](https://myanimelist.net/profile/spikedoanzz). reviews are sorted by rating, then alphabetically within ratings.
>
> many of the factors impacting my reviews are largely external to the shows themselves. all are excellent in their own right, but the best are often colored by the when and where they found me.
---
"""

PREAMBLE={
        10: """
## 10/10
---
>excellent shows that are at once deeply thought provoking, personal, and culturally foundational.
---

""",
        9: """
## 9/10
---
>amazing, even flawless shows, which nonetheless lack that special spark that would otherwise make them masterpieces.
---

""",
}

def parse_anime_list(xml_content):
    root = ET.fromstring(xml_content)
    anime_list = defaultdict(list)
    for anime in root.findall('.//anime'):
        title = anime.find('series_title').text.strip('"')
        score = int(anime.find('my_score').text)
        notes = anime.find('my_comments').text
        
        if score > 0:  # Only include anime with a score
            anime_list[score].append((title, notes))
    return anime_list

def generate_markdown(anime_list):
    toc = ""
    notes_section = ""
    for score in range(10, 8, -1):
        if score in PREAMBLE.keys():
            toc += PREAMBLE[score]
        if score in anime_list:
            for title, notes in sorted(anime_list[score], key=lambda x: re.sub(r'^(a|an|the)\s+', '', x[0].lower())):
                if notes and notes.strip():
                    safe_title = re.sub(r'[^\w\- ]', '', title).replace(' ', '-').lower()
                    toc += f"* [{title}](#{safe_title})\n"
                    notes_section += f"\n## {title}\n"
                    notes_section += "---\n"
                    notes_section += f"{notes.strip()}\n\n"
                else:
                    toc += f"* {title}\n"
            
            toc += "\n"

    ret = "" 
    ret += toc
    ret += notes_section
    return toc + notes_section

# __main__
# Find the newest XML or gzipped XML file in the exports directory
exports_dir = 'utils/mal/exports'
xml_files = sorted([f for f in os.listdir(exports_dir) if f.endswith('.xml') or f.endswith('.xml.gz')], reverse=True)

if not xml_files:
    print("No XML or gzipped XML files found in the exports directory.")
    exit(1)

xml_file = os.path.join(exports_dir, xml_files[0])

# Read the XML content from the file, handling gzip if necessary
if xml_file.endswith('.gz'):
    with gzip.open(xml_file, 'rt', encoding='utf-8') as file:
        xml_content = file.read()
else:
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()

# Parse the anime list
anime_list = parse_anime_list(xml_content)

# Generate the markdown
markdown_output = ""
markdown_output += HEADER
markdown_output += generate_markdown(anime_list)

# Write the markdown to a file
name = 'content/anime-reviews.md'
with open(name, 'w', encoding='utf-8') as file:
    file.write(markdown_output)

print(f"Markdown file {name} has been generated using : {xml_file}")
