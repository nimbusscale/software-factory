#!/usr/bin/env bash
# Checks a project's specs and blueprints against the writing-project-docs skill's rules.
#
# Usage, from the repo root:  check-docs.sh [--uncited] <docs folder> <base branch>
#
# Docs are the specs and the blueprints. The specs are the .md files in the docs folder with F-SEC
# or T-SEC headings. Blueprints are the .md files in <docs folder>/blueprints. Source files are the
# other text files in the repo that git doesn't ignore, including other docs such as CLAUDE.md and
# the skills in .claude/skills, except this skill. Spec IDs cited in source files are checked too.
#
# The history checks look only at lines added since the base branch, uncommitted ones included.
# A line someone kept on purpose is then never flagged again. The other checks look at every doc.
#
# A requirement that nothing cites is flagged only if something cited it on the base branch. A
# requirement written before the code that meets it is normal, but one that lost its last citation
# may have lost its code or its test. With --uncited, every requirement that nothing cites is
# flagged instead, for a look at the docs and the code as a whole.
#
# When a change adds an item to a section, or edits one in it, each citation of that section from
# before the change is flagged. The citation now covers the item, and may not fit it.
#
# It writes no files, so it runs where nothing is writable, such as an eval sandbox. Each list it
# builds is kept in a variable, and passed to a command that needs a file through <(...).
#
# Prints one line per thing it flags:  RULE|SIGNAL <file>:<line> <what>
# RULE means a rule was broken. SIGNAL means only that something is worth a look.
# It exits 0 whenever it ran. What happens to the findings is up to the project's workflow.

set -u

