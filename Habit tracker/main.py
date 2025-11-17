"""
Command-Line Interface for Habit Tracker Application

This module provides a CLI for managing habits using the HabitTracker class.
Users can create, complete, list, analyze, and delete habits via terminal commands.
"""


import click
from tracker import HabitTracker


@click.group()
@click.pass_context
def cli(ctx):
    """
    Entry point for the Habit Tracker CLI.

    Initializes a HabitTracker instance and passes it to subcommands via context.
    """

    ctx.obj = HabitTracker()


@cli.command()
@click.argument("name")
@click.argument("task")
@click.argument("periodicity")
@click.pass_obj
def create(tracker, name, task, periodicity):
    """
    Create a new habit.

    Arguments:
        name (str): Name of the habit.
        task (str): Description of the task to be performed.
        periodicity (str): Frequency of the habit ('daily' or 'weekly').
    """

    tracker.add_habit(name, task, periodicity)


@cli.command()
@click.argument("name")
@click.pass_obj
def complete(tracker, name):
    """
    Mark a habit as completed.

    Arguments:
        name (str): Name of the habit to mark as completed.
    """

    tracker.complete_habit(name)


@cli.command()
@click.option("--periodicity", type=click.Choice(["daily", "weekly"]), required=False)
@click.pass_obj
def list(tracker, periodicity):
    """
    List all habits.

    Optionally filter by periodicity ('daily' or 'weekly').
    """

    tracker.list_habits(periodicity)


@cli.command()
@click.pass_obj
def analyze(tracker):
    """
    Analyze longest streaks for all habits.

    Displays the longest streak achieved for each habit.
    """

    tracker.analyze_longest_streaks()


@cli.command()
@click.argument("name")
@click.pass_obj
def delete(tracker, name):
    """
    Delete a habit.

    Arguments:
        name (str): Name of the habit to delete.
    """

    tracker.delete_habit(name)


if __name__ == "__main__":
    cli()
