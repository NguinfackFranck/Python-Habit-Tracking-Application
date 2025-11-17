"""
Habit Class Module for Habit Tracker Application
"""

from datetime import datetime
from typing import List, Optional, Dict, Any


class Habit:
    """
    Represents a single habit tracked by the user.

    Attributes:
        id (Optional[int]): Unique identifier for the habit.
        name (str): Name of the habit.
        task_specification (str): Description of the task to be performed.
        periodicity (str): Frequency of the habit, either 'daily' or 'weekly'.
        created_date (datetime): Timestamp when the habit was created.
        completions (List[datetime]): List of timestamps when the habit was completed.
    """

    def __init__(self, name: str, task_specification: str, periodicity: str,
                 created_date: Optional[datetime] = None,
                 completions: Optional[List[datetime]] = None,
                 habit_id: Optional[int] = None):
        """
        Initializes a Habit instance.

        Args:
            name (str): Name of the habit.
            task_specification (str): Description of the task.
            periodicity (str): 'daily' or 'weekly'.
            created_date (Optional[datetime]): Creation date of the habit.
            completions (Optional[List[datetime]]): List of completion dates.
            habit_id (Optional[int]): Unique identifier for the habit.

        Raises:
            ValueError: If periodicity is not 'daily' or 'weekly'.
        """
        if periodicity not in ["daily", "weekly"]:
            raise ValueError("Periodicity must be either 'daily' or 'weekly'")

        self.id = habit_id
        self.name = name
        self.task_specification = task_specification
        self.periodicity = periodicity
        self.created_date = created_date or datetime.now()
        self.completions = completions or []

    def complete_task(self, completion_date: Optional[datetime] = None):
        """
        Marks the habit as completed on the given date.

        Args:
            completion_date (Optional[datetime]): Date of completion. Defaults to now.
        """

        completion_date = completion_date or datetime.now()
        self.completions.append(completion_date)
        self.completions.sort()

    def get_current_streak(self) -> int:
        """
        Calculates the current streak of consecutive completions.

        Returns:
            int: Number of consecutive successful periods up to today.
        """

        if not self.completions:
            return 0

        period_days = 1 if self.periodicity == "daily" else 7
        streak = 0
        sorted_dates = sorted(self.completions, reverse=True)
        today = datetime.now().date()

        # Start checking from most recent
        for completion in sorted_dates:
            days_diff = (today - completion.date()).days
            if days_diff <= period_days * streak:
                streak += 1
            else:
                break
        return streak

    def get_longest_streak(self) -> int:
        """
        Finds the longest streak of consecutive completions.

        Returns:
            int: Maximum number of consecutive successful periods ever achieved.
        """

        if not self.completions:
            return 0

        period_days = 1 if self.periodicity == "daily" else 7
        sorted_dates = sorted(self.completions)
        max_streak, streak = 1, 1

        for i in range(1, len(sorted_dates)):
            diff = (sorted_dates[i] - sorted_dates[i - 1]).days
            if diff <= period_days:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        return max_streak

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Habit':
        """Create Habit from DB dictionary."""
        created = data.get('created_date')
        if isinstance(created, str):
            created = datetime.fromisoformat(created)
        completions = [
            datetime.fromisoformat(c) if isinstance(c, str) else c
            for c in data.get('completions', [])
        ]
        return cls(
            name=data['name'],
            task_specification=data['task_specification'],
            periodicity=data['periodicity'],
            created_date=created,
            completions=completions,
            habit_id=data.get('id')
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Habit to dictionary (for storage or JSON)."""
        return {
            'id': self.id,
            'name': self.name,
            'task_specification': self.task_specification,
            'periodicity': self.periodicity,
            'created_date': self.created_date.isoformat(),
            'completions': [c.isoformat() for c in self.completions]
        }

    def __str__(self):
        return f"{self.name} ({self.periodicity}) - {len(self.completions)} completions"
