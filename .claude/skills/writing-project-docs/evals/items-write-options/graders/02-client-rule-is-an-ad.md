---
type: llm
focus: {source: file, path: docs/technical-spec.md}
weight: 1
---

An architecture decision, an item with an `AD` ID, says the client holds no rules logic of its own
beyond what it needs to show a player their options. It can say this in any words, and can be part
of an `AD` that says what the client does. It fails if this rule is missing, or is only in a design
decision (`TD`), a technical requirement (`TR`) or a term.
