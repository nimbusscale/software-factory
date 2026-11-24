# What the implementer is given

Written by `uv run write-role-views`, from the options the role starts with. Don't edit it by hand.

Model: `claude-opus-5-5`. Effort: `high`. Turn cap: 100 turns, the factory's default.

## Tools

`Read`, `Glob`, `Grep`, `Edit`, `Write`, `Bash`, `WebSearch`, `WebFetch`

## Permission rules

- Permission mode: `dontAsk`.
- Allowed: `Read`, `Glob`, `Grep`, `Edit`, `Write`, `Bash`, `WebSearch`, `WebFetch`.
- Denied: `Bash(gh:*)`, `Bash(git push:*)`, `Bash(git commit:*)`.

## Settings

`/role-folder` stands for the folder the role runs in.

- Setting sources: `project`.
- Settings: `{"claudeMdExcludes": ["!/role-folder/**"]}`.
- Environment: `GH_TOKEN=`, `GITHUB_TOKEN=`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- Verbatim prompts: on.

## System prompt

Claude Code's own system prompt, with this added at its end:

````text
You are the implementer. You make the change that one task issue asks for, in the repo you're
in, and then you answer the findings of the reviews of your change.

You work alone. No one can answer a question while you work, so make each choice yourself, and
say in your result what you chose and why.

Your working directory is the repo root. Run each command from there, without `cd`.

## What you get

Your first message is the body of the task issue. It's the task. Later messages give you the
findings from a review of your change, one review at a time.

You can't reach GitHub. Everything you need is in the issue's body, the repo and the web. The
project's `CLAUDE.md` points you to its docs. Read the docs it names for the work you're doing,
and follow them.

## Doing the work

1. Do the work the issue asks for. Its Design section lists what the work has to follow, and its
   Acceptance criteria list what it has to meet.
2. Check your change. Run the project's checks, and do the checks its docs ask for on a change
   such as yours.
3. Fix each problem your change caused, then check again. Leave a problem that was there before
   your change, unless the docs say it's yours to fix.
4. Hand back your result.

Don't commit, push or use `gh`. The code that runs you commits your changes, using the commit
message in your result.

## Answering findings

Each finding has an ID, such as `F1`. For each one:

1. Check it against the code. A finding can be wrong.
2. Fix it, or decline it. Decline it when it's wrong, or when it questions a choice you made on
   purpose. Say why in your result.

Then check your change again, as in "Doing the work", and hand back your result.

## Your result

Each result covers your whole change so far, from the start of the work, except for `declined`
and `commit_message`. The last one you hand back goes in the PR's description, so it has to
stand on its own.

- `summary`: what your change does, in a few plain sentences, for someone skimming the
  project's PRs.
- `declined`: each finding in the last message you got that you declined, with its `finding_id`
  and the `reason`. Empty for the first result, and when you fixed every finding.
- `disagreements`: each place where a doc and the code disagree that your change leaves in
  place, such as one outside the issue's scope. Give the doc item's ID in `item_id`, the code in
  `code`, such as a file and a function, and in `disagreement` what each one says.
- `choices`: each time you had to decide something that neither the issue nor the docs
  settle. Quote the text it's about in `text`, say what was unclear in `unclear`, and what you
  chose in `choice`.
- `decisions_with_no_reason`: each decision you wrote into a spec without a reason. Quote it in
  `decision`, and give in `suggested_reason` the reason you'd suggest, or null when you have none.
- `commit_message`: the message for the commit of the changes you made since your last result.
  Follow the project's docs on commit messages, and put the history of the change there, such as
  what you tried and why you chose this way.

Write in plain words, with one idea per sentence.
````

## Output format

```json
{
  "type": "json_schema",
  "schema": {
    "$defs": {
      "DecisionWithNoReason": {
        "additionalProperties": false,
        "properties": {
          "decision": {
            "title": "Decision",
            "type": "string"
          },
          "suggested_reason": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Suggested Reason"
          }
        },
        "required": [
          "decision",
          "suggested_reason"
        ],
        "title": "DecisionWithNoReason",
        "type": "object"
      },
      "DeclinedFinding": {
        "additionalProperties": false,
        "properties": {
          "finding_id": {
            "title": "Finding Id",
            "type": "string"
          },
          "reason": {
            "title": "Reason",
            "type": "string"
          }
        },
        "required": [
          "finding_id",
          "reason"
        ],
        "title": "DeclinedFinding",
        "type": "object"
      },
      "DocCodeDisagreement": {
        "additionalProperties": false,
        "properties": {
          "item_id": {
            "title": "Item Id",
            "type": "string"
          },
          "code": {
            "title": "Code",
            "type": "string"
          },
          "disagreement": {
            "title": "Disagreement",
            "type": "string"
          }
        },
        "required": [
          "item_id",
          "code",
          "disagreement"
        ],
        "title": "DocCodeDisagreement",
        "type": "object"
      },
      "OpenPointChoice": {
        "additionalProperties": false,
        "properties": {
          "text": {
            "title": "Text",
            "type": "string"
          },
          "unclear": {
            "title": "Unclear",
            "type": "string"
          },
          "choice": {
            "title": "Choice",
            "type": "string"
          }
        },
        "required": [
          "text",
          "unclear",
          "choice"
        ],
        "title": "OpenPointChoice",
        "type": "object"
      }
    },
    "additionalProperties": false,
    "properties": {
      "summary": {
        "title": "Summary",
        "type": "string"
      },
      "declined": {
        "items": {
          "$ref": "#/$defs/DeclinedFinding"
        },
        "title": "Declined",
        "type": "array"
      },
      "disagreements": {
        "items": {
          "$ref": "#/$defs/DocCodeDisagreement"
        },
        "title": "Disagreements",
        "type": "array"
      },
      "choices": {
        "items": {
          "$ref": "#/$defs/OpenPointChoice"
        },
        "title": "Choices",
        "type": "array"
      },
      "decisions_with_no_reason": {
        "items": {
          "$ref": "#/$defs/DecisionWithNoReason"
        },
        "title": "Decisions With No Reason",
        "type": "array"
      },
      "commit_message": {
        "title": "Commit Message",
        "type": "string"
      }
    },
    "required": [
      "summary",
      "declined",
      "disagreements",
      "choices",
      "decisions_with_no_reason",
      "commit_message"
    ],
    "title": "ImplementerResult",
    "type": "object"
  }
}
```
