"""Command definitions."""

from abc import ABCMeta, abstractmethod

from localalias.utils import log


class Command(metaclass=ABCMeta):
    """Base command class.

    Args:
        lalias (str): local alias name.
        color (bool): if True, colorize output.
    """
    def __init__(self, lalias, *, color):
        self.lalias = lalias
        self.color = color

    @abstractmethod
    def __call__(self):
        log.logger.debug('Running {} command...'.format(self.__class__.__name__))


class Add(Command):
    def __call__(self):
        super().__call__()


class Remove(Command):
    def __call__(self):
        super().__call__()


class Edit(Command):
    def __call__(self):
        super().__call__()


class Execute(Command):
    def __call__(self):
        super().__call__()


class Show(Command):
    def __call__(self):
        super().__call__()
