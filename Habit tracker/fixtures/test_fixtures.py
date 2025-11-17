"""
Predefined Habit Fixture Data for Testing

This module provides a utility function to generate a list of Habit instances
with simulated completion data over the past 4 weeks. It is intended for use
in testing habit tracking features such as streak analysis, filtering, and reporting.
"""


from datetime import datetime, timedelta
from habit import Habit


def generate_test_habits():
    """
    Generate a list of predefined Habit objects with simulated completion history.

    Creates five sample habits (three daily, two weekly), each initialized with a
    creation date 28 days ago. Completion data is added to simulate realistic usage:
    - Daily habits are marked complete every day for the past 28 days.
    - Weekly habits are marked complete every 7 days (i.e., 4 completions total).

    Returns:
        List[Habit]: A list of Habit instances with populated completion data.
    """

    today = datetime.now()

    habits = [
        Habit("Morning Exercise", "30 minutes workout", "daily",
              created_date=today - timedelta(days=28)),
        Habit("Read Book", "Read 20 pages", "daily",
              created_date=today - timedelta(days=28)),
        Habit("Grocery Shopping", "Weekly groceries", "weekly",
              created_date=today - timedelta(days=28)),
        Habit("Deep Clean House", "Full cleaning session", "weekly",
              created_date=today - timedelta(days=28)),
        Habit("Meditation", "10 minutes meditation", "daily",
              created_date=today - timedelta(days=28)),
    ]

    # Simulate completions over the past 4 weeks

    for habit in habits:
        for i in range(28):  # 4 weeks
            if habit.periodicity == "daily":
                habit.complete_task(today - timedelta(days=i))
            else:
                if i % 7 == 0:  # weekly completions
                    habit.complete_task(today - timedelta(days=i))

    return habits
