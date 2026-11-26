---
type: llm
focus: {source: file, path: docs/functional-spec.md}
weight: 1
---

The spec has a requirement, with its own FR ID, that limits a booking to one organizer with "only", then names what that rules out, such as co-organizers or more than one organizer. For example, "The app shall give each booking only one organizer, not co-organizers" passes. A requirement that says only what the app refuses, with no "only", such as "The app shall not allow co-organizers", fails.
