# Python-Habit-Tracking-Application
OVERVIEW
This project is a Habit Tracking Application built for IU’s OOFPP course.
It allows users to:

Create daily or weekly habits

Mark tasks as completed

Track streaks and breaks

Analyze habit performance

Store data persistently using SQLite

Interact through a clean CLI interface

The app is designed using:

Object-Oriented Programming (Habit, HabitTracker)

Functional Programming (Analytics module)

SQLite database persistence

Pytest test suite

Click CLI interface

FEATURES
✔ Habit Management

Create new habits

Delete habits

View all habits

Filter by periodicity (daily/weekly)

✔ Tracking

Mark habit as completed

Track number of completions

Identify breaks (missed periods)

✔ Analytics (Functional Programming)

List all habits

List habits by periodicity

Find longest streak overall

Find longest streak for a specific habit

✔ Persistence

Automatic saving/loading using SQLite

Separate tables for habits and completions

✔ Predefined Test Habits

The project includes 5 predefined habits with 4 weeks of data, used as fixtures for testing.
