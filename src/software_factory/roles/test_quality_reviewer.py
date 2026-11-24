import pytest
from pydantic import ValidationError

from software_factory.roles.implementer import IMPLEMENTER
from software_factory.roles.quality_reviewer import (
    REVIEW_TARGET_PLACEHOLDER,
    UNCOMMITTED_CHANGES,
    QualityReviewerResult,
    quality_reviewer,
)

FINDING = {
    "id": "F1",
    "file": "src/trip.py",
    "line": 12,
    "label": "F1",
    "mark": "important",
    "problem": "A trip of 15 days saves.",
    "failure_case": "Save a trip of 15 days.",
    "label_reason": "The app does the wrong thing in normal use.",
}


def test_prompt_names_the_review_target_on_its_first_line() -> None:
    prompt = quality_reviewer(UNCOMMITTED_CHANGES).prompt

    assert prompt.splitlines()[0] == "Review target: the changes not yet committed"
    assert REVIEW_TARGET_PLACEHOLDER not in prompt


def test_is_a_different_agent_from_the_implementer() -> None:
    reviewer = quality_reviewer(UNCOMMITTED_CHANGES)

    assert reviewer.name != IMPLEMENTER.name
    assert reviewer.prompt != IMPLEMENTER.prompt


def test_has_no_tool_that_edits() -> None:
    tools = quality_reviewer(UNCOMMITTED_CHANGES).tools

    assert not {"Edit", "Write", "NotebookEdit"} & set(tools)


def test_result_needs_the_dropped_list_even_when_its_empty() -> None:
    with pytest.raises(ValidationError, match="dropped"):
        QualityReviewerResult.model_validate(
            {"status": "done", "reason": "No findings.", "findings": []}
        )


@pytest.mark.parametrize("mark", ["important", "pre_existing", "nit", "to_check"])
def test_finding_takes_each_mark(mark: str) -> None:
    result = QualityReviewerResult.model_validate(
        {
            "status": "done",
            "reason": "1 finding.",
            "findings": [{**FINDING, "mark": mark}],
            "dropped": [],
        }
    )

    assert result.findings[0].mark == mark


def test_finding_refuses_any_other_mark() -> None:
    with pytest.raises(ValidationError, match="mark"):
        QualityReviewerResult.model_validate(
            {
                "status": "done",
                "reason": "1 finding.",
                "findings": [{**FINDING, "mark": "blocker"}],
                "dropped": [],
            }
        )


def test_dropped_candidate_takes_only_the_two_reasons() -> None:
    schema = QualityReviewerResult.model_json_schema()

    dropped_as = schema["$defs"]["DroppedCandidate"]["properties"]["dropped_as"]
    assert dropped_as["enum"] == ["false_claim", "older_note"]
