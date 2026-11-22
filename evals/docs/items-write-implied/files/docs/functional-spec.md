# Functional spec

The functional spec: what the app should do, in the user's terms. Requirements are in GEARS, with
`FR` IDs. It never links to other docs. Other docs, prompts and code point to its IDs.

## F-SEC-1. Terms

- **Note.** A piece of text the user saves.

## F-SEC-2. Notes

**FR-1.** When the user adds a note, the tool shall save it and print its ID.

**FR-2.** When the user asks for the list of notes, the tool shall print each note with its ID,
oldest first.

**FR-3.** When the user deletes a note by its ID, the tool shall remove that note.
