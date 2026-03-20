import asyncio
import copy

import pytest

from app.main import (
    MOCK_TASKS,
    fetch_all_tasks,
    generate_productivity_report,
    get_all_tasks,
    get_productivity_report,
    get_status,
    get_task_status,
    log_task,
)
from app.models import DeveloperTask, TaskStatus


@pytest.fixture(autouse=True)
def restore_mock_tasks() -> None:
    snapshot = copy.deepcopy(MOCK_TASKS)
    yield
    MOCK_TASKS.clear()
    MOCK_TASKS.update(snapshot)


def test_fetch_all_tasks_returns_list() -> None:
    tasks = asyncio.run(fetch_all_tasks())
    assert isinstance(tasks, list)


def test_fetch_all_tasks_returns_all_current_tasks() -> None:
    tasks = asyncio.run(fetch_all_tasks())
    returned_ids = {task.task_id for task in tasks}
    stored_ids = set(MOCK_TASKS.keys())

    assert len(tasks) == len(MOCK_TASKS)
    assert returned_ids == stored_ids


def test_generate_productivity_report_calculates_expected_values() -> None:
    report = asyncio.run(generate_productivity_report())

    expected_total = len(MOCK_TASKS)
    expected_completed = sum(1 for t in MOCK_TASKS.values() if t.status == TaskStatus.COMPLETE)
    expected_hours = round(sum(t.hours_spent for t in MOCK_TASKS.values()), 2)
    expected_rate = round(expected_completed / expected_total, 2) if expected_total else 0.0

    assert report.total_tasks == expected_total
    assert report.completed_tasks == expected_completed
    assert report.total_hours_spent == expected_hours
    assert report.completion_rate == expected_rate


def test_generate_productivity_report_with_empty_store_returns_zeroed_metrics() -> None:
    MOCK_TASKS.clear()

    report = asyncio.run(generate_productivity_report())

    assert report.total_tasks == 0
    assert report.completed_tasks == 0
    assert report.total_hours_spent == 0.0
    assert report.completion_rate == 0.0


def test_get_status_returns_ok_payload() -> None:
    result = asyncio.run(get_status())
    assert result == {"status": "ok"}


def test_get_all_tasks_returns_tasks() -> None:
    result = asyncio.run(get_all_tasks())

    assert isinstance(result, list)
    assert len(result) == len(MOCK_TASKS)
    assert all(isinstance(task, DeveloperTask) for task in result)


def test_get_productivity_report_returns_expected_report() -> None:
    result = asyncio.run(get_productivity_report())

    expected_total = len(MOCK_TASKS)
    expected_completed = sum(1 for t in MOCK_TASKS.values() if t.status == TaskStatus.COMPLETE)

    assert result.total_tasks == expected_total
    assert result.completed_tasks == expected_completed


def test_log_task_assigns_next_id_and_persists() -> None:
    task = DeveloperTask(
        task_id=999,
        title="Add caching to analytics endpoint",
        status=TaskStatus.PENDING,
        hours_spent=2.5,
    )

    response = asyncio.run(log_task(task))
    new_id = response["task_id"]

    assert response["message"] == "Task logged successfully."
    assert new_id == max(MOCK_TASKS.keys())
    assert new_id in MOCK_TASKS
    assert MOCK_TASKS[new_id].title == "Add caching to analytics endpoint"
    assert MOCK_TASKS[new_id].status == TaskStatus.PENDING
    assert MOCK_TASKS[new_id].hours_spent == 2.5


def test_log_task_starts_ids_from_one_when_store_empty() -> None:
    MOCK_TASKS.clear()
    task = DeveloperTask(
        task_id=42,
        title="Bootstrap new project docs",
        status=TaskStatus.IN_PROGRESS,
        hours_spent=1.0,
    )

    response = asyncio.run(log_task(task))

    assert response["task_id"] == 1
    assert response["message"] == "Task logged successfully."
    assert 1 in MOCK_TASKS


def test_get_task_status_returns_existing_task_status() -> None:
    existing_id = next(iter(MOCK_TASKS.keys()))

    response = asyncio.run(get_task_status(existing_id))

    assert response["task_id"] == existing_id
    assert response["status"] == MOCK_TASKS[existing_id].status


def test_get_task_status_returns_not_found_for_missing_task() -> None:
    missing_id = 99999

    response = asyncio.run(get_task_status(missing_id))

    assert response == {"task_id": missing_id, "status": "Task not found"}
