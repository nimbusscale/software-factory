"""Find every time an agent read a road-trip-agent issue or PR, from the local Claude Code transcripts.
Usage: python3 -I reads.py OUT_JSON PROJECT_DIR..."""
import json, re, sys, os, glob
out, dirs = sys.argv[1], sys.argv[2:]
PAT = [
    ('issue', re.compile(r'gh issue view\s+#?(\d+)([^\n;&|]*)')),
    ('pr', re.compile(r'gh pr view\s+#?(\d+)([^\n;&|]*)')),
    ('issue', re.compile(r'gh api\s+[^\n]*?repos/[^/\s]+/[^/\s]+/issues/(\d+)(/comments)?')),
    ('pr', re.compile(r'gh api\s+[^\n]*?repos/[^/\s]+/[^/\s]+/pulls/(\d+)(/comments|/reviews)?')),
    ('edit-issue', re.compile(r'gh issue edit\s+#?(\d+)([^\n;&|]*)')),
    ('comment-issue', re.compile(r'gh issue comment\s+#?(\d+)()')),
    ('create-issue', re.compile(r'gh issue create()()')),
    ('edit-pr', re.compile(r'gh pr edit\s+#?(\d+)([^\n;&|]*)')),
    ('comment-pr', re.compile(r'gh pr comment\s+#?(\d+)()')),
]
rows = []
for d in dirs:
    for f in glob.glob(f'{d}/**/*.jsonl', recursive=True):
        sub = '/subagents/' in f
        for line in open(f, errors='replace'):
            if '"tool_use"' not in line or 'gh ' not in line: continue
            try: e = json.loads(line)
            except Exception: continue
            msg = e.get('message') or {}
            for c in msg.get('content') or []:
                if not isinstance(c, dict) or c.get('type') != 'tool_use' or c.get('name') != 'Bash': continue
                cmd = (c.get('input') or {}).get('command', '')
                for kind, p in PAT:
                    for m in p.finditer(cmd):
                        rest = m.group(2) or ''
                        rows.append(dict(kind=kind, n=int(m.group(1)) if m.group(1) else None, ts=e.get('timestamp'),
                            session=os.path.basename(f), subagent=sub, dir=os.path.basename(d),
                            comments=('comments' in rest) or ('--comments' in cmd and kind in ('issue','pr')),
                            fields=re.findall(r'--json\s+([\w,]+)', rest)))
json.dump(rows, open(out, 'w'))
from collections import Counter
print(len(rows), Counter(r['kind'] for r in rows))
