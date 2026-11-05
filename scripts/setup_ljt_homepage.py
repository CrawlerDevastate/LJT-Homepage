#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
from string import Template

ROOT = Path.cwd()


def write_text(rel, content):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def remove_path(rel):
    path = ROOT / rel
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def yaml_scalar(value):
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False)


def set_line(lines, key, value, indent=0):
    expected_leading = " " * indent
    for i, line in enumerate(lines):
        stripped = line.lstrip(" ")
        leading = line[: len(line) - len(stripped)]
        if leading == expected_leading and stripped.startswith(key + ":"):
            new_line = (leading + key + ": " + yaml_scalar(value)).rstrip() + "\n"
            lines[i] = new_line
            return
    raise RuntimeError("Missing config key: " + expected_leading + key)


# Update site-wide Jekyll configuration.
config_path = ROOT / "_config.yml"
config_lines = config_path.read_text(encoding="utf-8").splitlines(keepends=True)

set_line(config_lines, "title", "Junteng Liu")
set_line(config_lines, "name", "Junteng Liu")
set_line(
    config_lines,
    "description",
    "Junteng Liu is a first-year PhD candidate at HKUST NLP Group.",
)
set_line(config_lines, "url", "https://crawlerdevastate.github.io")
set_line(config_lines, "baseurl", "/LJT-Homepage")
set_line(config_lines, "repository", "CrawlerDevastate/LJT-Homepage")
set_line(config_lines, "og_image", None)

author_values = [
    ("avatar", None),
    ("name", "Junteng Liu"),
    (
        "bio",
        "First-year PhD candidate at HKUST NLP Group. Research focuses on natural language processing and machine learning.",
    ),
    ("location", None),
    ("employer", "Hong Kong University of Science and Technology"),
    ("uri", None),
    ("email", "jliugi@connect.ust.hk"),
    (
        "googlescholar",
        "https://scholar.google.com/citations?hl=en&user=tbK9jl4AAAAJ&view_op=list_works&sortby=pubdate",
    ),
    ("orcid", None),
    ("pubmed", None),
    ("github", "Vicent0205"),
    ("bluesky", None),
    ("twitter", "junteng88716710"),
]
for key, value in author_values:
    set_line(config_lines, key, value, indent=2)

for i, line in enumerate(config_lines):
    if line.strip() == "title: 'Journal Articles'":
        config_lines[i] = line.replace("Journal Articles", "Preprints")
        break
else:
    raise RuntimeError("Journal Articles publication category was not found")

in_publications = False
for i, line in enumerate(config_lines):
    if line.startswith("  publications:"):
        in_publications = True
    elif in_publications and line.startswith("    output: true"):
        config_lines[i] = line.replace("true", "false")
        break
else:
    raise RuntimeError("publications collection output setting was not found")

config_path.write_text("".join(config_lines), encoding="utf-8")

# Hide the sidebar avatar block when no profile photo is available in memory.
profile_path = ROOT / "_includes" / "author-profile.html"
profile = profile_path.read_text(encoding="utf-8")
avatar_start = profile.index('  <div class="author__avatar">')
avatar_end = profile.index("  </div>", avatar_start) + len("  </div>")
avatar_block = """  {% if author.avatar %}
  <div class="author__avatar">
    {% if author.avatar contains "://" %}
      <img src="{{ author.avatar }}" alt="{{ author.name }}" fetchpriority="high" />
    {% else %}
      <img src="{{ author.avatar | prepend: "/images/" | prepend: base_path }}" class="author__avatar" alt="{{ author.name }}" fetchpriority="high" />
    {% endif %}
  </div>
  {% endif %}"""
profile_path.write_text(profile[:avatar_start] + avatar_block + profile[avatar_end:], encoding="utf-8")

# Navigation and author data.
write_text(
    "_data/navigation.yml",
    """
main:
  - title: "About"
    url: /
  - title: "Publications"
    url: /publications/
""",
)
write_text(
    "_data/authors.yml",
    "# Site author details are maintained through site.author in _config.yml.\n",
)

# Remove sample/demo content that is not supported by the memory record.
sample_dirs = [
    "_drafts",
    "_portfolio",
    "_posts",
    "_talks",
    "_teaching",
    "talkmap",
    "files",
    "markdown_generator",
    "images/wiki",
]
for rel in sample_dirs:
    remove_path(rel)

