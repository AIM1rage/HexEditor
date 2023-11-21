import abc
from editor.hex_file import HexFile


class Command(abc.ABC):
    def __init__(self, file: HexFile):
        self.file: HexFile = file

    @abc.abstractmethod
    def do(self):
        ...

    @abc.abstractmethod
    def undo(self):
        ...
