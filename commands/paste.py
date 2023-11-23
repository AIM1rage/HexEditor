from commands.command import Command
from editor.hex_file import HexFile


class PasteCommand(Command):
    old_hex_chars: bytes

    def __init__(self, file: HexFile, new_chars: bytes, position: int):
        super().__init__(file)
        self.new_chars: bytes = new_chars
        self.position: int = position

    def undo(self):
        self.hex_editor.write(self.old_hex_chars, self.position)

    def do(self):
        self.old_hex_chars = self.hex_editor.read_chunk(self.position, len(self.new_chars))

        self.hex_editor.write(self.new_chars, self.position)
