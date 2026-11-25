from typing import TYPE_CHECKING

from software_factory.github.pull_request import MARK_NAMES, where

if TYPE_CHECKING:
    from collections.abc import Collection, Sequence

    from software_factory.github.pull_request import NumberedFinding

FINDINGS_INTRO = (
    "The quality reviewer reviewed your change. Here are its findings. Fix each one,"
    " or decline it with a reason."
)


def findings_message(given: Sequence[NumberedFinding]) -> str:
    """The message that gives the implementer a round's findings (FR-9)."""
    parts = [FINDINGS_INTRO]
    parts.extend(finding_text(numbered, declined=False) for numbered in given)
    return "\n\n".join(parts) + "\n"


def reviewer_message(
    issue_body: str,
    earlier: Sequence[NumberedFinding],
    declined_ids: Collection[str],
) -> str:
    """The message that starts the quality reviewer in a round (TR-7).

    `earlier` holds the findings from the run's earlier rounds, and `declined_ids` the
    IDs of the ones the implementer declined.
    """
    # Tags, not headings, since the issue's body has headings of its own.
    earlier_text = (
        "\n\n".join(
            finding_text(n, declined=n.finding_id in declined_ids) for n in earlier
        )
        if earlier
        else "None."
    )
    return (
        "The body of the run's task issue:\n\n"
        f"<issue>\n{issue_body.strip()}\n</issue>\n\n"
        "The findings from the run's earlier rounds:\n\n"
        f"<earlier_findings>\n{earlier_text}\n</earlier_findings>\n"
    )


def finding_text(numbered: NumberedFinding, *, declined: bool) -> str:
    finding = numbered.finding
    # The mark alone, with no reason, so the reviewer doesn't raise a declined finding
    # again (TR-10).
    declined_mark = ", declined by the implementer" if declined else ""
    return (
        f"### {numbered.finding_id}, {with_article(MARK_NAMES[finding.mark])}"
        f"{declined_mark}\n\n"
        f"{where(finding)}, labeled {finding.label}.\n\n"
        f"**Problem:** {finding.problem}\n\n"
        f"**Where it goes wrong:** {finding.failure_case}\n\n"
        f"**Why this label:** {finding.label_reason}"
    )


def with_article(name: str) -> str:
    return f"{'an' if name[0] in 'aeiou' else 'a'} {name}"
