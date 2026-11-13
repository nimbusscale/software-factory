"""Total the step 2 labels. Usage: python3 -I labels_report.py STEP2_DIR"""
import json, sys, glob, collections
d = sys.argv[1]
IB = json.load(open(f'{d}/issue-blocks.json')); PB = json.load(open(f'{d}/pr-blocks.json'))
KINDS = ['task','reason','open-question','settled-question','decision','status','result','log','history','copy','set-aside','boilerplate','other']
def row(c, total): return ' | '.join(f"{round(100*c.get(k,0)/total) if total else 0}" for k in KINDS)
issue_tot = collections.Counter(); pr_tot = collections.Counter(); dec_tot = collections.Counter(); com_tot = collections.Counter()
need = collections.Counter(); need_after = collections.Counter(); missing = []
lines = []
for f in sorted(glob.glob(f'{d}/labels/*.json'), key=lambda f: int(f.split('/')[-1][:-5])):
    L = json.load(open(f)); n = str(L['issue']); lab = L['labels']; ib = IB[n]; pb = PB[n]
    c = collections.Counter(); nd = collections.Counter()
    for b in ib['blocks']:
        l = lab.get(b['id']); 
        if not l: missing.append(b['id']); continue
        c[l['kind']] += b['words']; nd[l.get('needed','?')] += b['words']
        need[l.get('needed','?')] += b['words']
        if b['after_first_pr']: need_after[(l['kind'])] += b['words']
    issue_tot.update(c)
    pc = collections.Counter(); dc = collections.Counter(); docs = collections.Counter()
    for p in pb['prs']:
        for b in p['description']:
            l = lab.get(b['id']); 
            if not l: missing.append(b['id']); continue
            pc[l['kind']] += b['words']
        for b in p['decisions']:
            l = lab.get(b['id'])
            if not l: missing.append(b['id']); continue
            dc[l['kind']] += b['words']
            if l['kind'] == 'decision': docs[l.get('doc','?')] += 1
    pr_tot.update(pc); dec_tot.update(dc)
    cc = collections.Counter()
    for b in pb['issue_comments']:
        l = lab.get(b['id'])
        if not l: missing.append(b['id']); continue
        cc[l['kind']] += b['words']
    com_tot.update(cc)
    tw = sum(c.values())
    lines.append((n, ib['kind'], tw, c, nd, sum(pc.values()), pc, sum(dc.values()), docs, sum(cc.values()), cc, dc))
print('Missing labels:', missing or 'none')
print('\n### Issue body: share of words by kind (%)\n')
print('| issue | kind | words | needed yes % | ' + ' | '.join(KINDS) + ' |'); print('|' + '---|' * (len(KINDS) + 4))
for n, k, tw, c, nd, *_ in lines: print(f"| #{n} | {k} | {tw} | {round(100*nd['yes']/tw) if tw else 0} | {row(c, tw)} |")
T = sum(issue_tot.values()); print(f"| all | | {T} | {round(100*need['yes']/T)} | {row(issue_tot, T)} |")
print('\nWords added after the first PR, by kind:', dict(need_after.most_common()))
print('\n### PR descriptions: share of words by kind (%)\n')
print('| issue | words | ' + ' | '.join(KINDS) + ' |'); print('|' + '---|' * (len(KINDS) + 2))
for n, k, tw, c, nd, pw, pc, *_ in lines:
    if pw: print(f"| #{n} | {pw} | {row(pc, pw)} |")
T = sum(pr_tot.values()); print(f"| all | {T} | {row(pr_tot, T)} |")
print('\n### Decisions comments\n')
print('| issue | words | decision items | named a doc | ' + ' | '.join(KINDS) + ' |'); print('|' + '---|' * (len(KINDS) + 4))
alld = collections.Counter()
for n, k, tw, c, nd, pw, pc, dw, docs, cw, cc, dc in lines:
    alld.update(docs)
    if dw: print(f"| #{n} | {dw} | {sum(docs.values())} | {docs['yes']} | {row(dc, dw)} |")
T = sum(dec_tot.values()); print(f"| all | {T} | {sum(alld.values())} | {alld['yes']} | {row(dec_tot, T)} |")
print('\n### Issue comments\n')
print('| issue | words | ' + ' | '.join(KINDS) + ' |'); print('|' + '---|' * (len(KINDS) + 2))
for n, k, tw, c, nd, pw, pc, dw, docs, cw, cc, dc in lines:
    if cw: print(f"| #{n} | {cw} | {row(cc, cw)} |")
T = sum(com_tot.values()); print(f"| all | {T} | {row(com_tot, T)} |")
