import abc


class Command(abc.ABC):
    def __init__(self, hex_editor):
        self.hex_editor = hex_editor

    @abc.abstractmethod
    def do(self):
        ...

    @abc.abstractmethod
    def undo(self):
        ...
