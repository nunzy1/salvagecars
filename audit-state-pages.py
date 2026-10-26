#!/usr/bin/env python3
"""Read-only structural audit of SalvageCars.com state pages.
Usage: python3 audit-state-pages.py [public/states | states.zip] [--output report.md]
Requires: pip install beautifulsoup4
"""
import argparse, collections, pathlib, re, zipfile
from bs4 import BeautifulSoup

def pages(path):
    path=pathlib.Path(path)
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path) as archive:
            for name in sorted(archive.namelist()):
                parts=pathlib.PurePosixPath(name).parts
                if len(parts)==3 and parts[-1]=='index.html' and parts[0]=='states' and not parts[1].startswith('.'):
                    yield parts[1], archive.read(name).decode('utf-8-sig'), name
    else:
        for file in sorted(path.glob('*/index.html')):
            yield file.parent.name, file.read_text(encoding='utf-8-sig'), str(file)

def section_by_heading(soup, heading):
    for h in soup.find_all(['h2','h3']):
        if heading in ' '.join(h.stripped_strings).lower():
            return h.find_parent(['section','aside']), h
    return None, None

def analyze(name, raw):
    soup=BeautifulSoup(raw,'html.parser'); issues=[]
    def add(level, finding): issues.append((level,finding))
    doctype=len(re.findall(r'<!doctype\s+html\s*>',raw,re.I))
    if doctype!=1: add('Fix',f'{doctype} DOCTYPE declarations (expected 1)')
    ids=[tag['id'] for tag in soup.find_all(id=True)]
    for k,v in collections.Counter(ids).items():
        if v>1:add('Fix',f'Duplicate ID #{k} ({v} times)')
    for a in soup.select('a[href^="#"]'):
        target=a.get('href','')[1:]
        if target and target not in ids:add('Fix',f'Broken on-page anchor #{target}')
    for heading in ('what you should know','about this guidance','official '):
        sec,h=section_by_heading(soup,heading)
        if not sec:
            add('Review',f'Cannot locate section headed {heading!r}')
            continue
        if heading=='what you should know':
            # Some older pages put the background on a child wrapper, not section.
            has_white=bool(sec.select_one('.bg-white')) or 'bg-white' in sec.get('class',[]) or bool(re.search(r'background(?:-color)?\s*:\s*(?:white|#fff(?:fff)?)',str(sec),re.I))
            if not has_white:add('Review','What you should know: no explicit white background found (check CSS/template)')
        if heading=='about this guidance' and not sec.get('id'):
            add('Review','About this guidance has no section ID (may be intentional)')
        if heading=='official ':
            links=sec.find_all('a',href=True)
            if not links:add('Fix','Official sources has no links')
            for a in links:
                href=a['href']
                if not href.startswith('https://'):
                    add('Review',f'Official source uses non-HTTPS or relative URL: {href}')
            # Only flag if no descriptions at all; different templates use small or p.
            containers=[a.find_parent(['div','li']) for a in links]
            described=sum(bool(c and (c.find('small') or c.find('p'))) for c in containers)
            if links and described==0:add('Review','Official source links: no adjacent descriptions detected')
            dark=sum('text-slate-900' in a.get('class',[]) for a in links)
            if dark:add('Review',f'{dark} official-source links use text-slate-900 (check link highlighting)')
    return issues

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',nargs='?',default='public/states')
    parser.add_argument('--output',default='state-page-audit.md')
    args=parser.parse_args()
    records=list(pages(args.source))
    if not records:parser.error('No state pages found. Supply public/states or states.zip')
    result=[(name,analyze(name,raw)) for name,raw,_ in records]
    total=sum(len(v) for _,v in result)
    lines=['# SalvageCars.com — State page structural audit','',f'Scanned **{len(records)}** jurisdiction pages. Flagged **{total}** potential findings across **{sum(bool(v) for _,v in result)}** pages.','', '> Read-only heuristic scan. Review findings before editing. It does not verify legal accuracy, external link availability, visual rendering, or navigation targets in other files.','', '## Findings','']
    for name,issues in result:
        if issues:
            lines.append(f'### {name}')
            for level,msg in issues:lines.append(f'- **{level}:** {msg}')
            lines.append('')
    lines+=['## Pages with no findings','',', '.join(name for name,issues in result if not issues) or 'None','']
    pathlib.Path(args.output).write_text('\n'.join(lines),encoding='utf-8')
    print(f'Scanned {len(records)} pages; {total} potential findings across {sum(bool(v) for _,v in result)} pages. Report: {args.output}')
if __name__=='__main__':main()
