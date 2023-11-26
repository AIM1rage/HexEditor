from commands.command import Command
from editor.editor import HexEditor


class DeleteCommand(Command):
    def __init__(self, hex_editor: HexEditor, checked: bool):
        super().__init__(hex_editor)
        self.checked = checked
        self.deleted_hex_char: bytes = (self
                                        .hex_editor
                                        .file
                                        .read_hex_char(self.pointer)
                                        )

    def undo(self):
        self.hex_editor.file.insert(self.deleted_hex_char, self.pointer)
        self.hex_editor.set_cursor(self.position)

    def do(self):
        if abs(self.hex_editor.pointer - self.hex_editor.file.length) > 10 ** 9:
            if not self.checked:
                raise Exception()
        self.hex_editor.set_cursor(self.position)
        self.hex_editor.file.delete(self.pointer)
        