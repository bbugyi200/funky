"""Shared utility functions for command tests."""
import json

from funky import commands


def load_funks():
    """Loads funks from database file"""
    with open(commands.Command.FUNKY_DB_FILENAME, 'r') as f:
        loaded_funks = json.load(f)
    return loaded_funks
