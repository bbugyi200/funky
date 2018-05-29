"""Shared utility functions for command tests."""
import json

from localalias import commands


def load_aliases():
    """Loads aliases from database file"""
    with open(commands.Command.LOCALALIAS_DB_FILENAME, 'r') as f:
        loaded_aliases = json.load(f)
    return loaded_aliases
