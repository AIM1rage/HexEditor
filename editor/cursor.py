from enum import IntEnum

ROWS_COUNT = 16
COLUMNS_COUNT = 16


class EditMode(IntEnum):
    HEX = 0x00
    CHAR = 0x01


class Cursor:

    def __init__(self):
        self.column_index: int = 0
        self.row_index: int = 0
        self.cell_index: int = 0

        self.row_offset: int = 0
        self.context: EditMode = EditMode.HEX

    @property
    def y(self) -> int:
        return self.row_index

    @property
    def hex_x(self) -> int:
        return 3 * self.column_index + self.cell_index

    @property
    def char_x(self) -> int:
        return self.column_index

    @property
    def pointer(self) -> int:
        return ((self.row_index + self.row_offset) *
                COLUMNS_COUNT + self.column_index
                )

    def switch_context(self):
        self.context = (EditMode.CHAR if self.context == EditMode.HEX else
                        EditMode.HEX)

    def set_cursor(self, position: tuple[int, int, int, int]):
        (self.row_index,
         self.column_index,
         self.cell_index,
         self.row_offset,
         ) = position

    def move_up(self):
        if self.row_index == 0 and self.row_offset > 0:
            self.row_offset -= 1
        elif self.row_index > 0:
            self.row_index -= 1

    def move_down(self):
        if self.row_index >= ROWS_COUNT - 1:
            self.row_offset += 1
        else:
            self.row_index += 1

    def move_left(self):
        if self.context == EditMode.HEX and self.cell_index == 1:
            self.cell_index = 0
        elif self.column_index > 0:
            self.column_index -= 1
            self.cell_index = 1
        elif self.row_offset + self.row_index > 0:
            self.move_up()
            self.column_index = COLUMNS_COUNT - 1
            self.cell_index = 1

    def move_right(self):
        if self.context == EditMode.HEX and self.cell_index == 0:
            self.cell_index = 1
        elif self.column_index < COLUMNS_COUNT - 1:
            self.column_index += 1
            self.cell_index = 0
        else:
            self.move_down()
            self.column_index = 0
            self.cell_index = 0
