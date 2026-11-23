# What goes in your report

The questions in "Which doc a fact goes in" in `project-docs.md` sort some facts out of the docs.
Each of those goes in your report, so whoever gave you the task can decide what happens to it
next:

- **About the past or the work in progress** (question 1). Keep notes in a file in the session's
  scratchpad while you work, and write the commit message from them. Name any work left to do.
- **About something other than what the app does and how it's built** (question 2), including
  commands and pointers kept out of the technical spec. Name it, with where it likely belongs,
  such as a skill, a research doc or a README.
- **A decision not made yet.** Name it as a decision still to make, such as one that needs a spike
  to settle.
- **Not settled by the source,** including an option named with "may", "could" or "such as".
  Raise it as a question: quote the source text, say what's unclear, and suggest an answer. When a
  sentence only makes sense under one option, ask about the two together. For example, when notes
  say an app "may keep a copy of the orders on the phone" and that the order list "syncs to the
  phone", ask whether the app keeps a copy, and say the sync depends on the answer.
- **A decision with no reason in the source,** whether its home is a spec, a code comment, or a
  blueprint until the code exists. Ask for the reason: quote the decision, and suggest a reason if
  you have one. If you can't tell whether anyone had another option, ask that too: was another way
  weighed, and if so, why this one? In a spec, the check script flags the missing Why until the
  reason is known. A fact with no other option isn't a decision, so don't ask for its reason. Say
  where its home is instead.
