import binascii
import pyperclip
from editor.hex_file import HEX_CHARS
from commands.command import Command
from editor.editor import EditMode, HexEditor


def parse_input_from_clipboard(mode: EditMode):

    data = pyperclip.paste()
    answer: bytes
    if mode == EditMode.HEX:
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
