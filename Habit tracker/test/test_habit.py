from datetime import datetime, timedelta
from habit import Habit


def test_habit_creation():
    """
    Test the creation of a Habit instance.

    Verifies that the habit is initialized with the correct name and periodicity.
    """

    h = Habit("Exercise", "Workout", "daily")
    assert h.name == "Exercise"
    assert h.periodicity == "daily"


def test_habit_completion():
    """
    Test marking a habit as completed.

    Ensures that calling complete_task adds a timestamp to the completions list.
    """

    h = Habit("Exercise", "Workout", "daily")
    h.complete_task()
    assert len(h.completions) == 1


def test_streak_calculation():
    """
    Test current streak calculation for a daily habit.

    Simulates three consecutive daily completions and verifies the streak is at least 3.
    """

    h = Habit("Exercise", "Workout", "daily")
    today = datetime.now()
    h.complete_task(today)
    h.complete_task(today - timedelta(days=1))
    h.complete_task(today - timedelta(days=2))
    assert h.get_current_streak() >= 3


def test_longest_streak():
    """
    Test longest streak calculation for a daily habit.

    Simulates five consecutive daily completions and verifies the longest streak is 5.
    """

    h = Habit("Exercise", "Workout", "daily")
    today = datetime.now()
    for i in range(5):
        h.complete_task(today - timedelta(days=i))
    assert h.get_longest_streak() == 5
