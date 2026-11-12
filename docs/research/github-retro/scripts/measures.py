"""Per-issue and per-PR measures from the raw pull. Usage: python3 -I measures.py RAWDIR OUTDIR"""
import json, re, sys, collections, statistics as st
from datetime import datetime
raw, out = sys.argv[1], sys.argv[2]
iss = {i['number']: i for i in map(json.loads, open(f'{raw}/issues.jsonl'))}
prs = {p['number']: p for p in map(json.loads, open(f'{raw}/prs.jsonl'))}

KIND = {}
def k(kind, nums):
    for n in nums: KIND[n] = kind
k('feature', [47,48,52,54,55,56,57,58,59,60,61,62,63,64,65,66,118,123,125,135,141,142,147,151,152,155,161,166,168,169,170,176,184,197,198,199,204,208,211,221,222,230,236,243,252,117])
k('fix', [145,148,156,160,187,212,218,219,220,231,232,233,253,258,261,262,265,281,296])
k('eval', [53,69,167,177,185,209,223,225,234,235,266,269,282,288,244,245,251])
k('spike', [173,80,87,110,129,132,136,163,182,188,191,193,194])
k('devloop', [50,70,71,72,75,76,77,82,84,85,86,89,92,93,114,115,241])
k('recording', [67,68,259,271,272,273,274,275,276])
missing = [n for n in iss if n not in KIND]
assert not missing, missing

def t(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
WHY = t('2026-10-22T16:15:50Z')   # Why section added to the template
ISSUES = t('2026-10-19T17:57:01Z')  # plan moved into issues
AUTO = t('2026-10-28T16:43:24Z')  # DEVELOPMENT.md section 10, autonomous work
def era(ts):
    ts = t(ts)
    return 'A plan/' if ts < ISSUES else 'B issues' if ts < WHY else 'C why' if ts < AUTO else 'D auto'

def words(s): return len((s or '').split())
def sections(body):
    out, name = collections.OrderedDict(), '(top)'
    for line in (body or '').splitlines():
        m = re.match(r'^#{2,3}\s+(.*)', line)
        if m: name = m.group(1).strip(); out.setdefault(name, 0); continue
        out[name] = out.get(name, 0) + words(line)
    return out

# Link PRs to issues
pr_issues = collections.defaultdict(set)
for p in prs.values():
    s = set(x['number'] for x in p['closingIssuesReferences']['nodes'])
    s |= set(int(m) for m in re.findall(r'\(#(\d+)\)\s*$', p['title']))
    s |= set(int(m) for m in re.findall(r'(?i)(?:closes|fixes|resolves|part of)\s+#(\d+)', p['body'] or ''))
    pr_issues[p['number']] = {n for n in s if n in iss}
issue_prs = collections.defaultdict(list)
for pn, s in pr_issues.items():
    for n in s: issue_prs[n].append(pn)

DEC = re.compile(r'^\s*(## Decisions|\*\*Decisions|Decisions( and things set aside)?:)', re.I)
def decisions_comment(p):
    for c in p['comments']['nodes']:
        if c['author'] and c['author']['login'] == 'nimbusscale' and DEC.match(c['body']):
            return c
def count_items(body):
    return len(re.findall(r'^[-*] |^\d+\. ', body, re.M))

irows = []
for n, i in sorted(iss.items()):
    secs = sections(i['body'])
    oq = next((v for kk, v in secs.items() if kk.lower().startswith('open question')), None)
    oq_text = (i['body'] or '').split('## Open questions', 1)[1].split('\n## ', 1)[0] if '## Open questions' in (i['body'] or '') else ''
    ps = sorted(issue_prs.get(n, []))
    first_pr = min((t(prs[x]['createdAt']) for x in ps), default=None)
    edits = [t(e['createdAt']) for e in i['userContentEdits']['nodes']]
    closed = t(i['closedAt']) if i['closedAt'] else t('2026-11-11T23:59:00Z')
    irows.append(dict(n=n, title=i['title'], kind=KIND[n], era=era(i['createdAt']),
        state=i['state'], reason=i['stateReason'], status=(i['projectItems']['nodes'][0]['fieldValueByName'] or {}).get('name') if i['projectItems']['nodes'] else None,
        words=words(i['body']), sections=secs, edits=len(edits),
        edits_after_pr=sum(1 for e in edits if first_pr and e > first_pr),
        comments=i['comments']['totalCount'], comment_words=sum(words(c['body']) for c in i['comments']['nodes']),
        prs=ps, merged_prs=[x for x in ps if prs[x]['mergedAt']],
        days_open=round((closed - t(i['createdAt'])).total_seconds() / 86400, 1),
        open_q_items=count_items(oq_text), open_q_struck=oq_text.count('~~') // 2,
        labels=[l['name'] for l in i['labels']['nodes']]))

prow = []
for n, p in sorted(prs.items()):
    dc = decisions_comment(p)
    threads = p['reviewThreads']['nodes']
    prow.append(dict(n=n, title=p['title'], era=era(p['createdAt']), state=p['state'],
        words=words(p['body']), closes=bool(re.search(r'(?i)closes #\d+', p['body'] or '')),
        issues=sorted(pr_issues[n]), kinds=sorted({KIND[x] for x in pr_issues[n]}),
        has_done_when=bool(re.search(r'(?i)done when', p['body'] or '')),
        has_why=bool(re.search(r'(?im)^#+\s*why', p['body'] or '')),
        decisions=bool(dc), decision_items=count_items(dc['body']) if dc else 0, decision_words=words(dc['body']) if dc else 0,
        comments=p['comments']['totalCount'],
        joe_comments=sum(1 for c in p['comments']['nodes'] if c['author'] and c['author']['login']=='nimbusscale'),
        threads=len(threads), review_comments=sum(th['comments']['totalCount'] for th in threads),
        reviews=p['reviews']['totalCount'], commits=p['commits']['totalCount'], edits=p['userContentEdits']['totalCount'],
        files=p['changedFiles'], lines=p['additions'] + p['deletions'],
        hours_to_merge=round((t(p['mergedAt']) - t(p['createdAt'])).total_seconds() / 3600, 1) if p['mergedAt'] else None))

json.dump(dict(issues=irows, prs=prow), open(f'{out}/measures.json', 'w'), indent=1, default=list)
print('issues', len(irows), 'prs', len(prow))
