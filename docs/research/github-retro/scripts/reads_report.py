import json, sys, collections
from datetime import datetime
rows = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])); M = {r['n']: r for r in json.load(open(sys.argv[3]))['issues']}
RAW = {i['number']: i for i in map(json.loads, open(sys.argv[4]))}
def t(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
print('All issue reads:', sum(r['kind']=='issue' for r in rows), 'with comments:', sum(r['kind']=='issue' and r['comments'] for r in rows),
      'by subagents:', sum(r['kind']=='issue' and r['subagent'] for r in rows))
print('All PR reads:', sum(r['kind']=='pr' for r in rows), 'with comments:', sum(r['kind']=='pr' and r['comments'] for r in rows))
print('\n| issue | kind | sessions that read it | reads before first PR | reads during work | reads after close | reads with comments | body edits by command |')
print('|---|---|---|---|---|---|---|---|')
for n in sorted(B, key=int):
    n = int(n); i = RAW[n]; fp = B[str(n)]['first_pr']; fp = t(fp) if fp else None
    cl = t(i['closedAt']) if i['closedAt'] else None
    rs = [r for r in rows if r['kind']=='issue' and r['n']==n and r['ts']]
    def phase(r):
        ts = t(r['ts'])
        if cl and ts > cl: return 'after'
        if fp and ts >= fp: return 'during'
        return 'before'
    c = collections.Counter(phase(r) for r in rs)
    ed = sum(1 for r in rows if r['kind']=='edit-issue' and r['n']==n)
    print(f"| #{n} | {M[n]['kind']} | {len({r['session'] for r in rs})} | {c['before']} | {c['during']} | {c['after']} | {sum(r['comments'] for r in rs)} | {ed} |")