sample_files = [
    "_pages/archive-layout-with-content.md",
    "_pages/cv.md",
    "_pages/markdown.md",
    "_pages/non-menu-page.md",
    "_pages/portfolio.html",
    "_pages/talkmap.html",
    "_pages/talks.html",
    "_pages/teaching.html",
    "_pages/year-archive.html",
    "_pages/category-archive.html",
    "_pages/collection-archive.html",
    "_pages/page-archive.html",
    "_pages/tag-archive.html",
    "_pages/terms.md",
    "_pages/sitemap.md",
    "talkmap.ipynb",
    "talkmap_out.ipynb",
    "talkmap.py",
    "images/bio-photo.jpg",
    "images/bio-photo-2.jpg",
    "images/profile.png",
    "images/editing-talk.png",
    "images/500x300.png",
]
for rel in sample_files:
    remove_path(rel)

files_dir = ROOT / "files"
files_dir.mkdir(exist_ok=True)
(files_dir / ".gitkeep").write_text("", encoding="utf-8")

# Publication records from memory.
publications = [
    {
        "slug": "synlogic",
        "title": "SynLogic: Synthesizing Verifiable Reasoning Data at Scale for Learning Logical Reasoning and Beyond",
        "authors": "Junteng Liu, Yuanxiang Fan, Zhuo Jiang, Han Ding, Yongyi Hu, Chi Zhang, Yiqi Shi, Shitong Weng, Aili Chen, Shiqi Chen, Yunan Huang, Mozhi Zhang, Pengyu Zhao, Junjie Yan, Junxian He",
        "venue": "arXiv",
        "year": 2025,
        "date": "2025-01-01",
        "category": "manuscripts",
        "role": "First author.",
        "note": "GitHub code repository available.",
    },
    {
        "slug": "perception-bottleneck-vlm-chart-understanding",
        "title": "On the Perception Bottleneck of VLMs for Chart Understanding",
        "authors": "Junteng Liu, Weihao Zeng, Xiwen Zhang, Yijun Wang, Zifei Shan, Junxian He",
        "venue": "arXiv",
        "year": 2025,
        "date": "2025-01-01",
        "category": "manuscripts",
        "role": "First author.",
        "note": "GitHub code repository: Vision4Chart.",
    },
    {
        "slug": "universal-truthfulness-hyperplane",
        "title": "On the Universal Truthfulness Hyperplane Inside LLMs",
        "authors": "Junteng Liu, Shiqi Chen, Yu Cheng, Junxian He",
        "venue": "EMNLP 2024",
        "year": 2024,
        "date": "2024-01-01",
        "category": "conferences",
        "role": "First author.",
        "note": "GitHub code repository: Universal_Truthfulness_Hyperplane.",
    },
    {
        "slug": "in-context-sharpness-alerts",
        "title": "In-Context Sharpness as Alerts: An Inner Representation Perspective for Hallucination Mitigation",
        "authors": "Shiqi Chen, Miao Xiong, Junteng Liu, Zhengxuan Wu, Teng Xiao, Siyang Gao, Junxian He",
        "venue": "ICML 2024",
        "year": 2024,
        "date": "2024-01-01",
        "category": "conferences",
        "role": "Co-author.",
        "note": "",
    },
    {
        "slug": "c-eval",
        "title": "C-Eval: A Multi-Level Multi-Discipline Chinese Evaluation Suite for Foundation Models",
        "authors": "Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, Junteng Liu, Chuancheng Lv, Yikai Zhang, Jiayi Lei, Yao Fu, Maosong Sun, Junxian He",
        "venue": "NeurIPS 2023",
        "year": 2023,
        "date": "2023-01-01",
        "category": "conferences",
        "role": "Co-author.",
        "note": "",
    },
    {
        "slug": "composing-parameter-efficient-modules",
        "title": "Composing Parameter-Efficient Modules with Arithmetic Operations",
        "authors": "Jinghan Zhang, Shiqi Chen, Junteng Liu, Junxian He",
        "venue": "NeurIPS 2023",
        "year": 2023,
        "date": "2023-01-01",
        "category": "conferences",
        "role": "Co-author.",
        "note": "",
    },
]

pub_dir = ROOT / "_publications"
pub_dir.mkdir(exist_ok=True)
for old_file in pub_dir.glob("*.md"):
    old_file.unlink()


def publication_note(pub):
    return " ".join(part for part in [pub["role"], pub.get("note", "")] if part)


