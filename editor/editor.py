from collections import deque
from editor.file import HexFile
from commands.command import Command
from enum import IntEnum


class EditMode(IntEnum):
    HEX = 0x00
    CHAR = 0x01


class HexEditor:
    ROWS_COUNT = 16
    COLUMNS_COUNT = 16

    def __init__(self, file: HexFile):
        self.file: HexFile = file
        self.context: EditMode = EditMode.HEX

        self.column_index: int = 0
        self.row_index: int = 0
        self.cell_index: int = 0

        self.row_offset: int = 0

        self.redo_stack: deque[Command] = deque()
        self.undo_stack: deque[Command] = deque(maxlen=100)

    @property
    def rows(self) -> list[bytes]:
        raw_window = self.file.read_window(HexEditor.ROWS_COUNT,
                                           HexEditor.COLUMNS_COUNT,
                                           self.row_offset,
                                           )
        return [raw_window[
                HexEditor.COLUMNS_COUNT * i:
                HexEditor.COLUMNS_COUNT * (i + 1)
                ] for i in range(HexEditor.ROWS_COUNT)]

    @property
    def cursor_y(self) -> int:
        return self.row_index

    @property
    def hex_cursor_x(self) -> int:
        return 3 * self.column_index + self.cell_index

    @property
    def char_cursor_x(self) -> int:
        return self.column_index

    @property
    def pointer(self) -> int:
        return ((self.row_index + self.row_offset) *
                HexEditor.COLUMNS_COUNT + self.column_index
                )

    def switch_context(self):
        self.context = (EditMode.CHAR if self.context == EditMode.HEX else
                        EditMode.HEX)

    def execute_command(self, command: Command):
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
        (self.row_index,
         self.column_index,
         self.cell_index,
         self.row_offset,
         ) = position

    def move_cursor_up(self):
        if self.row_index == 0 and self.row_offset > 0:
            self.row_offset -= 1
        elif self.row_index > 0:
            self.row_index -= 1

    def move_cursor_down(self):
        if self.row_index >= HexEditor.ROWS_COUNT - 1:
            self.row_offset += 1
        else:
            self.row_index += 1

    def move_cursor_left(self):
        if self.context == EditMode.HEX and self.cell_index == 1:
            self.cell_index = 0
        elif self.column_index > 0:
            self.column_index -= 1
            self.cell_index = 1
        elif self.row_offset + self.row_index > 0:
            self.move_cursor_up()
            self.column_index = HexEditor.COLUMNS_COUNT - 1
            self.cell_index = 1

    def move_cursor_right(self):
        if self.context == EditMode.HEX and self.cell_index == 0:
            self.cell_index = 1
        elif self.column_index < HexEditor.COLUMNS_COUNT - 1:
            self.column_index += 1
            self.cell_index = 0
        else:
            self.move_cursor_down()
            self.column_index = 0
            self.cell_index = 0
