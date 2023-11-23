from commands.command import Command
from editor.editor import HexEditor


class PasteCommand(Command):
    def __init__(self, hex_editor: HexEditor, new_chars: bytes):
        super().__init__(hex_editor)
        self.new_chars: bytes = new_chars
        self.old_hex_chars: bytes = (self
                                     .hex_editor
                                     .file
                                     .read_chunk(self.pointer,
                                                 len(self.new_chars),
                                                 )
                                     )

    def undo(self):
        self.hex_editor.file.write(self.old_hex_chars, self.pointer)
        self.hex_editor.file.truncate(self.old_length)
        self.hex_editor.set_cursor(self.position)

    def do(self):
        self.hex_editor.set_cursor(self.position)
        self.hex_editor.file.write(self.new_chars, self.pointer)
        for _ in range(len(self.new_chars) * 2):
            self.hex_editor.move_cursor_right()
        self.hex_editor.cell_index = 0