usage() { echo "usage: check-docs.sh [--uncited] <docs folder> <base branch>, run from the repo root" >&2; exit 2; }
all_uncited=
[[ ${1:-} == --uncited ]] && { all_uncited=1; shift; }
[[ $# -eq 2 && -d $1 ]] || usage
[[ $(git rev-parse --show-toplevel 2>/dev/null) == "$PWD" ]] || usage
base=$(git merge-base "$2" HEAD 2>/dev/null) || usage
docs_dir=${1%/}
blueprints_dir=$(realpath -m "$docs_dir/blueprints")
research_dir=$(realpath -m "$docs_dir/research")
self_dir=$(realpath "$(dirname "$0")/..")
self_rel=$(realpath --relative-to=. "$self_dir")
ids='(FR|TR|AD|TD|CS)-[0-9]+'
sec_ids='[FT]-SEC-[0-9]+'

# Prints a list kept in a variable, one item per line. An empty list prints nothing.
lines() { [[ -z $1 ]] || printf '%s\n' "$1"; }
# Whether a list kept in a variable has a line that is exactly the second argument.
has_line() { [[ $'\n'$1$'\n' == *$'\n'"$2"$'\n'* ]]; }

# --- Which files are which ---------------------------------------------------------------------

is_blueprint() { [[ $(realpath -m "$1") == "$blueprints_dir"/* ]]; }

md_files=$(find "$docs_dir" -name '*.md' -type f | sed 's|^\./||' | sort)
fspec=$(lines "$md_files" | xargs -d '\n' -r grep -lE '^#+ F-SEC-[0-9]+')
tspec=$(lines "$md_files" | xargs -d '\n' -r grep -lE '^#+ T-SEC-[0-9]+')
specs=$(lines "$fspec"; lines "$tspec")
docs=$({ lines "$specs"; while read -r f; do is_blueprint "$f" && echo "$f"; done < <(lines "$md_files"); } | sort -u)

# The same rule picks the source files in the base commit, further down.
is_src() {
  awk -v self="$self_rel/" '/\.(ts|tsx|js|mjs|cjs|py|sh|md|txt)$/ &&
    (!/^\.claude\// || (/^\.claude\/skills\/.*\.md$/ && index($0, self) != 1))'
}
src=$(git ls-files --cached --others --exclude-standard | is_src |
  grep -vxFf <(lines "$docs") | while read -r f; do [[ -f $f ]] && echo "$f"; done | sort)

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

# Only the specs are checked, since a blueprint can hold history. Each match prints as
# "<line> <what>", and only matches on added lines are kept.
months='(January|February|March|April|May|June|July|August|September|October|November|December)'
while read -r f; do
  prose=$(prose "$f" scenarios | sed -E 's/\]\([^)]*\)/]/g')
  hist=$({
    grep -noE "\b20[0-9]{2}-[0-9]{2}-[0-9]{2}\b|\b$months [0-9]{1,2}\b" <(lines "$prose") |
      while IFS=: read -r n m; do echo "$n date: $m"; done
    grep -noE '(^|[^A-Za-z0-9&/])#[0-9]+\b' <(lines "$prose") |
      while IFS=: read -r n m; do echo "$n issue or PR number: ${m#"${m%%#*}"}"; done
    grep -noiwE 'settled|decided|drafted|assumption|for now|to come|in progress|no longer|used to|the new' \
      <(lines "$prose") | while IFS=: read -r n m; do echo "$n marker word: $m"; done
    grep -niwE 'was\b.*\bnow' <(lines "$prose") | cut -d: -f1 | while read -r n; do echo "$n \"was ... now\""; done
  })
  added_lines "$f" | awk -v f="$f" 'NR == FNR { added[$1]; next }
    ($1 in added) { n = $1; $1 = ""; print "SIGNAL " f ":" n " may be history:" $0 }' - <(lines "$hist")
done < <(lines "$specs")

# --- References --------------------------------------------------------------------------------

# Definitions: file, line, ID.
defs=$(while read -r f; do
  grep -noE "^\*\*$ids\.\*\*" "$f" | sed -E 's/\*//g; s/\.$//' | sed "s|^|$f:|"
  grep -noE "^#+ $sec_ids" "$f" | sed -E 's/#+ //' | sed "s|^|$f:|"
done < <(lines "$specs"))
defined=$(lines "$defs" | cut -d: -f3 | sort -u)

# Each ID defined twice in one doc, and each item in the wrong spec.
lines "$defs" |
  awk -F: '{ k = $1 FS $3 } seen[k]++ { print "RULE " $1 ":" $2 " " $3 " is defined twice in this doc" }'
while IFS=: read -r f n id; do
  if has_line "$fspec" "$f" && [[ $id =~ ^(TR|AD|TD|CS|T-SEC) ]]; then
    echo "RULE $f:$n $id belongs in the technical spec"
  elif has_line "$tspec" "$f" && [[ $id =~ ^(FR|F-SEC) ]]; then
    echo "RULE $f:$n $id belongs in the functional spec"
  fi
done < <(lines "$defs")

# Citations in docs and source files: file, line, ID. Definitions count too.
all=$(lines "$docs"; lines "$src")
cites=$(lines "$all" | xargs -d '\n' -r grep -HnoE "\b($ids|$sec_ids)\b")
awk -F: 'NR == FNR { d[$1]; next } !($3 in d) { print "RULE " $1 ":" $2 " cites " $3 ", which isn'\''t defined" }' \
  <(lines "$defined") <(lines "$cites")

# The line numbers inside a spec's Terms section, for a spec read from stdin. A section ends at the
# next heading of its level or higher.
terms_lines() {
  awk '
    /^#+ / { lvl = match($0, /[^#]/) - 1
      if (terms && lvl <= terms) terms = 0
      if ($0 ~ /^#+ [FT]-SEC-[0-9]+\. Terms[ \t]*$/) { terms = lvl; next } }
    terms { print FNR }'
}

# How often each ID appears outside Terms sections, as "<count> <ID>". Takes the Terms lines as
# "file:line" and the citations as "file:line:ID". A citation from Terms doesn't count, since a
# term only explains a word, so the requirement may still be unbuilt.
counts() {
  awk -F: 'FILENAME == ARGV[1] { t[$1 FS $2]; next } !(($1 FS $2) in t) { print $3 }' \
    <(lines "$1") <(lines "$2") | sort | uniq -c
}

# Requirements that nothing cites: their only appearance is the definition.
terms=$(while read -r f; do terms_lines <"$f" | sed "s|^|$f:|"; done < <(lines "$specs"))
once=$(counts "$terms" "$cites" | awk '$1 == 1 { print $2 }')

# Requirements cited on the base: the definition and at least one citation. The files are the
# docs and source files in the base commit, found by the same rules as above.
if [[ -z $all_uncited ]]; then
  base_files=$(git ls-tree -r --name-only "$base" | is_src)
  base_cites=$(lines "$base_files" | xargs -d '\n' -r git grep -nowE "$ids|$sec_ids" "$base" -- |
    sed "s|^$base:||")
  base_specs=$(lines "$base_files" | xargs -d '\n' -r git grep -lE '^#+ [FT]-SEC-[0-9]+' "$base" -- |
    sed "s|^$base:||")
  base_terms=$(while read -r f; do
    git show "$base:$f" | terms_lines | sed "s|^|$f:|"
  done < <(lines "$base_specs"))
  cited_before=$(counts "$base_terms" "$base_cites" | awk '$1 > 1 { print $2 }')
fi

lines "$defs" | grep -E ":(FR|TR)-" | while IFS=: read -r f n id; do
  has_line "$once" "$id" || continue
  if [[ -n $all_uncited ]]; then
    echo "SIGNAL $f:$n $id isn't cited anywhere, so it may be unbuilt or untested"
  elif has_line "$cited_before" "$id"; then
    echo "SIGNAL $f:$n $id was cited on the base branch and isn't now, so it may be unbuilt or untested"
  fi
done

# Older citations of a section that this change adds an item to, or edits an item in. A citation of
# a section means whatever the section holds now, so it may now cover an item it shouldn't.
# A citation on an added line is left out, since it was written against the section as it is now.
# First, each item in the specs, as "<file> <ID> <first line> <last line> <sections>". An item is
# its own paragraph. Its sections are the one it's in and the ones around that.
items=$(while read -r f; do
  awk -v f="$f" '
    function flush(   s, l) {
      if (id == "") return
      s = ""; for (l = 1; l <= 9; l++) if (sec[l] != "") s = s " " sec[l]
      print f "\t" id "\t" from "\t" to "\t" s; id = ""
    }
    /^[ \t>]*(```|~~~)/ { flush(); fence = !fence; next }
    fence { next }
    /^#+ / { flush(); lvl = match($0, /[^#]/) - 1
      for (l = lvl; l <= 9; l++) sec[l] = ""
      if (match($0, /[FT]-SEC-[0-9]+/) && RSTART == lvl + 2) sec[lvl] = substr($0, RSTART, RLENGTH)
      next }
    /^[ \t>]*$/ { flush(); next }
    /^[ \t>]*\*\*(FR|TR|AD|TD|CS)-[0-9]+\.\*\*/ { flush()
      match($0, /(FR|TR|AD|TD|CS)-[0-9]+/); id = substr($0, RSTART, RLENGTH); from = FNR }
    { to = FNR }
    END { flush() }
  ' "$f"
done < <(lines "$specs"))

# Then each section with an added or edited item, as "<section> <ID>".
declare -A added
grown=$(while IFS=$'\t' read -r f id from to secs; do
  [[ -v added[$f] ]] || added[$f]=$(added_lines "$f")
  lines "${added[$f]}" | awk -v a="$from" -v b="$to" '$1 >= a && $1 <= b { hit = 1; exit }
    END { exit !hit }' || continue
  for s in $secs; do echo "$s $id"; done
done < <(lines "$items"))

if [[ -n $grown ]]; then
  while IFS=: read -r f n s; do
    changed=$(lines "$grown" | awk -v s="$s" '$1 == s && !seen[$2]++ { printf "%s%s", sep, $2; sep = ", " }')
    [[ -n $changed ]] || continue
    has_line "$defs" "$f:$n:$s" && continue
    [[ -v added[$f] ]] || added[$f]=$(added_lines "$f")
    has_line "${added[$f]}" "$n" && continue
    echo "SIGNAL $f:$n cites $s, which this change adds to or edits: $changed. Check that the citation still fits"
  done < <(lines "$cites" | grep -E ":$sec_ids$" | sort -u)
fi

# ID ranges.
lines "$all" | xargs -d '\n' -r grep -HnoE "\b$ids( (to|through) | ?[-–—] ?)(($ids)|[0-9]+)\b" |
  while IFS=: read -r f n m; do echo "RULE $f:$n cites a range: $m"; done

# Links in docs.
while read -r f; do
  prose "$f" | grep -noE '\]\([^)]+\)' | while IFS=: read -r n m; do
    target=${m#](}; target=${target%)}; target=${target%%#*}; target=${target%% *}
    [[ -z $target || $target =~ ^[a-z]+: ]] && continue
    path=$(realpath -m "$(dirname "$f")/$target")
    [[ -e $path ]] || echo "RULE $f:$n links to $target, which doesn't exist"
    if has_line "$fspec" "$f"; then
      echo "RULE $f:$n the functional spec links out, to $target"
    elif [[ $path == "$blueprints_dir"/* ]] && ! is_blueprint "$f"; then
      echo "RULE $f:$n links to a blueprint, $target"
    fi
  done
done < <(lines "$docs")

# --- Item shape --------------------------------------------------------------------------------

while read -r f; do
  awk -v f="$f" '
    function flush() { if (para != "") check(para, start); para = "" }
    # A design decision cites the requirement it meets in its own line or its Why.
    function cites_req(t) { return t ~ /(^|[^A-Za-z])(FR|TR)-[0-9]+/ }
    function check_td(p) {
      if (td_id == "") return
      if (p ~ /^\*Why:\*/ && cites_req(p)) td_ok = 1
      if (!td_ok) print "RULE " f ":" td_line " " td_id " cites no requirement, an FR or a TR, in its line or its Why"
      td_id = ""
    }
    function check(p, n,   id, body, pre, w, i, k, last, order) {
      check_td(p)
      if (match(p, /^\*\*(FR|TR|AD|TD|CS)-[0-9]+\.\*\*/)) {
        if (why_id != "") print "RULE " f ":" why_line " " why_id " has no Why line right after it"
        why_id = ""
        id = substr(p, 3, RLENGTH - 5); body = substr(p, RLENGTH + 2)
        req_id = ""
        if (id ~ /^TD/) { td_id = id; td_line = n; td_ok = cites_req(body) }
        # A code standard gets a Why only when it needs one, as a requirement does.
        if (id ~ /^CS/) return
        if (id ~ /^(AD|TD)/) { why_id = id; why_line = n; return }
        req_id = id; req_body = body
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
      # Under a requirement, only labeled lines, and a table that the requirement text points to.
      # A "shall" paragraph is left to the no-ID check below, so one problem gets one line.
      if (p ~ /^#/) req_id = ""
      if (req_id != "") {
        if (p ~ /^\|/) {
          if (tolower(req_body) !~ /table/)
            print "RULE " f ":" n " a table under " req_id ", whose text doesn'\''t point to it"
        } else if (p !~ /^\*(Why|Scenario|Accepted gap):\*/ && p !~ /(^|[^A-Za-z])shall([^A-Za-z]|$)/)
          print "RULE " f ":" n " a paragraph under " req_id " with no label, such as Why or Scenario"
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
    END { flush(); check_td("")
      if (why_id != "") print "RULE " f ":" why_line " " why_id " has no Why line right after it" }
  ' "$f"
done < <(lines "$specs")

# --- Copies ------------------------------------------------------------------------------------

# Every run of eight words, with the file and line it starts on. Research docs in
# <docs folder>/research are left out. They're frozen records that no agent reads as a current
# rule, and specs are often written from them, so shared text there is expected.
runs() {
  { lines "$docs"; lines "$src"; } | while read -r f; do
    [[ $(realpath -m "$f") == "$research_dir"/* ]] && continue
    awk -v f="$f" '{
      s = tolower($0); gsub(/[^a-z0-9'\'']+/, " ", s); k = split(s, w, " ")
      for (i = 1; i <= k; i++) { buf[++nw] = w[i]; at[nw] = FNR
        if (nw >= 8) { r = buf[nw-7]; for (j = nw-6; j <= nw; j++) r = r " " buf[j]; print r "\t" f "\t" at[nw-7] } }
    }' "$f"
  done | sort -t$'\t' -k1,1
}

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
' <(lines "$docs") <(runs) | sort

# --- Size --------------------------------------------------------------------------------------

while read -r f; do
  tokens=$(($(wc -c <"$f") / 4))
  ((tokens > 20000)) && echo "SIGNAL $f:1 about $tokens tokens, and the Read tool reads at most 25,000 in one call"
done < <(lines "$docs")

exit 0
