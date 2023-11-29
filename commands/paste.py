import binascii
import pyperclip
from editor.file import HEX_CHARS
from commands.command import Command
from editor.editor import HexEditor
from editor.cursor import EditMode


def parse_input_from_clipboard(context: EditMode) -> bytes:
    data = pyperclip.paste()
    if context == EditMode.HEX:
        res = []
        for ch in data:
            if ch in HEX_CHARS:
                res.append(ch)
            else:
                res.append('0')
        if len(res) % 2 != 0:
            last = res.pop()
            res.append('0')
            res.append(last)
        hexes = "".join(res).encode()
        answer = binascii.unhexlify(hexes)
    else:
        answer = data.encode()
    return answer


class PasteCommand(Command):
    def __init__(self, hex_editor: HexEditor):
        super().__init__(hex_editor)
        self.new_chars: bytes = parse_input_from_clipboard(self.context)
        self.old_hex_chars: bytes = (self
                                     .hex_editor
                                     .file
                                     .read_chunk(self.cursors[0].pointer,
                                                 len(self.new_chars),
                                                 )
                                     )

    def undo(self):
        self.restore_editor_state()

        self.hex_editor.file.write(self.old_hex_chars, self.cursors[0].pointer)

        self.restore_file_length()

    def do(self):
        self.restore_editor_state()

        if len(self.hex_editor.cursors) > 1:
            raise ValueError('Unsupported pasting for multiple cursors')

        self.hex_editor.file.write(self.new_chars, self.cursors[0].pointer)
        iterations_count = (
            len(self.new_chars) * 2 if self.context == EditMode.HEX
            else len(self.new_chars))
        for _ in range(iterations_count):
            self.hex_editor.move_cursors_right()
        self.hex_editor.cursors[0].cell_index = 0
