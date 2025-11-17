"""
Database Manager Module for Habit Tracker Application

This module handles all database operations for storing and retrieving habits
and their completion records using SQLite.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional


class DatabaseManager:
    """
    Manages all database operations for the habit tracker.

    This class provides methods to create tables, save habits, load habits,
    and manage completion records in an SQLite database.
    """

    def __init__(self, db_name: str = "habits.db"):
        """
        Initialize the database manager.

        Args:
            db_name (str): Name of the SQLite database file. Defaults to "habits.db"
        """
        self.db_name = db_name
        self.create_tables()

    def get_connection(self) -> sqlite3.Connection:
        """
        Create and return a database connection.

        Returns:
            sqlite3.Connection: Database connection object
        """
        conn = sqlite3.connect(self.db_name)
        # This makes rows accessible by column name
        conn.row_factory = sqlite3.Row
        return conn

    def create_tables(self):
        """
        Create the necessary database tables if they don't exist.

        Creates two tables:
        - habits: Stores habit information
        - completions: Stores completion timestamps for each habit
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create habits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                task_specification TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        ''')

        # Create completions table with foreign key to habits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def save_habit(self, name: str, task_specification: str,
                   periodicity: str, created_date: datetime) -> Optional[int]:
        """
        Save a new habit to the database.

        Args:
            name (str): Name of the habit
            task_specification (str): Description of what needs to be done
            periodicity (str): Either "daily" or "weekly"
            created_date (datetime): When the habit was created

        Returns:
            Optional[int]: The ID of the inserted habit, or None if insertion failed
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO habits (name, task_specification, periodicity, created_date)
                VALUES (?, ?, ?, ?)
            ''', (name, task_specification, periodicity, created_date.isoformat()))

            habit_id = cursor.lastrowid
            conn.commit()
            return habit_id
        except sqlite3.IntegrityError as e:
            # Habit with this name already exists
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    def save_completion(self, habit_id: int, completion_date: datetime) -> bool:
        """
        Save a habit completion record.

        Args:
            habit_id (int): The ID of the habit being completed
            completion_date (datetime): When the habit was completed

        Returns:
            bool: True if successful, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO completions (habit_id, completion_date)
                VALUES (?, ?)
            ''', (habit_id, completion_date.isoformat()))

            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error saving completion: {e}")
            return False
        finally:
            conn.close()

    def load_all_habits(self) -> List[dict]:
        """
        Load all habits from the database with their completions.

        Returns:
            List[dict]: List of habit dictionaries, each containing:
                - id: Habit ID
                - name: Habit name
                - task_specification: What needs to be done
                - periodicity: "daily" or "weekly"
                - created_date: When habit was created
                - completions: List of completion datetime objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Get all habits
        cursor.execute('SELECT * FROM habits')
        habits_rows = cursor.fetchall()

        habits_list = []
        for habit_row in habits_rows:
            habit_dict = {
                'id': habit_row['id'],
                'name': habit_row['name'],
                'task_specification': habit_row['task_specification'],
                'periodicity': habit_row['periodicity'],
                'created_date': datetime.fromisoformat(habit_row['created_date']),
                'completions': []
            }

            # Get all completions for this habit
            cursor.execute('''
                SELECT completion_date FROM completions 
                WHERE habit_id = ? 
                ORDER BY completion_date
            ''', (habit_row['id'],))

            completion_rows = cursor.fetchall()
            habit_dict['completions'] = [
                datetime.fromisoformat(row['completion_date'])
                for row in completion_rows
            ]

            habits_list.append(habit_dict)

        conn.close()
        return habits_list

    def get_habit_by_name(self, name: str) -> Optional[dict]:
        """
        Load a specific habit by name.

        Args:
            name (str): Name of the habit to retrieve

        Returns:
            Optional[dict]: Habit dictionary with completions, or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM habits WHERE name = ?', (name,))
        habit_row = cursor.fetchone()

        if not habit_row:
            conn.close()
            return None

        habit_dict = {
            'id': habit_row['id'],
            'name': habit_row['name'],
            'task_specification': habit_row['task_specification'],
            'periodicity': habit_row['periodicity'],
            'created_date': datetime.fromisoformat(habit_row['created_date']),
            'completions': []
        }

        # Get completions
        cursor.execute('''
            SELECT completion_date FROM completions 
            WHERE habit_id = ? 
            ORDER BY completion_date
        ''', (habit_row['id'],))

        completion_rows = cursor.fetchall()
        habit_dict['completions'] = [
            datetime.fromisoformat(row['completion_date'])
            for row in completion_rows
        ]

        conn.close()
        return habit_dict

    def delete_habit(self, name: str) -> bool:
        """
        Delete a habit and all its completions from the database.

        Args:
            name (str): Name of the habit to delete

        Returns:
            bool: True if habit was deleted, False if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM habits WHERE name = ?', (name,))
            deleted_rows = cursor.rowcount
            conn.commit()
            return deleted_rows > 0
        except sqlite3.Error as e:
            print(f"Error deleting habit: {e}")
            return False
        finally:
            conn.close()

    def habit_exists(self, name: str) -> bool:
        """
        Check if a habit with the given name exists.

        Args:
            name (str): Name of the habit to check

        Returns:
            bool: True if habit exists, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT COUNT(*) as count FROM habits WHERE name = ?', (name,))
        result = cursor.fetchone()

        conn.close()
        return result['count'] > 0

    def clear_all_data(self):
        """
        Delete all data from the database. USE WITH CAUTION!

        This is useful for testing purposes.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM completions')
        cursor.execute('DELETE FROM habits')

        conn.commit()
        conn.close()
