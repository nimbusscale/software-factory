# The board's settings set by hand

A how-to doc: the settings of the factory's board that GitHub's API can't set, and how to set them
on GitHub. `uv run set-up-board` sets every other setting, from `board.toml` next to this file and
the factory's config.

The API sets a view's name, layout, filter and visible fields, but not how it's grouped, sorted or
sliced. It can delete a built-in workflow, but can't turn one on or off, or choose the status it
sets. These settings rarely change, so they're set by hand, or by an agent working in a browser.

The board is at `https://github.com/users/<owner>/projects/<number>`, with the owner and number in
the `[board]` table of `src/software_factory/factory.toml`. Run `uv run set-up-board --check`
first. If it lists anything, run `uv run set-up-board`, since the views below must exist before
they can be set.

## Views

Open each view by its tab, and change its settings from the View menu at the right of the filter
bar. Then save the view, from Save view in the same menu, and choose Save when GitHub asks to
confirm. GitHub keeps a change to a view only once it's saved.

| View | Column by | Group by | Sort by | Slice by |
|---|---|---|---|---|
| Factory | Status | none | none | none |
| Mine | Status | none | none | none |
| All | (a table) | none | none | Repository |

Factory and Mine show their issues as columns, one for each status. All lists every issue, with a
list of repos beside it to pick from.

## Built-in workflows

Open the board's menu, then Workflows. Set each built-in workflow as the table says, and save it.

| Workflow | Setting |
|---|---|
| Item added to project | On. When an issue is added, set the status to Backlog. |
| Item closed | On. Set the status to Done. |
| Pull request merged | On. Set the status to Done. |
| Auto-close issue | On. Close the issue when its status is set to Done. |
| Auto-add sub-issues to project | On. |
| Auto-add to project | Off, or not there. |
| Pull request linked to issue | Not there. `uv run set-up-board` deletes it. |

A new issue starts in Backlog, so the factory never takes an issue the owner hasn't looked at. The
workflows left on add an issue to the board or move it to Done, and none changes a status the
factory sets. Auto-close issue is how the owner finishes an issue with sub-issues, by moving it to
Done.

Auto-add to project isn't used, since GitHub Free allows one, which adds the issues of one repo.
Each repo on the board has the `actions/add-to-project` Action instead.
