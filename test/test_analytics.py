"""
Unit tests for the analytics module.

These tests ensure:
- Analytics functions work correctly
- Functional programming principles are followed
- Streak calculations respect habit periodicity
"""

from datetime import datetime, timedelta
from habit import Habit
from analytics import (
    get_all_habits,
    filter_by_periodicity,
    calculate_longest_streak_all,
    calculate_longest_streak_for_habit
)


def create_test_habits():
    """
    Create a list of test habits with predefined completion data.

    Includes:
    - One daily habit with a 4-day streak
    - One weekly habit with a 2-week streak
    """
    daily = Habit("Daily Habit", "Task", "daily")
    weekly = Habit("Weekly Habit", "Task", "weekly")

    # Daily habit: 4 consecutive days
    for i in range(4):
        daily.complete_task(datetime.now() - timedelta(days=i))

    # Weekly habit: 2 consecutive weeks
    for i in range(2):
        weekly.complete_task(datetime.now() - timedelta(weeks=i))

    return [daily, weekly]


def test_get_all_habits():
    """
    Test returning all habits.
    """
    habits = create_test_habits()
    assert len(get_all_habits(habits)) == 2


def test_filter_by_periodicity():
    """
    Test filtering habits by periodicity.
    """
    habits = create_test_habits()
    daily_habits = filter_by_periodicity(habits, "daily")

    assert len(daily_habits) == 1
    assert daily_habits[0].periodicity == "daily"


def test_longest_streak_all():
    """
    Test finding the longest streak across all habits.

    The analytics function returns the Habit object with the
    longest streak. The streak value is then extracted using
    calculate_longest_streak_for_habit().
    """
    habits = create_test_habits()

    # Function returns the Habit with the longest streak
    habit_with_longest = calculate_longest_streak_all(habits)

    # Extract the streak value using the single-habit analytics function
    longest_streak = calculate_longest_streak_for_habit(habit_with_longest)

    assert longest_streak == 4


def test_longest_streak_for_specific_habit():
    """
    Test finding the longest streak for a specific habit.
    """
    habits = create_test_habits()
    daily_habit = habits[0]

    assert calculate_longest_streak_for_habit(daily_habit) == 4
