from habit import Habit
from analytics import *


def test_filter_by_periodicity():
    """
    Test filtering habits by periodicity.

    Creates two habits: one daily and one weekly.
    Applies the filter_by_periodicity function to extract only daily habits.

    Asserts:
        - The filtered list contains exactly one habit.
    """

    habits = [
        Habit("A", "task", "daily"),
        Habit("B", "task", "weekly")
    ]
    daily = filter_by_periodicity(habits, "daily")
    assert len(daily) == 1


def test_longest_streak_all():
    """
    Test identifying the habit with the longest streak.

    Creates two daily habits with empty completion lists.
    Marks one habit (h1) as completed once.
    Uses calculate_longest_streak_all to find the habit with the longest streak.

    Asserts:
        - The returned habit is h1, which has the longest streak.
    """

    h1 = Habit("A", "task", "daily")
    h2 = Habit("B", "task", "daily")
    h2.completions = h1.completions = []
    h1.complete_task()
    assert calculate_longest_streak_all([h1, h2]) == h1
