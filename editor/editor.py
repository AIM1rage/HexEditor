import curses
from editor.hex_file import HexFile


class HexEditor:
    ROWS_COUNT = 8
    COLUMNS_COUNT = 16

    def __init__(self, file: HexFile):
        self.file: HexFile = file

        self.column_index: int = 0
        self.row_index: int = 0
        self.cell_index: int = 0

        self.row_offset = 0

    @property
    def rows(self):
        raw_window = self.file.read_window(HexEditor.ROWS_COUNT,
                                           HexEditor.COLUMNS_COUNT,
                                           self.row_offset,
                                           )
        return [raw_window[
                HexEditor.COLUMNS_COUNT * i:
                HexEditor.COLUMNS_COUNT * (i + 1)
                ] for i in range(HexEditor.ROWS_COUNT)]

    @property
    def cursor_y(self):
        return self.row_index

    @property
    def cursor_x(self):
        return 2 * self.column_index + self.column_index + self.cell_index

    def process_key(self, key):
        match key:
            case curses.KEY_UP:
                if self.row_index == 0 and self.row_offset > 0:
                    self.row_offset -= 1
                elif self.row_index > 0:
                    self.row_index -= 1
            case curses.KEY_DOWN:
                if self.row_index >= HexEditor.ROWS_COUNT - 1:
                    self.row_offset += 1
                else:
                    self.row_index += 1
            case curses.KEY_LEFT:
                if self.column_index >= 0:
                    if self.cell_index == 1:
                        self.cell_index = 0
                    elif self.column_index > 0:
                        self.column_index -= 1
                        self.cell_index = 1
            case curses.KEY_RIGHT:
                if self.column_index <= HexEditor.COLUMNS_COUNT - 1:
                    if self.cell_index == 0:
                        self.cell_index = 1
                    elif self.column_index < HexEditor.COLUMNS_COUNT - 1:
                        self.column_index += 1
                        self.cell_index = 0
