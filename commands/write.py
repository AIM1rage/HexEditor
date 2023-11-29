import binascii
from commands.command import Command
from editor.editor import HexEditor
from editor.cursor import EditMode


class WriteCommand(Command):
    def __init__(self, hex_editor: HexEditor, new_hex_char: str):
        super().__init__(hex_editor)
        self.new_hex_char: str = new_hex_char
        self.old_hex_chars: list[bytes] = [
            self.hex_editor.file.read_hex_char(c.pointer) for c in
            self.cursors]

    def undo(self):
        self.restore_editor_state()

        for cursor, old_hex_char in zip(self.hex_editor.cursors,
                                        self.old_hex_chars):
            self.hex_editor.file.write(old_hex_char, cursor.pointer)

        self.restore_file_length()

    def do(self):
        self.restore_editor_state()

        for cursor, old_hex_char in zip(self.hex_editor.cursors,
                                        self.old_hex_chars):
            unhex_old_char = binascii.hexlify(old_hex_char).decode()
            unhex_old_char = unhex_old_char if unhex_old_char else '00'
            if self.context == EditMode.HEX:
                if cursor.cell_index == 0:
                    new_hex_char = binascii.unhexlify(self.new_hex_char +
                                                      unhex_old_char[1]
                                                      )
                else:
                    new_hex_char = binascii.unhexlify(unhex_old_char[0] +
                                                      self.new_hex_char
                                                      )
            else:
                new_hex_char = self.new_hex_char.encode()
            self.hex_editor.file.write(new_hex_char, cursor.pointer)
        self.hex_editor.move_cursors_right()
