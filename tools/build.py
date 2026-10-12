#!/usr/bin/env python3
"""Generate the 13 static pages using only the Python standard library.

Run from anywhere: python3 /path/to/light-lattice/tools/build.py
Edit data/site.json and assets/style.css; do not edit generated HTML.
"""
import json
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
ALGORITHMS = DATA["algorithms"]
CSS_VERSION = sha256((ROOT / "assets/style.css").read_bytes()).hexdigest()[:12]


def e(value):
    return escape(str(value), quote=True)


ARROW = '<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
DOWNLOAD = '<svg class="arrow-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3v12m-4-4 4 4 4-4M5 16v4h14v-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MARK = '<svg viewBox="0 0 38 40" fill="none" aria-hidden="true"><path d="M7 29 14 9M17 32 24 12M27 35 34 15M7 29l20 6M10.5 19l20 6M14 9l20 6" stroke="#9aafd0" stroke-width="1.1"/><g fill="#245cce"><circle cx="7" cy="29" r="2.5"/><circle cx="14" cy="9" r="2.5"/><circle cx="24" cy="12" r="2.5"/><circle cx="34" cy="15" r="2.5"/><circle cx="17" cy="32" r="2.5"/><circle cx="27" cy="35" r="2.5"/><circle cx="10.5" cy="19" r="2.5"/><circle cx="20.5" cy="22" r="3.4"/><circle cx="30.5" cy="25" r="2.5"/></g></svg>'
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="6" fill="#162b40"/><path d="M10 29 16 9m4 22 6-20M10 29l20 6M13 19l20 6M16 9l20 6" stroke="#83a5ec" stroke-width="1.5"/><g fill="white"><circle cx="10" cy="29" r="2.7"/><circle cx="16" cy="9" r="2.7"/><circle cx="20" cy="32" r="2.7"/><circle cx="26" cy="12" r="2.7"/><circle cx="23" cy="22" r="3"/></g></svg>'
FILE_ICON = '<svg class="document-icon" viewBox="0 0 38 48" fill="none" aria-hidden="true"><path d="M5 2h18l10 10v33H5V2Z" stroke="currentColor" stroke-width="1.3"/><path d="M23 2v11h10M11 23h16M11 29h16M11 35h10" stroke="currentColor" stroke-width="1.3"/></svg>'
CODE_ICON = '<svg class="document-icon" viewBox="0 0 38 48" fill="none" aria-hidden="true"><rect x="2" y="6" width="34" height="34" rx="3" stroke="currentColor" stroke-width="1.3"/><path d="m12 18-5 5 5 5m14-10 5 5-5 5m-4-14-6 20" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def lattice():
    """An abstract two-dimensional lattice, not a security/performance plot."""
    lines, dots = [], []
    def point(i, j):
        return 33 + 42*i + 15*j, 217 + 10*i - 34*j
    for i in range(6):
        x1,y1 = point(i,0); x2,y2 = point(i,5)
        lines.append(f'<path d="M{x1} {y1}L{x2} {y2}"/>')
    for j in range(6):
        x1,y1 = point(0,j); x2,y2 = point(5,j)
        lines.append(f'<path d="M{x1} {y1}L{x2} {y2}"/>')
    for i in range(6):
        for j in range(6):
            x,y = point(i,j)
            dots.append(f'<circle cx="{x}" cy="{y}" r="{2.6 if 1<i<5 and 0<j<4 else 2}"/>')
    x,y = point(2,2); bx,by=point(3,2); cx,cy=point(2,3); dx,dy=point(3,3)
    def basis_label(lx, ly, index):
        return f'''<g class="basis-label" aria-label="b {index}">
<text x="{lx}" y="{ly}" fill="#245cce" font-family="Georgia,serif" font-size="16" font-style="italic">b<tspan baseline-shift="sub" font-size="10" font-style="normal">{index}</tspan></text>
</g>'''
    return f'''<figure class="lattice-figure" aria-label="An abstract two-dimensional lattice">
<svg viewBox="0 0 380 304" role="img" aria-labelledby="lattice-title">
<title id="lattice-title">Lattice points with two basis vectors, vector b one and vector b two</title>
<defs><marker id="basis-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#245cce"/></marker></defs>
<polygon class="basis-cell" points="{x},{y} {bx},{by} {dx},{dy} {cx},{cy}" fill="#dce8ff" stroke="none"/>
<g stroke="#d7e3f7" stroke-width="1">{''.join(lines)}</g>
<g fill="#86a3d8">{''.join(dots)}</g>
<g class="basis-vectors" fill="none" stroke="#245cce" stroke-width="2" marker-end="url(#basis-arrow)"><path d="M{x} {y}L{bx} {by}"/><path d="M{x} {y}L{cx} {cy}"/></g>
<circle cx="{x}" cy="{y}" r="4" fill="#245cce"/>
{basis_label(bx+8,by+23,1)}
{basis_label(cx-22,cy-2,2)}
</svg><figcaption class="lattice-caption">LATTICE FOUNDATIONS / LIGHTWEIGHT DESIGN</figcaption></figure>'''


