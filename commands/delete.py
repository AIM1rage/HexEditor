from commands.command import Command
from editor.hex_file import HexFile


class DeleteCommand(Command):
    deleted_hex_char: bytes

    def __init__(self, file: HexFile, position: int):
        super().__init__(file)
        self.position: int = position

    def undo(self):
        self.file.insert(self.deleted_hex_char, self.position)

    def do(self):
        self.deleted_hex_char = self.file.read_hex_char(self.position)
        self.file.delete(self.position)
