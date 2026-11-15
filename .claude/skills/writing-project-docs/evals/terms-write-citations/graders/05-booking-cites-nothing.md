---
type: regex
target: {source: file, path: docs/functional-spec.md}
match: not_contains
flags: mi
---

^- \*\*Booking\.\*\*(?:.|\n(?!- |\n))*?\bFR-\d+
