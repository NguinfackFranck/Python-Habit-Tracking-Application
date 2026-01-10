"""
HabitTracker Module for Habit Tracker Application

This module provides the HabitTracker class which manages multiple habits
and coordinates between the Habit objects and the database.
"""
from datetime import datetime
from typing import List, Optional
from analytics import (

    calculate_longest_streak_all,
    get_most_struggled_habits,
    summarize_habits,
)

from habit import Habit
from database import DatabaseManager


class HabitTracker:
    """
    Central manager for all habit operations.

    Attributes:
        db (DatabaseManager): Interface to the underlying database.
        habits (List[Habit]): In-memory list of all loaded Habit instances.
    """

    def __init__(self, db_name: str = "habits.db"):
        """
        Initialize the HabitTracker with a database connection and load habits.

        Args:
            db_name (str): Name of the SQLite database file.
        """

        self.db = DatabaseManager(db_name)
        self.habits: List[Habit] = []
        self.load_habits_from_db()

    def load_habits_from_db(self):
        """Load all habits from database into memory."""
        habit_dicts = self.db.load_all_habits()
        self.habits = [Habit.from_dict(h) for h in habit_dicts]

    def add_habit(self, name: str, task_specification: str, periodicity: str) -> Optional[Habit]:
        """
        Create and save a new habit.

        Args:
            name (str): Name of the habit.
            task_specification (str): Description of the task to perform.
            periodicity (str): Frequency of the habit ('daily' or 'weekly').

        Returns:
            Optional[Habit]: The created Habit object, or None if creation failed.
        """

        if self.db.habit_exists(name):
            print(f"Habit '{name}' already exists.")
            return None

        habit = Habit(name, task_specification, periodicity)
        habit_id = self.db.save_habit(
            name, task_specification, periodicity, habit.created_date)

        if habit_id:
            habit.id = habit_id
            self.habits.append(habit)
            print(f"Habit '{name}' added successfully.")
            return habit
        else:
            print(f"Error saving habit '{name}' to database.")
            return None

    def complete_habit(self, name: str, completion_date: Optional[datetime] = None):
        """
        Mark a habit as completed on a given date.

        Args:
            name (str): Name of the habit to complete.
            completion_date (Optional[datetime]): Date of completion. Defaults to now.

        Returns:
            bool: True if the habit was found and marked complete, False otherwise.
        """

        habit = next((h for h in self.habits if h.name == name), None)
        if not habit:
            print(f"Habit '{name}' not found.")
            return False

        completion_date = completion_date or datetime.now()
        habit.complete_task(completion_date)

        self.db.save_completion(habit.id, completion_date)
        print(
            f"Habit '{name}' marked as complete on {completion_date.date()}.")
        return True

    def delete_habit(self, name: str) -> bool:
        """
        Delete a habit from memory and the database.

        Args:
            name (str): Name of the habit to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """

        # First, find the habit object in the local list
        habit_obj = next((h for h in self.habits if h.name == name), None)

        if not habit_obj:
            print(f"Habit '{name}' not found in memory.")
            return False

        # Next, attempt to delete it from the database
        success = self.db.delete_habit(name)

        if success:
            # If DB deletion worked, remove the specific object from the local list
            self.habits.remove(habit_obj)
            print(f"Habit '{name}' deleted.")
            return True
        else:
            print(f"Error: Could not delete habit '{name}' from the database.")
            return False

    def list_habits(self, periodicity: Optional[str] = None):
        """
        List all habits, optionally filtered by periodicity.

        Args:
            periodicity (Optional[str]): 'daily' or 'weekly' to filter habits.
        """

        filtered = self.habits
        if periodicity:
            filtered = [h for h in self.habits if h.periodicity == periodicity]

        if not filtered:
            print("No habits found.")
            return

        for habit in filtered:
            print(
                f"- {habit.name} ({habit.periodicity}) | Streak: {habit.get_current_streak()} days")

    def analyze_longest_streaks(self):
        """
        Display a summary of habit analytics, including:
        - Current and longest streaks for each habit
        - The habit with the longest overall streak
        - The top 3 most struggled habits
        """

        if not self.habits:
            print("No habits to analyze.")
            return

        # The following code has been indented to be part of the method scope
        print("\n📊 Habit Analysis Summary\n" + "-" * 35)

        # Assuming summarize_habits is a defined function/method
        summary = summarize_habits(self.habits)
        for s in summary:
            print(f"{s['name']} ({s['periodicity']}) → "
                  f"Current: {s['current_streak']}, Longest: {s['longest_streak']}")

        print("\n🏆 Longest Streak Overall:")

        # Assuming calculate_longest_streak_all is a defined function/method
        top_habit = calculate_longest_streak_all(self.habits)
        if top_habit:
            print(
                f"  {top_habit.name} with {top_habit.get_longest_streak()} streaks!")

        print("\n⚠️ Habits You Struggle With Most:")

        # Assuming get_most_struggled_habits is a defined function/method
        struggles = get_most_struggled_habits(self.habits)[:3]
        for h in struggles:
            print(f"  {h.name} — {h.get_current_streak()} current streaks, "
                  f"{len(h.completions)} completions")
        print("-" * 35)
