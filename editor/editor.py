from editor.hex_file import HexFile
from commands.command import Command


class HexEditor:
    ROWS_COUNT = 16
    COLUMNS_COUNT = 16

    def __init__(self, file: HexFile):
        self.file: HexFile = file

        self.column_index: int = 0
        self.row_index: int = 0
        self.cell_index: int = 0

        self.row_offset: int = 0

        self.do_stack: list[Command] = []
        self.undo_stack: list[Command] = []

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

    @property
    def pointer(self):
        return ((self.row_index + self.row_offset) *
                HexEditor.COLUMNS_COUNT + self.column_index)

    def execute_command(self, command: Command):
        self.undo_stack.append(command)
        command.do()
        if self.do_stack:
            self.do_stack.clear()

    def do(self):
        if self.do_stack:
            self.undo_stack.append(self.do_stack.pop())
            self.undo_stack[-1].do()

    def undo(self):
        if self.undo_stack:
            self.do_stack.append(self.undo_stack.pop())
            self.do_stack[-1].undo()
