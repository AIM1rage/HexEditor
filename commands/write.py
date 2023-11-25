import binascii
from commands.command import Command
from editor.editor import HexEditor, EditMode




class WriteCommand(Command):
    def __init__(self, hex_editor: HexEditor, new_hex_char: str):
        super().__init__(hex_editor)
        self.new_hex_char: str = new_hex_char
        self.old_hex_char: bytes = self.hex_editor.file.read_hex_char(self.pointer)

    def undo(self):
        self.hex_editor.file.write(self.old_hex_char, self.pointer)
        self.hex_editor.file.truncate(self.old_length)
        self.hex_editor.set_cursor(self.position)

    def do(self):

        self.hex_editor.set_cursor(self.position)
        unhex_old_char = binascii.hexlify(self.old_hex_char).decode()
        unhex_old_char = unhex_old_char if unhex_old_char else '00'
        if self.context == EditMode.HEX:
            if self.position.cell_index == 0:
                new_hex_cell = binascii.unhexlify(self.new_hex_char +
                                                unhex_old_char[1]
                                                )
            else:
                new_hex_cell = binascii.unhexlify(unhex_old_char[0] +
                                                self.new_hex_char
                                                )
        else:
            new_hex_cell = self.new_hex_char.encode()


        self.hex_editor.file.write(new_hex_cell, self.pointer)
        self.hex_editor.move_cursor_right()
