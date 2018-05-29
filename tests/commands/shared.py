"""Shared utility functions for command tests."""
import argparse
import json

from localalias import commands


def load_aliases():
    """Loads aliases from database file"""
    with open(commands.Command.LOCALALIAS_DB_FILENAME, 'r') as f:
        loaded_aliases = json.load(f)
    return loaded_aliases


def build_args(alias):
    """Returns an argparse.Namespace where args.alias=None."""
    return argparse.Namespace(alias=alias, cmd_args=[], color=False, debug=False)
