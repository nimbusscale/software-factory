import json
KEY = {"pr30": "a named hotel loses its Google name (`isAddress()` drops `premise` places)",
       "pr32": "`scheduleOf()` can return entries out of time order",
       "pr33": "`TripRepository.save()` stops checking the started-trip lock",
       "pr35": "the driving warning and the schedule count a day's driving two different ways"}
MATCH = {("stock","pr32"):"S1", ("stock","pr33"):"S1", ("first","pr30"):"F3", ("first","pr32"):"F1", ("current","pr33"):"F3"}
RUNS = [("stock","Stock prompt","runs-v1/{}-stock.json"),("first","Ours, first wording","runs-v1/{}-ours.json"),("current","Ours, current wording","runs/{}-ours.json")]
TAG = {"important":"important","nit":"nit","pre_existing":"pre-existing"}
out=[]
for pr in ["pr30","pr32","pr33","pr35"]:
    out.append(f"## Road-trip-agent PR #{pr[2:]}\n")
    out.append(f"The known bug: {KEY[pr]}.\n")
    for key,label,path in RUNS:
        r=json.load(open(path.format(pr)))
        fs=r["findings"]; m=MATCH.get((key,pr))
        counts={}
        for x in fs: counts[x["severity"]]=counts.get(x["severity"],0)+1
        cs=", ".join(f"{v} {TAG[k]}" for k,v in counts.items())
        out.append(f"### {label}: {len(fs)} findings ({cs}). Known bug: {'found, as ' + m if m else 'missed'}\n")
        for i,x in enumerate(fs,1):
            fid = x.get("id") or f"S{i}"
            mark = " **This is the known bug.**" if fid==m else ""
            out.append(f"- **{fid}, {TAG[x['severity']]},** `{x['file']}:{x['line']}`.{mark} {x['summary']}")
        out.append("")
print("\n".join(out))