def shell(title, description, body, active=None, subpage="home"):
    prefix = "../" if active else ""
    root_current = ' aria-current="page"' if not active else ''
    nav = [f'<li><a href="{prefix}index.html"{root_current}>Overview</a></li>']
    for a in ALGORITHMS:
        current = ''
        if a["slug"] == active:
            current = ' aria-current="page"' if subpage == "home" else ' aria-current="true"'
        nav.append(f'<li><a href="{prefix}{a["slug"]}/index.html"{current}>{e(a["name"])}</a></li>')
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#162b40">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(FAVICON, safe='')}">
  <link rel="stylesheet" href="{prefix}assets/style.css?v={CSS_VERSION}">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="masthead">
  <div class="container masthead-inner">
    <a class="brand" href="{prefix}index.html" aria-label="light-lattice home">{MARK}<span class="brand-name">light-lattice</span></a>
    <p class="masthead-note"><span>A Lightweight Lattice Cryptography Suite</span>Signatures · Encapsulation · Key Exchange</p>
  </div>
  <nav class="primary-nav" aria-label="Suite navigation"><ul class="container">{''.join(nav)}</ul></nav>
</header>
<main id="main" class="container" tabindex="-1">{body}</main>
<footer class="container footer"><a class="footer-brand" href="{prefix}index.html">light-lattice</a><div class="footer-info"><p class="copyright">Copyright © <a href="https://sklois.cn/">State Key Laboratory of Cyberspace Security Defense, Institute of Information Engineering, CAS</a>. All rights reserved.</p></div></footer>
</body>
</html>
'''


def page_top(a, page):
    tabs = []
    for key, label, file in [("home","Home","index.html"),("specification","Specification","specification.html"),("implementation","Implementation","implementation.html")]:
        current = ' aria-current="page"' if page == key else ''
        tabs.append(f'<a href="{file}"{current}>{label}</a>')
    full_name = ''.join(f'<span class="name-accent">{e(text)}</span>' if accent else e(text) for text,accent in a['long_name_parts'])
    return f'''<div class="page-top"><p class="eyebrow">{e(a['type'])}</p><h1>{e(a['name'])}</h1><p class="page-subtitle">{full_name}</p></div>
<nav class="secondary-nav" aria-label="{e(a['name'])} pages">{''.join(tabs)}</nav>'''


def facts(a):
    """Identical sidebar on all three pages for a given algorithm."""
    pairs = [("Primitive",a["type"]),("Foundation",a["foundation"]),("Design Focus",a["design_focus"]),("Structure",a["structure"])]
    title = 'At a Glance'
    def phrases(value):
        parts = value.split(' · ')
        return ' '.join(f'<span class="fact-phrase">{e(part)}{" ·" if i < len(parts)-1 else ""}</span>' for i,part in enumerate(parts))
    entries = ''.join(f'<dt>{e(k)}</dt><dd>{phrases(v)}</dd>' for k,v in pairs)
    return f'<aside><section class="facts"><h2>{title}</h2><dl>{entries}</dl></section></aside>'


def home():
    rows = []
    for i,a in enumerate(ALGORITHMS,1):
        rows.append(f'''<li><a class="algorithm-row" href="{a['slug']}/index.html"><span class="row-index">{i:02d}</span><span class="row-title"><span class="row-name">{e(a['name'])}</span><span class="row-type">{e(a['type'])}</span></span><span class="row-summary">{e(a['summary'])}</span>{ARROW}</a></li>''')
    body = f'''<section class="home-hero" aria-labelledby="suite-title"><div><p class="eyebrow">The light-lattice suite</p><h1 id="suite-title">A lightweight approach<br>to <em>lattice cryptography.</em></h1><p class="intro">{e(DATA['intro'])}</p></div>{lattice()}</section>
