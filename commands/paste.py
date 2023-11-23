from commands.command import Command
from editor.editor import HexEditor


class PasteCommand(Command):
    old_hex_chars: bytes
    position: int

    def __init__(self, hex_editor: HexEditor, new_chars: bytes):
        super().__init__(hex_editor)
        self.new_chars: bytes = new_chars

    def undo(self):
        self.hex_editor.file.write(self.old_hex_chars, self.position)

    def do(self):
        self.position = self.hex_editor.pointer
        self.old_hex_chars = self.hex_editor.file.read_chunk(self.position, len(self.new_chars))

        self.hex_editor.file.write(self.new_chars, self.position)
