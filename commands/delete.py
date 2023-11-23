from commands.command import Command
from editor.editor import HexEditor


class DeleteCommand(Command):
    deleted_hex_char: bytes
    position: int

    def __init__(self, hex_editor: HexEditor):
        super().__init__(hex_editor)

    def undo(self):
        self.hex_editor.file.insert(self.deleted_hex_char, self.position)

    def do(self):
        self.position = self.hex_editor.pointer
        self.deleted_hex_char = (self
                                 .hex_editor
                                 .file
                                 .read_hex_char(self.position)
                                 )
        self.hex_editor.file.delete(self.position)
