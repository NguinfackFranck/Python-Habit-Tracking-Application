from tracker import HabitTracker


def test_add_habit():
    tracker = HabitTracker("test.db")
    tracker.db.clear_all_data()
    habit = tracker.add_habit("Test Habit", "Test", "daily")
    assert habit is not None
    assert habit.name == "Test Habit"


def test_complete_habit():
    tracker = HabitTracker("test.db")
    tracker.db.clear_all_data()
    tracker.add_habit("Test Habit", "Test", "daily")
    result = tracker.complete_habit("Test Habit")
    assert result is True


def test_delete_habit():
    """
    Test the deletion of a habit from the HabitTracker system.

    This test performs the following steps:
    1. Initializes a HabitTracker instance with a test database.
    2. Clears all existing data to ensure a clean test environment.
    3. Adds a habit named 'DeleteMe' with weekly periodicity.
    4. Deletes the habit using the delete_habit method.
    5. Asserts that the habit no longer exists in the database.

    Expected Outcome:
        The habit 'DeleteMe' should be successfully removed from both memory and persistent storage.
    """

    tracker = HabitTracker("test.db")
    tracker.db.clear_all_data()
    tracker.add_habit("DeleteMe", "Test", "weekly")
    tracker.delete_habit("DeleteMe")
    assert tracker.db.habit_exists("DeleteMe") is False
