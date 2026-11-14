#!/usr/bin/env bash
# Checks a project's docs against the writing-project-docs skill's rules.
#
# Usage, from the repo root:  check-docs.sh <docs folder> <base branch>
#
# Docs are every .md file in the docs folder, plus CLAUDE.md and the skills in .claude/skills,
# except this skill. Source files are the other text files in the repo that git doesn't ignore.
# The specs are found by their F-SEC and T-SEC headings. Research docs and blueprints are the ones
# in <docs folder>/research and <docs folder>/blueprints.
#
# The history checks look only at lines added since the base branch, uncommitted ones included.
# A line someone kept on purpose is then never flagged again. The other checks look at every doc.
#
# Prints one line per thing it flags:  RULE|SIGNAL <file>:<line> <what>
# RULE means a rule was broken. SIGNAL means only that something is worth a look.
# It exits 0 whenever it ran. What happens to the findings is up to the project's workflow.

set -u

usage() { echo "usage: check-docs.sh <docs folder> <base branch>, run from the repo root" >&2; exit 2; }
[[ $# -eq 2 && -d $1 ]] || usage
[[ $(git rev-parse --show-toplevel 2>/dev/null) == "$PWD" ]] || usage
base=$(git merge-base "$2" HEAD 2>/dev/null) || usage
docs_dir=${1%/}
research_dir=$(realpath -m "$docs_dir/research")
blueprints_dir=$(realpath -m "$docs_dir/blueprints")
self_dir=$(realpath "$(dirname "$0")/..")
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

ids='(FR|TR|AD|TD)-[0-9]+'
sec_ids='[FT]-SEC-[0-9]+'

# --- Which files are which ---------------------------------------------------------------------

{
  find "$docs_dir" -name '*.md' -type f
  [[ -f CLAUDE.md ]] && echo CLAUDE.md
  [[ -d .claude/skills ]] && find .claude/skills -name '*.md' -type f
} | while read -r f; do
  [[ $(realpath "$f") == "$self_dir"/* ]] || echo "${f#./}"
done | sort -u >"$tmp/docs"

git ls-files --cached --others --exclude-standard | grep -E '\.(ts|tsx|js|mjs|cjs|py|sh|md|txt)$' | grep -vxFf "$tmp/docs" |
  grep -v '^\.claude/' | while read -r f; do [[ -f $f ]] && echo "$f"; done | sort >"$tmp/src"

is_research() { [[ $(realpath -m "$1") == "$research_dir"/* ]]; }
is_blueprint() { [[ $(realpath -m "$1") == "$blueprints_dir"/* ]]; }

# The line numbers in a file that were added since the base. Every line, for a new file.
added_lines() {
  if git cat-file -e "$base:$1" 2>/dev/null; then
    git diff -U0 "$base" -- "$1" | awk '/^@@/ {
      split(substr($3, 2), a, ","); n = (a[2] == "" ? 1 : a[2])
      for (i = 0; i < n; i++) print a[1] + i }'
  else
    awk 'END { for (i = 1; i <= NR; i++) print i }' "$1"
  fi
}

xargs -d '\n' -r grep -lE '^#+ F-SEC-[0-9]+' <"$tmp/docs" >"$tmp/fspec" || true
xargs -d '\n' -r grep -lE '^#+ T-SEC-[0-9]+' <"$tmp/docs" >"$tmp/tspec" || true
cat "$tmp/fspec" "$tmp/tspec" >"$tmp/specs"

# Prints a file with its fenced code blocks and inline code blanked out, keeping line numbers.
# With "scenarios" as the second argument, it blanks Scenario paragraphs too.
prose() {
  awk -v skip_scen="${2:-}" '
    /^[ \t>]*(```|~~~)/ { fence = !fence; print ""; next }
    fence { print ""; next }
    /^[ \t>]*$/ { scen = 0 }
    skip_scen && /^[ \t>]*\*Scenario:\*/ { scen = 1 }
    scen { print ""; next }
    { gsub(/`[^`]*`/, ""); print }
  ' "$1"
}

# --- History -----------------------------------------------------------------------------------

# Each match prints as "<line> <what>", and only matches on added lines are kept.
months='(January|February|March|April|May|June|July|August|September|October|November|December)'
while read -r f; do
  is_research "$f" || is_blueprint "$f" && continue
  prose "$f" scenarios | sed -E 's/\]\([^)]*\)/]/g' >"$tmp/prose"
  {
    grep -noE "\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b|\b$months [0-9]{1,2}\b" "$tmp/prose" |
      while IFS=: read -r n m; do echo "$n date: $m"; done
    grep -noE '(^|[^A-Za-z0-9&/])#[0-9]+\b' "$tmp/prose" |
      while IFS=: read -r n m; do echo "$n issue or PR number: ${m#"${m%%#*}"}"; done
    grep -noiwE 'settled|decided|drafted|assumption|for now|to come|in progress|no longer|used to|the new' \
      "$tmp/prose" | while IFS=: read -r n m; do echo "$n marker word: $m"; done
    grep -niwE 'was\b.*\bnow' "$tmp/prose" | cut -d: -f1 | while read -r n; do echo "$n \"was ... now\""; done
  } >"$tmp/hist"
  added_lines "$f" | awk -v f="$f" 'NR == FNR { added[$1]; next }
    ($1 in added) { n = $1; $1 = ""; print "SIGNAL " f ":" n " may be history:" $0 }' - "$tmp/hist"
done <"$tmp/docs"

# --- References --------------------------------------------------------------------------------

# Definitions: file, line, ID.
while read -r f; do
  grep -noE "^\*\*$ids\.\*\*" "$f" | sed -E 's/\*//g; s/\.$//' | sed "s|^|$f:|"
  grep -noE "^#+ $sec_ids" "$f" | sed -E 's/#+ //' | sed "s|^|$f:|"
done <"$tmp/specs" >"$tmp/defs"
cut -d: -f3 "$tmp/defs" | sort -u >"$tmp/defined"

# Each ID defined twice in one doc, and each item in the wrong spec.
awk -F: '{ k = $1 FS $3 } seen[k]++ { print "RULE " $1 ":" $2 " " $3 " is defined twice in this doc" }' \
  "$tmp/defs"
while IFS=: read -r f n id; do
  if grep -qxF "$f" "$tmp/fspec" && [[ $id =~ ^(TR|AD|TD|T-SEC) ]]; then
    echo "RULE $f:$n $id belongs in the technical spec"
  elif grep -qxF "$f" "$tmp/tspec" && [[ $id =~ ^(FR|F-SEC) ]]; then
    echo "RULE $f:$n $id belongs in the functional spec"
  fi
done <"$tmp/defs"

# Citations in docs and source files: file, line, ID. Definitions count too.
cat "$tmp/docs" "$tmp/src" >"$tmp/all"
xargs -d '\n' -r grep -HnoE "\b($ids|$sec_ids)\b" <"$tmp/all" >"$tmp/cites" || true
awk -F: 'NR == FNR { d[$1]; next } !($3 in d) { print "RULE " $1 ":" $2 " cites " $3 ", which isn'\''t defined" }' \
  "$tmp/defined" "$tmp/cites"

# Requirements that nothing cites: their only appearance is the definition.
cut -d: -f3 "$tmp/cites" | sort | uniq -c | awk '$1 == 1 { print $2 }' >"$tmp/once"
grep -E ":(FR|TR)-" "$tmp/defs" | while IFS=: read -r f n id; do
  grep -qxF "$id" "$tmp/once" && echo "SIGNAL $f:$n $id isn't cited anywhere, so it may be unbuilt or untested"
done

# ID ranges.
xargs -d '\n' -r grep -HnoE "\b$ids( (to|through) | ?[-–—] ?)(($ids)|[0-9]+)\b" <"$tmp/all" |
  while IFS=: read -r f n m; do echo "RULE $f:$n cites a range: $m"; done || true

# Links in docs.
while read -r f; do
  prose "$f" | grep -noE '\]\([^)]+\)' | while IFS=: read -r n m; do
    target=${m#](}; target=${target%)}; target=${target%%#*}; target=${target%% *}
    [[ -z $target || $target =~ ^[a-z]+: ]] && continue
    path=$(realpath -m "$(dirname "$f")/$target")
    [[ -e $path ]] || echo "RULE $f:$n links to $target, which doesn't exist"
    if grep -qxF "$f" "$tmp/fspec"; then
      echo "RULE $f:$n the functional spec links out, to $target"
    elif is_research "$f"; then
      echo "RULE $f:$n a research doc links to another doc, $target"
    elif [[ $path == "$research_dir"/* ]]; then
      echo "RULE $f:$n links to a research doc, $target"
    elif [[ $path == "$blueprints_dir"/* ]] && ! is_blueprint "$f"; then
      echo "RULE $f:$n links to a blueprint, $target"
    fi
  done
done <"$tmp/docs"

# --- Item shape --------------------------------------------------------------------------------

while read -r f; do
  awk -v f="$f" '
    function flush() { if (para != "") check(para, start); para = "" }
    function check(p, n,   id, body, pre, w, i, k, last, order) {
      if (match(p, /^\*\*(FR|TR|AD|TD)-[0-9]+\.\*\*/)) {
        if (why_id != "") print "RULE " f ":" why_line " " why_id " has no Why line right after it"
        why_id = ""
        id = substr(p, 3, RLENGTH - 5); body = substr(p, RLENGTH + 2)
        if (id ~ /^(AD|TD)/) { why_id = id; why_line = n; return }
        if (body !~ /^(Where|While|When|The)[ ,]/)
          print "RULE " f ":" n " " id " doesn'\''t start with Where, While, When or The"
        k = gsub(/(^|[^A-Za-z])shall([^A-Za-z]|$)/, "&", body)
        if (k != 1) print "RULE " f ":" n " " id " has " k " \"shall\"s, not one"
        pre = tolower(body); sub(/[^a-z]shall[^a-z].*/, "", pre)
        k = split(pre, w, /[^a-z]+/); last = 0; order = "where while when"
        for (i = 1; i <= k; i++) if (w[i] ~ /^(where|while|when)$/) {
          if (index(order, w[i]) <= last) {
            print "RULE " f ":" n " " id " has Where, While and When out of order, or one twice"; break
          }
          last = index(order, w[i])
        }
        return
      }
      if (p ~ /^\*Why:\*/) { why_id = ""; return }
      if (why_id != "") print "RULE " f ":" why_line " " why_id " has no Why line right after it"
      why_id = ""
      if (p !~ /^(#|\*[A-Z][a-z ]+:\*)/ && p ~ /(^|[^A-Za-z])shall([^A-Za-z]|$)/)
        print "RULE " f ":" n " a \"shall\" sentence with no ID"
    }
    /^[ \t]*(```|~~~)/ { fence = !fence; flush(); next }
    fence { next }
    /^[ \t>]*$/ { flush(); next }
    { line = $0; sub(/^[ \t>]+/, "", line)
      if (para == "") { start = NR; para = line } else para = para " " line }
    END { flush(); if (why_id != "") print "RULE " f ":" why_line " " why_id " has no Why line right after it" }
  ' "$f"
done <"$tmp/specs"

# --- Copies ------------------------------------------------------------------------------------

# Every run of eight words, with the file and line it starts on. Research docs are left out.
while read -r f; do
  is_research "$f" || echo "$f"
done <"$tmp/docs" >"$tmp/copy-docs"
cat "$tmp/copy-docs" "$tmp/src" | while read -r f; do
  awk -v f="$f" '{
    s = tolower($0); gsub(/[^a-z0-9'\'']+/, " ", s); k = split(s, w, " ")
    for (i = 1; i <= k; i++) { buf[++nw] = w[i]; at[nw] = FNR
      if (nw >= 8) { r = buf[nw-7]; for (j = nw-6; j <= nw; j++) r = r " " buf[j]; print r "\t" f "\t" at[nw-7] } }
  }' "$f"
done | sort -t$'\t' -k1,1 >"$tmp/runs"

# For each pair of files sharing runs, where at least one is a doc: how many, and the first.
awk -F'\t' '
  NR == FNR { doc[$0]; next }
  $1 != run { flush(); run = $1; n = 0 }
  { file[++n] = $2; line[n] = $3 }
  function flush(   i, j, a, b, k) {
    for (i = 1; i <= n; i++) for (j = 1; j <= n; j++) {
      a = file[i]; b = file[j]
      if (a >= b || !((a in doc) || (b in doc))) continue
      k = a SUBSEP b
      if (!(k in count)) first[k] = a ":" line[i] " and " b ":" line[j] ": \"" run "\""
      count[k]++
    }
  }
  END { flush(); for (k in count) print "SIGNAL " first[k] " (" count[k] " shared 8-word runs)" }
' "$tmp/copy-docs" "$tmp/runs" | sort

# --- Size --------------------------------------------------------------------------------------

while read -r f; do
  tokens=$(($(wc -c <"$f") / 4))
  ((tokens > 20000)) && echo "SIGNAL $f:1 about $tokens tokens, and the Read tool reads at most 25,000 in one call"
done <"$tmp/docs"

exit 0
