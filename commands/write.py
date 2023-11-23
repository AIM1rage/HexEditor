import binascii
from commands.command import Command
from editor.editor import HexEditor


class WriteCommand(Command):
    old_hex_char: bytes
    position: int
    cell_index: int

    def __init__(self, hex_editor: HexEditor, new_hex_char: str):
        super().__init__(hex_editor)
        self.new_hex_char: str = new_hex_char

    def undo(self):
        self.hex_editor.file.write(self.old_hex_char, self.position)

    def do(self):
        self.position = self.hex_editor.pointer
        self.cell_index = self.hex_editor.cell_index
        self.old_hex_char = self.hex_editor.file.read_hex_char(self.position)

        unhex_old_char = binascii.hexlify(self.old_hex_char).decode()
        if self.cell_index == 0:
            new_hex_cell = binascii.unhexlify(self.new_hex_char + unhex_old_char[1])
        else:
            new_hex_cell = binascii.unhexlify(unhex_old_char[0] + self.new_hex_char)
        self.hex_editor.file.write(new_hex_cell, self.position)
