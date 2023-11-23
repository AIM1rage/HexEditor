from commands.command import Command
from editor.editor import HexEditor


class WriteCommand(Command):
    old_hex_char: bytes
    position: int

    def __init__(self, hex_editor: HexEditor, new_char: bytes):
        super().__init__(hex_editor)
        self.new_char: bytes = new_char

    def undo(self):
        self.hex_editor.file.write(self.old_hex_char, self.position)

    def do(self):
        self.position = self.hex_editor.pointer
        self.old_hex_char = self.hex_editor.file.read_hex_char(self.position)
        self.hex_editor.file.write(self.new_char, self.position)
