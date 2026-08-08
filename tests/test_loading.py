from utils.loading import (
    show_loading,
    create_progress,
    run_progress,
)


def sample_function():
    """Simple function used for testing."""
    return "completed"


def test_show_loading():
    """Test loading wrapper."""

    result = show_loading(
        "Processing...",
        sample_function,
    )

    assert result == "completed"


def test_create_progress():
    """Test progress creation."""

    progress = create_progress()

    assert progress is not None


def test_run_progress():
    """Test progress creation and task registration."""

    progress = run_progress(
        "Testing...",
        10,
    )

    assert progress is not None
    assert len(progress.task_ids) == 1

    progress.stop()