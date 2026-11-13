"""Body growth of every issue: first version, at its first PR, and final. Usage: python3 -I growth.py VERSIONS_DIR MEASURES RAW_PRS"""
import json, sys, glob, statistics as st, collections
from datetime import datetime
def t(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
M = {r['n']: r for r in json.load(open(sys.argv[2]))['issues']}; P = {p['number']: p for p in map(json.loads, open(sys.argv[3]))}
rows = []
for f in glob.glob(f'{sys.argv[1]}/*.json'):
    d = json.load(open(f)); n = d['number']
    v = sorted((t(e['editedAt']), len((e['diff'] or '').split())) for e in d['userContentEdits']['nodes'] if len((e['diff'] or '').split()) > 10) or [(t(d['createdAt']), len(d['body'].split()))]
    fp = min((t(P[p]['createdAt']) for p in M[n]['prs']), default=None)
    before = [x for x in v if not fp or x[0] <= fp]
    at = (before[-1] if before else v[0])[1]
    rows.append(dict(n=n, kind=M[n]['kind'], first=v[0][1], at_pr=at, final=len(d['body'].split()), has_pr=bool(fp)))
by = collections.defaultdict(list)
for r in rows: by[r['kind']].append(r)
print('| kind | n | median first version | median at first PR | median final | median growth before work (x) |')
print('|---|---|---|---|---|---|')
for k, rs in sorted(by.items()) + [('all', rows)]:
    print(f"| {k} | {len(rs)} | {st.median(r['first'] for r in rs)} | {st.median(r['at_pr'] for r in rs)} | {st.median(r['final'] for r in rs)} | {round(st.median(r['at_pr']/max(r['first'],1) for r in rs),1)} |")
big = sorted(rows, key=lambda r: -(r['at_pr'] - r['first']))[:8]
print('\nLargest growth before work:', [(r['n'], r['first'], r['at_pr']) for r in big])
print('Issues that at least doubled before work:', sum(1 for r in rows if r['at_pr'] >= 2*r['first']), 'of', len(rows))
print('Issues that grew after their first PR:', [(r['n'], r['at_pr'], r['final']) for r in rows if r['has_pr'] and r['final'] > r['at_pr'] * 1.1])
