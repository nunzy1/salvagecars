#!/usr/bin/env python3
"""Read-only audit of internal links in a static public/ tree. Python 3 stdlib only."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        if tag=='a' and 'href' in attrs: self.links.append(attrs['href'])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', nargs='?', default='public', help='Website root directory (default: public)')
    ap.add_argument('--report', default='site-link-audit.md', help='Markdown report path')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    if not root.is_dir(): ap.error(f'Not a directory: {root}')
    pages={p.relative_to(root).as_posix():p for p in root.rglob('*.html')}
    parsed={}
    for name,p in pages.items():
        parser=PageParser();parser.feed(p.read_text(encoding='utf-8',errors='replace'));parsed[name]=parser
    legacy=[];broken=[];checked=0
    for name,parser in sorted(parsed.items()):
        source=pages[name]
        for href in parser.links:
            url=urlsplit(href)
            if url.scheme or url.netloc or href.startswith('//'): continue
            checked+=1
            path=unquote(url.path)
            target=(root/path.lstrip('/')) if path.startswith('/') else (source.parent/path if path else source)
            target=target.resolve()
            try: relative=target.relative_to(root).as_posix()
            except ValueError:
                broken.append((name,href,'Outside website root'));continue
            if target.is_dir() or not target.suffix:
                target=target/'index.html'
                relative=target.relative_to(root).as_posix()
            if relative=='states/index.html':legacy.append((name,href))
            if not target.exists(): broken.append((name,href,'Missing destination'))
            elif url.fragment and relative in parsed and unquote(url.fragment) not in parsed[relative].ids:
                broken.append((name,href,'Missing destination anchor'))
    lines=['# Site internal-link audit','',f'- HTML pages scanned: {len(pages)}',f'- Internal links checked: {checked}',f'- Links to obsolete `/states/` index: {len(legacy)}',f'- Missing destinations or anchors: {len(broken)}','', '## Obsolete state-index links','']
    lines += [f'- `{name}`: `{href}`' for name,href in legacy] or ['None.']
    lines += ['','## Missing destinations or anchors','']
    lines += [f'- `{name}`: `{href}` — {reason}' for name,href,reason in broken] or ['None.']
    Path(args.report).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'Pages: {len(pages)}; internal links: {checked}; obsolete /states/ links: {len(legacy)}; broken links/anchors: {len(broken)}')
    print(f'Report: {args.report}')
    if broken: raise SystemExit(1)

if __name__=='__main__': main()
