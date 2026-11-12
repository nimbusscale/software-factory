import json, sys, collections, statistics as st
d = json.load(open(sys.argv[1]))
I, P = d['issues'], d['prs']
def med(xs): xs=[x for x in xs if x is not None]; return round(st.median(xs),1) if xs else '-'
def tot(xs): return sum(xs)
def table(rows, keyf, title):
    g = collections.defaultdict(list)
    for r in rows: g[keyf(r)].append(r)
    print(f'\n### {title}\n')
    print('| group | n | median words | max words | median edits | edits total | median PRs | median days open | closed done | closed not planned | open |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for kk in sorted(g):
        rs = g[kk]
        print(f"| {kk} | {len(rs)} | {med([r['words'] for r in rs])} | {max(r['words'] for r in rs)} | {med([r['edits'] for r in rs])} | {tot([r['edits'] for r in rs])} | {med([len(r['prs']) for r in rs])} | {med([r['days_open'] for r in rs if r['state']=='CLOSED'])} | {sum(r['reason']=='COMPLETED' for r in rs)} | {sum(r['reason']=='NOT_PLANNED' for r in rs)} | {sum(r['state']=='OPEN' for r in rs)} |")
table(I, lambda r: r['kind'], 'Issues by kind of work')
table(I, lambda r: r['era'], 'Issues by era created')
print('\n### Top issues by words\n')
for r in sorted(I, key=lambda r: -r['words'])[:12]:
    print(f"- #{r['n']} {r['kind']}, {r['words']} words, {r['edits']} edits ({r['edits_after_pr']} after its first PR), {len(r['prs'])} PRs, {r['comments']} comments, {r['status']}: {r['title'][:70]}")
print('\n### PRs per issue\n')
c = collections.Counter(min(len(r['prs']),5) for r in I)
print(dict(sorted(c.items())))
print('issues with 3+ PRs:', [(r['n'], len(r['prs'])) for r in I if len(r['prs'])>=3])
print('\n### Edits after the first PR opened\n')
print('issues with any:', sum(1 for r in I if r['edits_after_pr']), 'total such edits:', sum(r['edits_after_pr'] for r in I))
print('\n### Section words, issues created after the Why section (era C and D)\n')
secs = collections.defaultdict(list); have = collections.Counter()
later = [r for r in I if r['era'] >= 'C']
for r in later:
    for s, w in r['sections'].items():
        key = s.split('(')[0].strip()[:30]; secs[key].append(w); have[key]+=1
for s, ws in sorted(secs.items(), key=lambda x: -len(x[1]))[:14]:
    print(f"- {s}: in {have[s]} of {len(later)}, median {med(ws)}, max {max(ws)}, total {sum(ws)}")
print('\n### Open questions\n')
print('issues with open-question items:', sum(1 for r in I if r['open_q_items']), 'items:', sum(r['open_q_items'] for r in I), 'struck:', sum(r['open_q_struck'] for r in I))
print('\n### Comments on issues\n')
print('issues with comments:', sum(1 for r in I if r['comments']), 'comments total:', sum(r['comments'] for r in I), 'comment words:', sum(r['comment_words'] for r in I))
print('not planned closures with a comment:', sum(1 for r in I if r['reason']=='NOT_PLANNED' and r['comments']))
print('\n### Open issues by status\n')
print(collections.Counter((r['status'], r['kind']) for r in I if r['state']=='OPEN'))

def ptable(rows, keyf, title):
    g = collections.defaultdict(list)
    for r in rows: g[keyf(r)].append(r)
    print(f'\n### {title}\n')
    print('| group | n | merged | median desc words | max | no issue | closes # | decisions comment | median decision items | median review threads | median commits | median hours to merge |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for kk in sorted(g):
        rs = g[kk]; m=[r for r in rs if r['state']=='MERGED']
        print(f"| {kk} | {len(rs)} | {len(m)} | {med([r['words'] for r in rs])} | {max(r['words'] for r in rs)} | {sum(not r['issues'] for r in rs)} | {sum(r['closes'] for r in rs)} | {sum(r['decisions'] for r in rs)} | {med([r['decision_items'] for r in rs if r['decisions']])} | {med([r['threads'] for r in rs])} | {med([r['commits'] for r in rs])} | {med([r['hours_to_merge'] for r in m])} |")
ptable(P, lambda r: r['era'], 'PRs by era opened')
ptable([r for r in P if r['issues']], lambda r: '+'.join(r['kinds']), 'PRs with an issue, by kind of work')
print('\n### Top PRs by description words\n')
for r in sorted(P, key=lambda r: -r['words'])[:8]:
    print(f"- PR #{r['n']} {r['era']}, {r['words']} words, issues {r['issues']}: {r['title'][:70]}")
print('\n### Top PRs by decision items\n')
for r in sorted(P, key=lambda r: -r['decision_items'])[:8]:
    print(f"- PR #{r['n']} {r['era']}, {r['decision_items']} items, {r['decision_words']} words, issues {r['issues']}: {r['title'][:60]}")
print('\ndecision comment words total:', sum(r['decision_words'] for r in P), 'desc words total:', sum(r['words'] for r in P))
print('PR desc edits: PRs with edits', sum(1 for r in P if r['edits']), 'total', sum(r['edits'] for r in P))
