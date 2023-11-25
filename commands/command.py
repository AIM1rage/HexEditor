import abc
from collections import namedtuple

CursorPosition = namedtuple('CursorPosition', [
    'row_index',
    'column_index',
    'cell_index',
    'row_offset',
],
                            )


class Command(abc.ABC):
    def __init__(self, hex_editor):
        self.hex_editor = hex_editor
        self.pointer = self.hex_editor.pointer
        self.old_length = self.hex_editor.file.length
        self.position = CursorPosition(self.hex_editor.row_index,
                                       self.hex_editor.column_index,
                                       self.hex_editor.cell_index,
                                       self.hex_editor.row_offset,
                                    )
        self.context = self.hex_editor.context

    @abc.abstractmethod
    def do(self):
        ...

    @abc.abstractmethod
    def undo(self):
        ...
