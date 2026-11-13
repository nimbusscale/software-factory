#!/bin/bash
# Pull every saved version of the body of each sampled issue and PR. Usage: pull_versions.sh OUTDIR N...
set -e
OUT=$1; shift
for n in "$@"; do
  gh api graphql -F n=$n -f query='
  query($n: Int!) { repository(owner: "nimbusscale", name: "road-trip-agent") {
    issueOrPullRequest(number: $n) {
      __typename
      ... on Issue { number createdAt body userContentEdits(first: 100) { nodes { createdAt editedAt diff } } }
      ... on PullRequest { number createdAt body userContentEdits(first: 100) { nodes { createdAt editedAt diff } } }
  } } }' --jq '.data.repository.issueOrPullRequest' > "$OUT/$n.json"
done
