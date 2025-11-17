"""
Analytics Module for Habit Tracker Application

Implements functional-style analysis functions for habits.
These functions operate purely on data and do not mutate state.
"""

from typing import List, Optional
from habit import Habit


# 1. Return a list of all currently tracked habits

def get_all_habits(habits: List[Habit]) -> List[str]:
    """
    Return names of all tracked habits.

    Args:
        habits (List[Habit]): List of Habit objects

    Returns:
        List[str]: Names of all habits
    """
    return [habit.name for habit in habits]


# 2. Return a list of all habits with the same periodicity

def filter_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Filter habits by periodicity.

    Args:
        habits (List[Habit]): List of Habit objects
        periodicity (str): 'daily' or 'weekly'

    Returns:
        List[Habit]: Filtered list
    """
    return list(filter(lambda h: h.periodicity == periodicity, habits))


# 3. Return the longest run streak of all defined habits

def calculate_longest_streak_all(habits: List[Habit]) -> Optional[Habit]:
    """
    Find the habit with the overall longest streak.

    Args:
        habits (List[Habit]): List of Habit objects

    Returns:
        Optional[Habit]: Habit with the longest streak, or None if no habits
    """
    if not habits:
        return None
    return max(habits, key=lambda h: h.get_longest_streak())


# 4. Return the longest run streak for a given habit

def calculate_longest_streak_for_habit(habit: Habit) -> int:
    """
    Return longest streak for a single habit.

    Args:
        habit (Habit): The habit to analyze

    Returns:
        int: Longest streak count
    """
    return habit.get_longest_streak()


# 5. Identify habits with the most breaks (missed periods)

def get_most_struggled_habits(habits: List[Habit]) -> List[Habit]:
    """
    Identify habits with the lowest streaks or fewest completions.

    Args:
        habits (List[Habit]): List of Habit objects

    Returns:
        List[Habit]: Habits considered most difficult for user
    """
    if not habits:
        return []

    # Sort by ascending streak (lowest first)
    return sorted(habits, key=lambda h: (h.get_current_streak(), len(h.completions)))


# 6. Summary report for all habits

def summarize_habits(habits: List[Habit]) -> List[dict]:
    """
    Create a summary list for all habits (pure data transformation).

    Args:
        habits (List[Habit]): List of Habit objects

    Returns:
        List[dict]: Each dictionary includes habit name, periodicity, and streaks
    """
    return [
        {
            "name": h.name,
            "periodicity": h.periodicity,
            "current_streak": h.get_current_streak(),
            "longest_streak": h.get_longest_streak(),
            "completions": len(h.completions),
        }
        for h in habits
    ]
