# Skill description eval

A fixed copy of skill-creator's scripts for testing and tuning a skill's description. They check
whether the description makes an agent load the skill for a list of prompts. They don't grade any
work.

Use them while developing a description: they're fast and cheap. They aren't the real test. Every
loading case also has to pass as a `claude plugin eval` case, which runs the real skill in the
case's setup and watches the whole run.

## Where it came from

Copied from the `skill-creator` plugin in `anthropics/claude-plugins-official`, at commit
`6d491811023d7af2c96a7fab274935922b29ed01`. Only the scripts for description tuning came across:
`run_eval.py`, `improve_description.py`, `run_loop.py`, `utils.py` and `generate_report.py`. The
license is Apache 2.0, in `LICENSE.txt`.

## What was changed

All changes are in `run_eval.py`, plus the option passed through `run_loop.py`.

- **The test skill goes in `.claude/skills/<name>/SKILL.md`.** Upstream writes it to
  `.claude/commands/<name>.md`. Claude Code doesn't offer a commands file through the Skill tool,
  so upstream scores every prompt as "didn't load". This is upstream issue
  [#2503](https://github.com/anthropics/claude-plugins-official/issues/2503). Checked on Claude
  Code 2.1.328: a prompt that named the skill outright loaded it 0 of 3 times.
- **Each run gets its own temp folder.** Upstream puts every run's test skill in one shared folder.
  With 10 runs at once, each agent sees 10 copies of the skill, often loads another run's copy, and
  that counts as a miss. With the location fixed but the folder shared, the same prompt loaded
  1 of 3. With a folder per run, it loaded 3 of 3. Upstream's issue doesn't mention this one.
- **New `--project-dir` option.** Each run's folder starts as a copy of this folder, such as a sample
  project with specs. Without it, each run starts in an empty folder. If the copy has its own copy
  of the skill under `.claude/skills/<name>/`, it's removed, so it doesn't compete with the test
  skill.

Drop this copy once upstream fixes both bugs.

## How to run it

Run from this folder, since the scripts import each other as `scripts.*`.

An eval set is a JSON list of prompts, each marked whether the skill should load:

```json
[
  {"query": "add a rule that bookings close at 6pm", "should_trigger": true},
  {"query": "what does check_booking_limit do?", "should_trigger": false}
]
```

Score one description:

```bash
python3 -m scripts.run_eval \
  --eval-set <eval-set.json> \
  --skill-path ../../.claude/skills/writing-project-docs \
  --project-dir <sample-project> \
  --verbose
```

Tune it with the improvement loop:

```bash
python3 -m scripts.run_loop \
  --eval-set <eval-set.json> \
  --skill-path ../../.claude/skills/writing-project-docs \
  --project-dir <sample-project> \
  --model claude-opus-5-5 \
  --max-iterations 5 \
  --report none \
  --results-dir ../../scratch/<run-name> \
  --verbose
```

The loop holds back 40% of the prompts as a test set and rewrites the description using only the
other 60%. It runs each prompt 3 times, and counts the skill as loaded if it loaded in at least half
of them. It rewrites the description up to 5 times, and returns the one that scored best on the
held-back prompts as `best_description`. Leave out `--report none` to have it open a live HTML
report in a browser.

Neither script changes `SKILL.md`. To try a description, pass it with `--description`.

## What it can't tell you

- **It counts only the agent's first tool call.** If the agent lists a folder or opens a spec first
  and then loads the skill, it's scored as a miss. So it can't test a skill that should load
  partway through a task. Only a plugin eval case can.
- **The agent sees the skill's name, not just its description.** A telling name can make the skill
  load even with a poor description.
- **The runs use your own setup.** `claude -p` loads your `~/.claude/CLAUDE.md`, your skills and
  your plugins, so they compete with the test skill as they would in your own sessions.
- **The test skill has only a description**, so a run that loads it gets no guidance. That's fine
  here, since only the load is scored.
- **Rewrites don't follow our rules for descriptions.** For example, one rewrite came out as "Use
  this skill when…", not in the third person. Treat `best_description` as a draft to edit.

Every prompt run is a `claude -p` call. A run of 20 prompts, 3 times each, over 5 loop iterations is
up to 300 calls, plus one call per rewrite.
