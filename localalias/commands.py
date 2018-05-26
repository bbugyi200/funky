"""Command definitions."""

from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    """Base command class.

    Args:
        lalias (str): local alias name.
    """
    def __init__(self, lalias):
        self.lalias = lalias

    @abstractmethod
    def __call__(self):
        pass


class Add(Command):
    """Add command."""
    def __call__(self):
        pass


class Remove(Command):
    """Remove command."""
    def __call__(self):
        pass


class Edit(Command):
    """Edit command."""
    def __call__(self):
        pass


class Execute(Command):
    """Execute command."""
    def __call__(self):
        pass


class Show(Command):
    """Show command.

    Args:
        color: if True, colorize output.
    """
    def __init__(self, lalias, *, color=False):
        super().__init__(lalias)
        self.color = color

    def __call__(self):
        pass
