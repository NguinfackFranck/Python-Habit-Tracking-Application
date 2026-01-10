"""
Unit tests for the Habit class.

These tests validate:
- Habit creation and validation
- Task completion tracking
- Current streak calculation
- Longest streak calculation
- Handling of broken habits

This file ensures the correctness of the core habit tracking logic.
"""

import pytest
from datetime import datetime, timedelta
from habit import Habit


def test_create_daily_habit():
    """
    Test creating a valid daily habit.

    Verifies that:
    - The habit is created successfully
    - Attributes are set correctly
    - No completions exist initially
    """
    habit = Habit(
        name="Exercise",
        task_specification="30 minutes cardio",
        periodicity="daily"
    )

    assert habit.name == "Exercise"
    assert habit.periodicity == "daily"
    assert habit.get_completion_count() == 0


def test_invalid_periodicity():
    """
    Test that creating a habit with an invalid periodicity raises an error.
    """
    with pytest.raises(ValueError):
        Habit("Invalid Habit", "Test task", "monthly")


def test_complete_habit_once():
    """
    Test completing a habit once.

    Verifies that:
    - Completion count increases correctly
    """
    habit = Habit("Read", "Read 10 pages", "daily")
    habit.complete_task()

    assert habit.get_completion_count() == 1


def test_current_streak_daily():
    """
    Test current streak calculation for a daily habit.

    Creates a 3-day streak and verifies the streak count.
    """
    habit = Habit("Exercise", "Workout", "daily")

    for i in range(3):
        habit.complete_task(datetime.now() - timedelta(days=i))

    assert habit.get_current_streak() == 3


def test_habit_breaks_streak():
    """
    Test that a streak is broken if the habit is missed.

    A completion outside the valid period should result in a streak of 0.
    """
    habit = Habit("Meditate", "10 minutes", "daily")
    habit.complete_task(datetime.now() - timedelta(days=3))

    assert habit.get_current_streak() == 0


def test_longest_streak():
    """
    Test longest streak calculation.

    Creates two streaks and verifies that the longest one is returned.
    """
    habit = Habit("Study", "Python practice", "daily")

    # First streak (2 days)
    habit.complete_task(datetime.now() - timedelta(days=6))
    habit.complete_task(datetime.now() - timedelta(days=5))

    # Second streak (3 days)
    habit.complete_task(datetime.now() - timedelta(days=2))
    habit.complete_task(datetime.now() - timedelta(days=1))
    habit.complete_task(datetime.now())

    assert habit.get_longest_streak() == 3
