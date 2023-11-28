from collections import deque
from editor.file import HexFile
from editor.cursor import Cursor, EditMode, ROWS_COUNT, COLUMNS_COUNT
from commands.command import Command


class HexEditor:
    def __init__(self, file: HexFile):
        self.file: HexFile = file
        self.context: EditMode = EditMode.HEX

        self.cursor: Cursor = Cursor()

        self.redo_stack: deque[Command] = deque()
        self.undo_stack: deque[Command] = deque(maxlen=100)

    @property
    def rows(self) -> list[bytes]:
        raw_window = self.file.read_window(ROWS_COUNT,
                                           COLUMNS_COUNT,
                                           self.cursor.row_offset,
                                           )
        return [raw_window[
                COLUMNS_COUNT * i:
                COLUMNS_COUNT * (i + 1)
                ] for i in range(ROWS_COUNT)]

    @property
    def cursor_y(self) -> int:
        return self.cursor.y

    @property
    def hex_cursor_x(self) -> int:
        return self.cursor.hex_x

    @property
    def char_cursor_x(self) -> int:
        return self.cursor.char_x

    @property
    def pointer(self) -> int:
        return self.cursor.pointer

    def switch_context(self):
        self.context = (EditMode.CHAR if self.context == EditMode.HEX else
                        EditMode.HEX)
        self.cursor.switch_context()

    def execute_command(self, command: Command):
        self.undo_stack.append(command)
        command.do()
        if self.redo_stack:
            self.redo_stack.clear()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.undo_stack[-1].do()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            self.redo_stack[-1].undo()

    def set_cursor(self, position: tuple[int, int, int, int]):
        self.cursor.set_cursor(position)

    def move_cursors_up(self):
        self.cursor.move_up()

    def move_cursors_down(self):
        self.cursor.move_down()

    def move_cursors_left(self):
        self.cursor.move_left()

    def move_cursors_right(self):
        self.cursor.move_right()
