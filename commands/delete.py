from commands.command import Command
from editor.editor import HexEditor


class DeleteCommand(Command):
    def __init__(self, hex_editor: HexEditor, is_confirmed: bool):
        super().__init__(hex_editor)
        self.is_confirmed = is_confirmed
        self.deleted_hex_char: bytes = (self.hex_editor.file.read_hex_char(
            self.cursors[0].pointer,
        ))

    def undo(self):
        self.restore_editor_state()
        self.hex_editor.file.insert(self.deleted_hex_char,
                                    self.cursors[0].pointer)

    def do(self):
        self.restore_editor_state()

        if len(self.hex_editor.cursors) > 1:
            raise ValueError('Unsupported deletion for multiple cursors')
        if abs(self.hex_editor.pointer -
               self.hex_editor.file.length) > 10 ** 6:
            if not self.is_confirmed:
                raise UserWarning('Trying to delete the symbol from BIG file. '
                                  'Please confirm this operation [y/Y]')

        self.hex_editor.file.delete(self.cursors[0].pointer)
