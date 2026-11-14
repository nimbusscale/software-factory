# Blueprint

What a blueprint holds, and how it changes. The questions in "Which doc a fact goes in", in
SKILL.md, decide which facts go in one.

Read by the agents building the code it describes. It holds whatever is useful to build from
before the code exists, and nothing is ruled out. It can link to other docs, but other docs don't
link to it, since it's archived once the code is built. It's edited freely until then. When it's
retired, the issue that builds the code lists these steps in its "Done when":

1. Move items that new code elsewhere could break into the technical spec, sorted by the questions
   in "Which doc a fact goes in" in SKILL.md.
2. Check that each rule about one object is a code comment or a test.
3. Turn rules a check can enforce into checks, such as a lint rule for imports.
4. Archive the doc, frozen, with its date and a line saying it isn't kept up to date.
