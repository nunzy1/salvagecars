#!/usr/bin/env python3
"""Read-only check of question-page state dropdown destinations and HTML anchors.
Run from the repository root: python3 check-question-navigation.py
Requires Python 3 and Node.js.
"""
from pathlib import Path
from html.parser import HTMLParser
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent / 'public'
QUESTIONS = sorted((ROOT / 'questions').glob('*/index.html'))

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.options = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'option' and attributes.get('value'):
            self.options.append(attributes['value'])
        if attributes.get('id'):
            self.ids.add(attributes['id'])

NODE_CHECKER = r'''
const fs = require('fs');
const vm = require('vm');
const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const results = {};
let selected = '';
let handler = null;
const select = {
  get value() { return selected; },
  options: data.states.map(value => ({value})),
  reportValidity: () => true
};
const form = {
  addEventListener: (type, callback) => {
    if (type === 'submit') handler = callback;
  }
};
const sandbox = {
  document: { getElementById: id => id === 'state-form' ? form : select },
  window: { location: { assign: url => { results[selected] = url; } } },
  console
};
for (const script of data.scripts) {
  vm.runInNewContext(script, sandbox, { timeout: 1000 });
}
if (typeof handler !== 'function') {
  throw new Error('No submit handler was registered by the page scripts');
}
for (const state of data.states) {
  selected = state;
  handler({ preventDefault() {} });
}
process.stdout.write(JSON.stringify(results));
'''

problems = []
checked = 0
if not QUESTIONS:
    problems.append('No question pages found under public/questions/')

for question in QUESTIONS:
    name = question.parent.name
    html = question.read_text(encoding='utf-8')
    parser = PageParser()
    parser.feed(html)
    states = parser.options
    # Skip external scripts (such as Tailwind CDN); execute all inline scripts.
    scripts = re.findall(r'<script\b([^>]*)>(.*?)</script\s*>', html, re.I | re.S)
    inline = [body for attrs, body in scripts if not re.search(r'\bsrc\s*=', attrs, re.I) and body.strip()]
    if not inline:
        problems.append(f'{name}: no inline JavaScript found')
        continue
    if not states:
        problems.append(f'{name}: no state options found')
        continue
    try:
        result = subprocess.run(
            ['node', '-e', NODE_CHECKER],
            input=json.dumps({'states': states, 'scripts': inline}),
            text=True, capture_output=True, timeout=15
        )
    except FileNotFoundError:
        print('ERROR: Node.js is not installed or not on PATH.', file=sys.stderr)
        sys.exit(2)
    except subprocess.TimeoutExpired:
        problems.append(f'{name}: JavaScript validation timed out')
        continue
    if result.returncode != 0:
        problems.append(f'{name}: JavaScript error: {result.stderr.strip()}')
        continue
    try:
        destinations = json.loads(result.stdout)
    except json.JSONDecodeError:
        problems.append(f'{name}: JavaScript did not return valid navigation results')
        continue
    for state in states:
        checked += 1
        url = destinations.get(state, '')
        prefix = f'/states/{state}/#'
        if not url.startswith(prefix):
            problems.append(f'{name} / {state}: invalid URL {url!r}')
            continue
        anchor = url.split('#', 1)[1]
        state_file = ROOT / 'states' / state / 'index.html'
        if not state_file.is_file():
            problems.append(f'{name} / {state}: state page missing')
            continue
        state_parser = PageParser()
        state_parser.feed(state_file.read_text(encoding='utf-8'))
        if anchor not in state_parser.ids:
            problems.append(f'{name} / {state}: missing anchor #{anchor}')
    print(f'Checked {name}: {len(states)} jurisdictions')

print(f'\nQuestion pages found: {len(QUESTIONS)}')
print(f'Destinations checked: {checked}')
print(f'Problems found: {len(problems)}')
for problem in problems:
    print('PROBLEM:', problem)
sys.exit(1 if problems else 0)
