"""Populate module for populating the database with habits, and habit completions"""
from fixtures.test_fixtures import generate_test_habits
from tracker import HabitTracker


def populate():
    """
    Populate the habit tracker database with predefined test habits.

    This function performs the following steps:
    1. Initializes a HabitTracker instance using 'habits.db'.
    2. Clears all existing data from the database to ensure a clean state.
    3. Loads predefined Habit instances using the generate_test_habits() fixture.
    4. Saves each habit to the database and assigns its generated ID.
    5. Saves all associated completion dates for each habit.

    This setup is useful for testing and development purposes, providing a consistent
    dataset for evaluating habit tracking features such as streaks, filtering, and analytics.
    """

    tracker = HabitTracker("habits.db")

    # Clear existing data
    tracker.db.clear_all_data()

    # Load predefined habits
    habits = generate_test_habits()

    for habit in habits:
        # Save habit to DB
        habit_id = tracker.db.save_habit(
            habit.name,
            habit.task_specification,
            habit.periodicity,
            habit.created_date
        )
        habit.id = habit_id  # *** Assign ID to habit object ***

        # Save completions
        for date in habit.completions:
            tracker.db.save_completion(habit_id, date)

    print("Test habits successfully populated into database.")


if __name__ == "__main__":
    populate()
