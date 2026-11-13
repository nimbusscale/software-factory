"""Split each sampled issue's final body into blocks, and find when each block first appeared.
Usage: python3 -I blocks.py MEASURES_JSON VERSIONS_DIR RAW_PRS OUT_JSON"""
import json, re, sys, glob, difflib
from datetime import datetime
measures, vdir, rawprs, out = sys.argv[1:5]
M = {r['n']: r for r in json.load(open(measures))['issues']}
PRS = {p['number']: p for p in map(json.loads, open(rawprs))}
def t(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
def norm(s): return re.sub(r'\s+', ' ', re.sub(r'~~', '', s)).strip().lower()

def split_blocks(body):
    """Paragraphs and top-level list items, each with its section heading."""
    blocks, sec, cur = [], '(top)', []
    def flush():
        if cur and ''.join(cur).strip(): blocks.append((sec, '\n'.join(cur).strip()))
        cur.clear()
    for line in (body or '').splitlines():
        h = re.match(r'^#{2,4}\s+(.*)', line)
        if h: flush(); sec = h.group(1).strip(); continue
        if not line.strip(): flush(); continue
        if re.match(r'^(- |\* |\d+\. )', line): flush()
        cur.append(line)
    flush()
    return blocks

res = {}
for f in glob.glob(f'{vdir}/*.json'):
    d = json.load(open(f))
    if d['__typename'] != 'Issue': continue
    n = d['number']
    versions = [(t(e['editedAt']), e['diff'] or '') for e in d['userContentEdits']['nodes'] if len((e['diff'] or '').split()) > 10]
    versions.sort()
    if not versions: versions = [(t(d['createdAt']), d['body'])]
    vblocks = [(ts, [norm(b) for _, b in split_blocks(body)]) for ts, body in versions]
    first_pr = min((t(PRS[p]['createdAt']) for p in M[n]['prs']), default=None)
    out_blocks = []
    for i, (sec, text) in enumerate(split_blocks(d['body'])):
        nt = norm(text); seen = None
        for ts, bl in vblocks:
            if any(b == nt or (len(nt) > 40 and difflib.SequenceMatcher(None, b, nt).quick_ratio() > 0.85 and difflib.SequenceMatcher(None, b, nt).ratio() > 0.8) for b in bl):
                seen = ts; break
        seen = seen or versions[-1][0]
        out_blocks.append(dict(id=f'I{n}-{i}', section=sec, words=len(text.split()), text=text,
            first_seen=seen.isoformat(), days_after_open=round((seen - versions[0][0]).total_seconds()/86400, 2),
            after_first_pr=bool(first_pr and seen > first_pr), struck='~~' in text))
    res[n] = dict(number=n, title=M[n]['title'], kind=M[n]['kind'], era=M[n]['era'], created=d['createdAt'],
        first_pr=first_pr.isoformat() if first_pr else None, prs=M[n]['prs'],
        words_first_version=len(versions[0][1].split()),
        words_at_first_pr=len(max((v for v in versions if not first_pr or v[0] <= first_pr), key=lambda v: v[0])[1].split()),
        words_final=len(d['body'].split()), versions=len(versions), blocks=out_blocks)
json.dump(res, open(out, 'w'), indent=1)
for n, r in sorted(res.items()):
    print(n, r['kind'], 'first', r['words_first_version'], 'at PR', r['words_at_first_pr'], 'final', r['words_final'], 'blocks', len(r['blocks']), 'words after PR', sum(b['words'] for b in r['blocks'] if b['after_first_pr']))
