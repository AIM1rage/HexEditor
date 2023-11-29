import abc
from copy import deepcopy


class Command(abc.ABC):
    def __init__(self, hex_editor):
        self.hex_editor = hex_editor
        self.old_length = self.hex_editor.file.length
        self.cursors = deepcopy(self.hex_editor.cursors)
        self.row_offset = hex_editor.row_offset
        self.context = self.hex_editor.context

    @abc.abstractmethod
    def do(self):
        ...

    @abc.abstractmethod
    def undo(self):
        ...

    def restore_editor_state(self):
        self.hex_editor.cursors = deepcopy(self.cursors)
        self.hex_editor.row_offset = self.row_offset
        self.hex_editor.context = self.context

    def restore_file_length(self):
        self.hex_editor.file.truncate(self.old_length)
