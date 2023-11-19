from commands.command import Command
from hex_file import HexFile


class WriteCommand(Command):
    old_char: bytes

    def __init__(self, file: HexFile, new_char: bytes, position: int):
        super().__init__(file)
        self.new_char: bytes = new_char
        self.position: int = position

    def undo(self):
        self.file.write(self.old_char, self.position)

    def do(self):
        self.old_char = self.file.read_char(self.position)
        self.file.write(self.new_char, self.position)