<section aria-labelledby="algorithms-title"><div class="section-heading"><h2 id="algorithms-title">Four algorithms. One suite.</h2></div><ol class="algorithm-list">{''.join(rows)}</ol></section>'''
    (ROOT / 'index.html').write_text(shell('light-lattice — Lightweight lattice cryptography', DATA['description'], body), encoding='utf-8')


def algorithm_home(a):
    features = ''.join(f'<li class="feature"><span class="feature-number">{i:02d}</span><div><h3>{e(title)}</h3><p>{e(text)}</p></div></li>' for i,(title,text) in enumerate(a['features'],1))
    return page_top(a,'home')+f'''<div class="content-grid"><article><h2>Introduction</h2><p class="lead">{e(a['intro'])}</p><ol class="features">{features}</ol><div class="actions"><a class="button" href="specification.html">Specification {ARROW}</a><a class="button" href="implementation.html">Implementation {ARROW}</a></div></article>{facts(a)}</div>'''


def release_path(entry, kind):
    """Path relative to an algorithm directory, using the release date."""
    directory, key = ('specifications', 'pdf') if kind == 'specification' else ('implementations', 'archive')
    released = date.fromisoformat(entry['date'])
    if entry['date'] != released.isoformat():
        raise ValueError('Release dates must use YYYY-MM-DD')
    filename = entry[key]
    if not filename or filename in ('.', '..') or Path(filename).name != filename or '\\' in filename:
        raise ValueError(f'{key} must contain a filename only: {filename!r}')
    return Path(directory) / released.strftime('%Y%m%d') / filename


def release_url(entry, kind):
    return quote(release_path(entry, kind).as_posix())


def history_table(a, entries, kind):
    """Shared history layout; each row retains its own downloadable file."""
    key = 'pdf' if kind == 'specification' else 'archive'
    rows = ''.join(f'<tr><td><time datetime="{e(entry["date"])}">{e(entry["date"])}</time></td><td>{e(entry["description"])}</td><td><a class="version-link" href="{e(release_url(entry,kind))}" download="{e(entry[key])}" aria-label="Download {e(a["name"])} {kind}, {e(entry["version"])}">{e(entry["version"])}</a></td></tr>' for entry in entries)
    return f'<section class="history" aria-labelledby="history-title"><h3 id="history-title">History</h3><table class="history-table" aria-labelledby="history-title"><thead><tr><th scope="col">Date</th><th scope="col">Description</th><th scope="col">Version</th></tr></thead><tbody>{rows}</tbody></table></section>'


def specification(a):
    history = sorted(a['history'], key=lambda entry: entry['date'], reverse=True)
    current = a['current'] if 'current' in a else history[0]
    description = a.get('current', {}).get('description', f"The full {a['name']} specification, including construction details, parameter choices, and security analysis.")
    pdf = e(release_url(current,'specification'))
    size = (ROOT/a['slug']/release_path(current,'specification')).stat().st_size/1024/1024
    return page_top(a,'specification')+f'''<div class="content-grid"><article><h2>Specification</h2><p class="body-copy">{e(description)}</p><div class="document">{FILE_ICON}<div><h3>{e(a['name'])} specification</h3><p>Date: <time datetime="{e(current['date'])}">{e(current['date'])}</time><br>PDF · {current['pages']} pages · {size:.1f} MB</p><div class="actions"><a class="button" href="{pdf}">Open PDF {ARROW}</a><a class="text-link" href="{pdf}" download="{e(current['pdf'])}">Download {DOWNLOAD}</a></div></div></div>{history_table(a,history,'specification')}</article>{facts(a)}</div>'''


def implementation(a):
    package = a['implementation']
    history = sorted(package['history'], key=lambda entry: entry['date'], reverse=True)
    current = package['current'] if 'current' in package else history[0]
    description = package.get('current', {}).get('description', package['description'])
    archive = e(release_url(current,'implementation'))
    size = (ROOT/a['slug']/release_path(current,'implementation')).stat().st_size/1024/1024
    return page_top(a,'implementation')+f'''<div class="content-grid"><article><h2>Implementation</h2><p class="body-copy">{e(description)}</p><div class="document">{CODE_ICON}<div><h3>{e(a['name'])} source package</h3><p>Date: <time datetime="{e(current['date'])}">{e(current['date'])}</time><br>ZIP · {size:.1f} MB</p><div class="actions"><a class="button" href="{archive}" download="{e(current['archive'])}">Download source {DOWNLOAD}</a></div></div></div>{history_table(a,history,'implementation')}</article>{facts(a)}</div>'''


def main():
    # Validate all release files before overwriting any generated pages.
    for a in ALGORITHMS:
        if ''.join(text for text,_ in a['long_name_parts']) != a['long_name']:
            raise ValueError(f"{a['name']}: full-name segments must preserve the documented name")
        highlight = a.get('long_name_highlight', a['name'])
        if ''.join(text for text,accent in a['long_name_parts'] if accent) != highlight:
            raise ValueError(f"{a['name']}: highlighted letters must spell {highlight}")
        for releases,kind in [(a,'specification'),(a['implementation'],'implementation')]:
            # An explicit current release leaves the historical records intact.
            entries = list(releases['history'])
            if 'current' in releases:
                entries.append(releases['current'])
            if not entries:
                raise ValueError(f"{a['name']}: at least one {kind} release entry is required")
            seen = set()
            for entry in entries:
                path = ROOT/a['slug']/release_path(entry,kind)
                if path in seen:
                    raise ValueError(f"{a['name']}: duplicate release file {path.relative_to(ROOT)}")
                seen.add(path)
                if not path.is_file():
                    raise FileNotFoundError(path.relative_to(ROOT))
    home()
    for a in ALGORITHMS:
        target = ROOT/a['slug']
        target.mkdir(exist_ok=True)
        for key, file, render in [('home','index.html',algorithm_home),('specification','specification.html',specification),('implementation','implementation.html',implementation)]:
            title = f"{a['name']} — {key.title()} · light-lattice"
            (target/file).write_text(shell(title,a['summary'],render(a),a['slug'],key),encoding='utf-8')
        # Remove the superseded generated page when upgrading an older checkout.
        (target/'algorithm.html').unlink(missing_ok=True)
    (ROOT/'.nojekyll').touch()
    print('Generated 13 static pages. Preview: python3 -m http.server 8000 --bind 127.0.0.1')


if __name__ == '__main__':
    main()
