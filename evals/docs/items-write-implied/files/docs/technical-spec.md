# Technical spec

The technical spec: what the system must achieve that a user wouldn't see (`TR`, in GEARS), the
architecture (`AD`) and design (`TD`) decisions, each with its reason, and the code standards
(`CS`), that new code could follow or break from anywhere. Decisions carried out in one place in
the code are comments there instead.

## T-SEC-1. Architecture decisions

**AD-1.** Python's standard library only, with no other packages.

*Why:* the tool then runs on any machine with Python, with nothing to install.

## T-SEC-2. Storage

How the tool keeps notes between runs.

**TD-1.** Each note gets a whole-number ID that's never used again, even after the note is
deleted, to meet FR-1.

*Why:* an ID someone wrote down then never points to a different note.
