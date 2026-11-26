# Status

Last run: 2026-11-26, with the standards loaded from the factory plugin. It passed 2 of 3. Every
earlier run passed.

## Known failure

`02-technical-spec-has-tags-file` failed in 1 run: the technical spec had no decision about the
tags file. The agent added FR-4 and FR-5 for tags, and asked in its reply why tags are kept in their
own file. It offered to put the reason in a code comment once it knew it, so no one moves tags into
the notes later. So it took the code, not the technical spec, as the decision's home.

"Which doc a fact goes in" in `project-docs.md` sends a decision to a comment only when every case
of it goes through one place in the code. New code could keep tags inside a note without touching
`TAGS_FILE`, so the decision belongs in the technical spec. If it keeps failing this way, that
question could give an example of a storage choice that new code could break.
