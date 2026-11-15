---
type: regex
target: {source: file, path: docs/functional-spec.md}
match: not_contains
flags: mi
---

^- \*\*Organizer\.\*\*(?:.|\n(?!- |\n))*?\bFR-\d+
