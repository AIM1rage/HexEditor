import curses
import binascii
from editor.file import HEX_CHARS
from editor.editor import HexEditor
from editor.cursor import EditMode, ROWS_COUNT, COLUMNS_COUNT, Cursor
from commands.delete import DeleteCommand
from commands.write import WriteCommand
from commands.paste import PasteCommand

OFFSET_Y = 1
HEX_OFFSET_X = 16
CHAR_OFFSET_X = 72


class HexApplication:
    def __init__(self, hex_editor: HexEditor, window):
        self.hex_editor: HexEditor = hex_editor
        self.window = window
        self.message: str = ''

    def run_event_loop(self):
        while True:
            self.window.clear()
            self.hex_editor.merge_cursors()
            self.render_window()
            self.handle()
            self.window.refresh()

    def handle(self):
        key = self.window.getkey()
        match key:
            case 'KEY_UP':
                self.hex_editor.move_cursors_up()
            case 'KEY_DOWN':
                self.hex_editor.move_cursors_down()
            case 'KEY_LEFT':
                self.hex_editor.move_cursors_left()
            case 'KEY_RIGHT':
                self.hex_editor.move_cursors_right()
            case 'KEY_DC':
                # Delete - character deletion
                try:
                    self.hex_editor.execute_command(
                        DeleteCommand(self.hex_editor, False),
                    )
                except UserWarning as delete_warning:
                    self.message = str(delete_warning)
                    if self.get_confirmation():
                        self.hex_editor.execute_command(
                            DeleteCommand(self.hex_editor, True),
                        )
                except ValueError as delete_error:
                    self.message = str(delete_error)
            case '':
                # Ctrl + Z - undo
                self.hex_editor.undo()
            case '':
                # Ctrl + Y - redo
                self.hex_editor.redo()
            case '':
                # Ctrl + P - paste
                try:
                    self.hex_editor.execute_command(
                        PasteCommand(self.hex_editor))
                except ValueError as paste_error:
                    self.message = str(paste_error)
            case '	':
                # Ctrl + I - context switching
                self.hex_editor.switch_context()
            case 'CTL_DOWN':
                # Ctrl + Down - add lower cursor
                self.hex_editor.add_lower_cursor()
            case 'CTL_UP':
                # Ctrl + Up - add upper cursor
                self.hex_editor.add_upper_cursor()
            case _:
                if self.hex_editor.context == EditMode.HEX:
                    if key.lower() in HEX_CHARS:
                        self.hex_editor.execute_command(WriteCommand(
                            self.hex_editor,
                            key.lower(),
                        ))
                else:
                    if key.isprintable() and len(key) == 1:
                        self.hex_editor.execute_command(
                            WriteCommand(self.hex_editor, key))
        self.message = f'{len(self.hex_editor.cursors)=}'

    def render_window(self):
        title = self.render_title()
        self.window.addstr(0, 0, title, curses.A_BOLD)
        for index, row in enumerate(self.hex_editor.rows):
            string = self.render_string_from_bytes(index, row)
            self.window.addstr(index + 1, 0, string)
        for cursor in self.hex_editor.cursors:
            self.add_hex(cursor)
            self.add_char(cursor)
        self.render_message()

    def render_message(self):
        self.window.addstr(ROWS_COUNT + 2, 0, self.message)

    def get_confirmation(self):
        key = self.window.getkey()
        return key == 'y' or key == 'Y'

    def add_hex(self, cursor: Cursor):
        cursor_y = cursor.y + OFFSET_Y
        hex_cursor_x = cursor.hex_x + HEX_OFFSET_X
        self.add_cursor(cursor_y, hex_cursor_x,
                        self.get_cursor_color(EditMode.HEX),
                        )

    def add_char(self, cursor: Cursor):
        cursor_y = cursor.y + OFFSET_Y
        char_cursor_x = cursor.char_x + CHAR_OFFSET_X
        self.add_cursor(cursor_y, char_cursor_x,
                        self.get_cursor_color(EditMode.CHAR),
                        )

    def add_cursor(self, y: int, x: int, color: int):
        self.window.addch(y, x, self.get_char_from_window(y, x), color)

    def get_cursor_color(self, context: EditMode) -> int:
        return (curses.A_REVERSE if context == self.hex_editor.context else
                curses.A_BLINK)

    def render_title(self) -> str:
        position_string = hex(self.hex_editor.pointer)[2:].rjust(10, '0')
        title_string = ' '.join(f'0{c}' for c in HEX_CHARS)
        return f'{position_string}\t{title_string}\t|\tDecoded text'

    def render_string_from_bytes(self,
                                 index: int,
                                 unhex_bytes: bytes,
                                 ) -> str:
        hex_bytes = binascii.hexlify(unhex_bytes)
        current_row_index = self.hex_editor.row_offset + index

        cells = [hex_bytes[i: i + 2].decode() for i in
                 range(0, len(hex_bytes), 2)]
        cells.extend('..' for _ in range(COLUMNS_COUNT -
                                         len(cells)))
        cells_string = ' '.join(cell for cell in cells)

        bytes_decoded = [
            HexApplication.get_char_from_byte(unhex_bytes[i: i + 1])
            for i in
            range(len(unhex_bytes))]
        bytes_decoded_string = ''.join(bytes_decoded)

        row_index = hex(current_row_index * COLUMNS_COUNT)[2:]
        row_index_string = row_index.rjust(10, '0')

        return '\t'.join(
            (row_index_string, cells_string, '|', bytes_decoded_string))

    def get_char_from_window(self, y: int, x: int) -> str:
        return chr(self.window.inch(y, x) & 0b11111111)

    @staticmethod
    def get_char_from_byte(byte: bytes) -> str:
        try:
            char = byte.decode()
            return char if char.isprintable() else '.'
        except (UnicodeDecodeError, curses.error):
            return '.'
