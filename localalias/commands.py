"""Command definitions."""

from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    """Base command class.

    Args:
        lalias (str): local alias name.
        color: if True, colorize output.
    """
    def __init__(self, lalias, *, color):
        self.lalias = lalias
        self.color = color

    @abstractmethod
    def __call__(self):
        pass


class Add(Command):
    def __call__(self):
        pass


class Remove(Command):
    def __call__(self):
        pass


class Edit(Command):
    def __call__(self):
        pass


class Execute(Command):
    def __call__(self):
        pass


class Show(Command):
    def __call__(self):
        pass
