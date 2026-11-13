"""Blocks for the sampled issues' PRs (description and decisions comment) and the issues' comments.
Usage: python3 -I pr_blocks.py ISSUE_BLOCKS RAW_ISSUES RAW_PRS OUT_JSON"""
import json, re, sys
B = json.load(open(sys.argv[1])); RI = {i['number']: i for i in map(json.loads, open(sys.argv[2]))}; RP = {p['number']: p for p in map(json.loads, open(sys.argv[3]))}
def split_blocks(body):
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
    flush(); return blocks
DEC = re.compile(r'^\s*(## Decisions|\*\*Decisions|Decisions( and things set aside)?:)', re.I)
out = {}
for n, r in B.items():
    n = int(n); item = dict(issue_comments=[], prs=[])
    for k, c in enumerate(RI[n]['comments']['nodes']):
        item['issue_comments'].append(dict(id=f'IC{n}-{k}', created=c['createdAt'], words=len(c['body'].split()), text=c['body']))
    for p in r['prs']:
        pr = RP[p]
        dc = next((c for c in pr['comments']['nodes'] if c['author'] and c['author']['login']=='nimbusscale' and DEC.match(c['body'])), None)
        other = [c for c in pr['comments']['nodes'] if c is not dc]
        item['prs'].append(dict(number=p, title=pr['title'], created=pr['createdAt'], merged=pr['mergedAt'],
            description=[dict(id=f'P{p}-d{i}', section=s, words=len(x.split()), text=x) for i, (s, x) in enumerate(split_blocks(pr['body']))],
            decisions=[dict(id=f'P{p}-c{i}', section=s, words=len(x.split()), text=x) for i, (s, x) in enumerate(split_blocks(dc['body']))] if dc else [],
            other_comments=[dict(author=c['author']['login'] if c['author'] else None, words=len(c['body'].split()), first_line=c['body'].strip().split('\n')[0][:150]) for c in other],
            review_threads=pr['reviewThreads']['totalCount']))
    out[n] = item
json.dump(out, open(sys.argv[4], 'w'), indent=1)
for n, it in sorted(out.items()):
    print(n, 'issue words', B[str(n)]['words_final'], 'comment words', sum(c['words'] for c in it['issue_comments']),
          'PR desc words', sum(b['words'] for p in it['prs'] for b in p['description']), 'decision words', sum(b['words'] for p in it['prs'] for b in p['decisions']))
