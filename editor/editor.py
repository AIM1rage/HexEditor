from copy import copy
from collections import deque
from editor.file import HexFile
from editor.cursor import Cursor, EditMode, ROWS_COUNT, COLUMNS_COUNT
from commands.command import Command


class HexEditor:
    def __init__(self, file: HexFile):
        self.file: HexFile = file
        self.context: EditMode = EditMode.HEX

        self.cursors: list[Cursor] = [Cursor()]
        self.row_offset: int = 0

        self.redo_stack: deque[Command] = deque()
        self.undo_stack: deque[Command] = deque(maxlen=1000)

    @property
    def rows(self) -> list[bytes]:
        raw_window = self.file.read_window(ROWS_COUNT,
                                           COLUMNS_COUNT,
                                           self.row_offset,
                                           )
        return [raw_window[
                COLUMNS_COUNT * i:
                COLUMNS_COUNT * (i + 1)
                ] for i in range(ROWS_COUNT)]

    @property
    def upper_cursor(self) -> Cursor:
        return min(self.cursors, key=lambda c: (
            c.row_offset + c.row_index, c.column_index
        ))

    @property
    def lower_cursor(self) -> Cursor:
        return max(self.cursors, key=lambda c: (
            c.row_offset + c.row_index, c.column_index
        ))

    @property
    def pointer(self) -> int:
        return self.upper_cursor.pointer

    def switch_context(self):
        self.context = (EditMode.CHAR if self.context == EditMode.HEX else
                        EditMode.HEX)
        for cursor in self.cursors:
            cursor.switch_context()

    def execute_command(self, command: Command):
        command.do()
        self.undo_stack.append(command)
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
        self.cursors[0].set_cursor(position)

    def merge_cursors(self):
        new_cursors = []
        for cursor in self.cursors:
            if cursor not in new_cursors:
                new_cursors.append(cursor)
        self.cursors = new_cursors

    def add_upper_cursor(self):
        if self.upper_cursor.row_index > 0:
            new_upper_cursor = copy(self.upper_cursor)
            new_upper_cursor.row_index -= 1
            self.cursors.append(new_upper_cursor)

    def add_lower_cursor(self):
        if self.lower_cursor.row_index < ROWS_COUNT - 1:
            new_lower_cursor = copy(self.lower_cursor)
            new_lower_cursor.row_index += 1
            self.cursors.append(new_lower_cursor)

    def move_cursors_up(self):
        upper_cursor = self.upper_cursor
        upper_cursor.move_up()
        if self.row_offset != upper_cursor.row_offset:
            self.update_row_offset(upper_cursor.row_offset)
        else:
            for cursor in self.cursors:
                if cursor != upper_cursor:
                    cursor.move_up()

    def move_cursors_down(self):
        lower_cursor = self.lower_cursor
        lower_cursor.move_down()
        if self.row_offset != lower_cursor.row_offset:
            self.update_row_offset(lower_cursor.row_offset)
        else:
            for cursor in self.cursors:
                if cursor != lower_cursor:
                    cursor.move_down()

    def move_cursors_left(self):
        upper_cursor = self.upper_cursor
        upper_cursor.move_left()
        for cursor in self.cursors:
            if cursor != upper_cursor:
                cursor.move_left()
                if self.row_offset != upper_cursor.row_offset:
                    cursor.row_offset = upper_cursor.row_offset
                    cursor.row_index += 1
        self.row_offset = upper_cursor.row_offset

    def move_cursors_right(self):
        lower_cursor = self.lower_cursor
        lower_cursor.move_right()
        for cursor in self.cursors:
            if cursor != lower_cursor:
                cursor.move_right()
                if self.row_offset != lower_cursor.row_offset:
                    cursor.row_offset = lower_cursor.row_offset
                    cursor.row_index -= 1
        self.row_offset = lower_cursor.row_offset

    def update_row_offset(self, row_offset: int):
        self.row_offset = row_offset
        for cursor in self.cursors:
            cursor.row_offset = self.row_offset
