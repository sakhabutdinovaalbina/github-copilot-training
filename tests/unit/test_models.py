import pytest
from pydantic import ValidationError

from app.models import DeveloperTask, ProductivityReport, TaskCompletionMetrics, TaskStatus


def test_task_status_has_expected_values() -> None:
    assert TaskStatus.PENDING.value == "pending"
    assert TaskStatus.IN_PROGRESS.value == "in_progress"
    assert TaskStatus.COMPLETE.value == "complete"


def test_task_status_parses_valid_string_values() -> None:
    assert TaskStatus("pending") is TaskStatus.PENDING
    assert TaskStatus("in_progress") is TaskStatus.IN_PROGRESS
    assert TaskStatus("complete") is TaskStatus.COMPLETE


def test_task_status_raises_for_invalid_value() -> None:
    with pytest.raises(ValueError):
        TaskStatus("done")


def test_developer_task_creates_with_defaults() -> None:
    task = DeveloperTask(task_id=1, title="Implement endpoint")

    assert task.task_id == 1
    assert task.title == "Implement endpoint"
    assert task.status == TaskStatus.PENDING
    assert task.hours_spent == 0.0


def test_developer_task_creates_with_explicit_values() -> None:
    task = DeveloperTask(
        task_id=2,
        title="Write tests",
        status=TaskStatus.IN_PROGRESS,
        hours_spent=3.5,
    )

    assert task.task_id == 2
    assert task.title == "Write tests"
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.hours_spent == 3.5


def test_developer_task_raises_when_title_missing() -> None:
    with pytest.raises(ValidationError):
        DeveloperTask(task_id=3)


def test_developer_task_raises_for_invalid_status() -> None:
    with pytest.raises(ValidationError):
        DeveloperTask(task_id=4, title="Bad status", status="finished")


def test_developer_task_coerces_numeric_hours_spent() -> None:
    task = DeveloperTask(task_id=5, title="Refactor", hours_spent=2)

    assert isinstance(task.hours_spent, float)
    assert task.hours_spent == 2.0


def test_productivity_report_creates_with_valid_data() -> None:
    report = ProductivityReport(
        total_tasks=10,
        completed_tasks=7,
        total_hours_spent=25.5,
        completion_rate=0.7,
    )

    assert report.total_tasks == 10
    assert report.completed_tasks == 7
    assert report.total_hours_spent == 25.5
    assert report.completion_rate == 0.7


def test_productivity_report_raises_when_required_field_missing() -> None:
    with pytest.raises(ValidationError):
        ProductivityReport(
            total_tasks=10,
            completed_tasks=7,
            total_hours_spent=25.5,
        )


def test_task_completion_metrics_creates_with_valid_data() -> None:
    metrics = TaskCompletionMetrics(
        total_tasks=8,
        completed_tasks=5,
        pending_tasks=3,
    )

    assert metrics.total_tasks == 8
    assert metrics.completed_tasks == 5
    assert metrics.pending_tasks == 3


def test_task_completion_metrics_raises_when_required_field_missing() -> None:
    with pytest.raises(ValidationError):
        TaskCompletionMetrics(total_tasks=8, completed_tasks=5)
