#!/bin/bash
# Pull all issues and PRs with bodies, comments, edit counts and links.
set -e
OUT=$1
gh api graphql --paginate -f query='
query($endCursor: String) {
  repository(owner: "nimbusscale", name: "road-trip-agent") {
    issues(first: 20, after: $endCursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title body state stateReason createdAt closedAt
        author { login }
        labels(first: 20) { nodes { name } }
        userContentEdits(first: 100) { totalCount nodes { createdAt editor { login } } }
        comments(first: 100) { totalCount nodes { author { login } createdAt body } }
        projectItems(first: 5) { nodes { fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } } } }
        timelineItems(first: 100, itemTypes: [CROSS_REFERENCED_EVENT, CLOSED_EVENT, REOPENED_EVENT, CONNECTED_EVENT]) {
          nodes {
            __typename
            ... on CrossReferencedEvent { createdAt source { __typename ... on PullRequest { number } ... on Issue { number } } }
            ... on ClosedEvent { createdAt closer { __typename ... on PullRequest { number } } }
            ... on ReopenedEvent { createdAt }
          }
        }
      }
    }
  }
}' --jq '.data.repository.issues.nodes[]' > "$OUT/issues.jsonl"

gh api graphql --paginate -f query='
query($endCursor: String) {
  repository(owner: "nimbusscale", name: "road-trip-agent") {
    pullRequests(first: 15, after: $endCursor, orderBy: {field: CREATED_AT, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title body state createdAt mergedAt closedAt isDraft headRefName
        author { login }
        additions deletions changedFiles
        labels(first: 20) { nodes { name } }
        userContentEdits(first: 100) { totalCount }
        commits { totalCount }
        closingIssuesReferences(first: 10) { nodes { number } }
        comments(first: 100) { totalCount nodes { author { login } createdAt body } }
        reviews(first: 50) { totalCount nodes { author { login } state createdAt body } }
        reviewThreads(first: 100) { totalCount nodes { isResolved comments(first: 20) { totalCount nodes { author { login } createdAt body path } } } }
      }
    }
  }
}' --jq '.data.repository.pullRequests.nodes[]' > "$OUT/prs.jsonl"
wc -l "$OUT"/*.jsonl
