# Skill

What a skill holds and keeps out, and how it changes. The questions in "Which doc a fact goes in",
in SKILL.md, decide which facts go in one.

Read by only the agent doing that task. Kept current, and changed when the task's steps change.
Skills for one project live in that project.

- **One task per skill,** such as running an evaluation, writing an issue, or restoring a backup.
- **Numbered steps,** each with its reason in the step.
- **Facts about the outside tools the task drives,** such as an observability tool's API or a
  CLI's flags, each with the version it was checked on.
- **Default paths,** for when CLAUDE.md's doc map doesn't name one.
- **Keeps out** facts about how the system works. Cite their one home. If a sentence came out and
  the steps would be done the same way, cut it. Rules other tasks also need go in CLAUDE.md or the
  technical spec.
- **Keeps out** how to run a script whose top comment already says it. Give just the command.
- **Keeps out** paths relative to the skill's own folder, for anything outside the skill.