for pub in publications:
    citation = f'{pub["authors"]}. “{pub["title"]}.” {pub["venue"]}, {pub["year"]}.'
    excerpt = f'{publication_note(pub)} {pub["venue"]}, {pub["year"]}.'
    front_matter = f'''---
title: {json.dumps(pub["title"], ensure_ascii=False)}
collection: publications
category: {pub["category"]}
permalink: /publications/{pub["slug"]}/
excerpt: {json.dumps(excerpt, ensure_ascii=False)}
date: {pub["date"]}
venue: {json.dumps(pub["venue"], ensure_ascii=False)}
citation: {json.dumps(citation, ensure_ascii=False)}
---
'''
    body = f"""{citation}

{publication_note(pub)}
"""
    write_text(f'_publications/{pub["slug"]}.md', front_matter + "\n" + body)


def markdown_publication(pub, index):
    return (
        f'{index}. {pub["authors"]}. **{pub["title"]}.** '
        f'*{pub["venue"]}, {pub["year"]}.* {publication_note(pub)}'
    )


markdown_publications = "\n\n".join(
    markdown_publication(pub, index)
    for index, pub in enumerate(publications, start=1)
)

about_content = f"""---
permalink: /
title: "Junteng Liu"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am a first-year PhD candidate at the **HKUST NLP Group**, Hong Kong University of Science and Technology. I graduated from Shanghai Jiao Tong University (SJTU) in June 2024. My research focuses on natural language processing and machine learning. My research interests include LLM reasoning and reinforcement learning, hallucination in vision-language models (VLMs), and LLM truthfulness and interpretability.

## Academic Background

- **Ph.D. in Computer Science**, Hong Kong University of Science and Technology (2024-Present). Member of the HKUST NLP Group. Supervisor: Professor Junxian He, who also previously advised my undergraduate studies at SJTU.
- **B.Eng.**, Shanghai Jiao Tong University (2020-2024). Graduated in June 2024.

## Research Experience

- **PhD Candidate**, HKUST NLP Group, Hong Kong University of Science and Technology (2024-Present). Supervisor: Professor Junxian He.
- **Research Intern**, MINIMAX (February 2025 - Present).
- **Research Intern**, Tencent WXG (June 2024 - September 2024). Advisor: Zifei Shan.
- **Research Intern**, Shanghai AI Lab (June 2023 - December 2023). Advisor: Prof. Yu Cheng.

## Research Skills and Interests

- Natural language processing
- Machine learning
- LLM reasoning and reinforcement learning
- Hallucination in vision-language models (VLMs)
- LLM truthfulness and interpretability

## Publications

{markdown_publications}

## Honors and Awards

- Zhiyuan Honor Scholarship, Shanghai Jiao Tong University.

## Contact Information

- Email: [jliugi@connect.ust.hk](mailto:jliugi@connect.ust.hk)
- GitHub: [Vicent0205](https://github.com/Vicent0205)
- Google Scholar: [Google Scholar profile](https://scholar.google.com/citations?hl=en&user=tbK9jl4AAAAJ&view_op=list_works&sortby=pubdate)
- X (Twitter): [@junteng88716710](https://twitter.com/junteng88716710)
"""
write_text("_pages/about.md", about_content)

preprints = [pub for pub in publications if pub["category"] == "manuscripts"]
conference_papers = [pub for pub in publications if pub["category"] == "conferences"]


def html_publication(pub):
    return f'''<li class="publication-item">
  <h3 class="archive__item-title" itemprop="headline">{pub["title"]}</h3>
  <p class="archive__item-excerpt" itemprop="description">{pub["authors"]}. <i>{pub["venue"]}, {pub["year"]}</i>. {publication_note(pub)}</p>
</li>'''


html_preprints = "\n".join(html_publication(pub) for pub in preprints)
html_conferences = "\n".join(html_publication(pub) for pub in conference_papers)

publications_page_template = Template("""---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% include base_path %}

<div class="wordwrap">You can also find my articles on <a href="{{ site.author.googlescholar }}">my Google Scholar profile</a>.</div>

<h2>Preprints</h2>
<hr />
<ol class="archive-list publication-list">
$preprints
</ol>

<h2>Conference Papers</h2>
<hr />
<ol class="archive-list publication-list">
$conferences
</ol>
""")
publications_page = publications_page_template.substitute(
    preprints=html_preprints,
    conferences=html_conferences,
)
write_text("_pages/publications.html", publications_page)

# Remove this one-time setup script after the site files have been generated.
script_path = Path(__file__).resolve()
if script_path.exists():
    script_path.unlink()

print("LJT homepage setup complete.")
