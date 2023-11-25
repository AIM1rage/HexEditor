import os
import sys
import curses
from utils import render_string_from_bytes, render_title
from editor.hex_file import HexFile, HEX_CHARS
from editor.editor import HexEditor, EditMode
from commands.delete import DeleteCommand
from commands.write import WriteCommand
from commands.paste import PasteCommand

HEX_OFFSET_Y = 1
HEX_OFFSET_X = 24

CHR_OFFSET_Y = 1
CHR_OFFSET_X = 72


def process_key(hex_editor: HexEditor, key):
    match key:
        case 'KEY_UP':
            hex_editor.move_cursor_up()
        case 'KEY_DOWN':
            hex_editor.move_cursor_down()
        case 'KEY_LEFT':
            hex_editor.move_cursor_left()
        case 'KEY_RIGHT':
            hex_editor.move_cursor_right()
        case 'KEY_DC':
            # Delete - character deletion
            hex_editor.execute_command(DeleteCommand(hex_editor))
        case '':
            # Ctrl + Z - undo
            hex_editor.undo()
        case '':
            # Ctrl + Y - redo
            hex_editor.redo()
        case '':
            # Ctrl + P - paste
            hex_editor.execute_command(PasteCommand(hex_editor))
        case '	':
            # Ctrl + I - context switching
            hex_editor.switch_context()
        case _:
            if hex_editor.context == EditMode.HEX:
                if key.lower() in HEX_CHARS:
                    hex_editor.execute_command(WriteCommand(
                        hex_editor,
                        key.lower(),
                    ))
            else:
                if key.isprintable():
                    hex_editor.execute_command(WriteCommand(hex_editor, key))


def render_window(main_screen, hex_editor: HexEditor):
    title = render_title(hex_editor.pointer)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    main_screen.addstr(0, 0, title, curses.color_pair(1))
    for index, row in enumerate(hex_editor.rows):
        main_screen.addstr(
            index + 1,
            0,
            render_string_from_bytes(
                row,
                hex_editor.row_offset + index,
                hex_editor.COLUMNS_COUNT,
            ),
        )
    if hex_editor.context == EditMode.HEX:
        offset_y, offset_x = HEX_OFFSET_Y, HEX_OFFSET_X

    else:
        offset_y, offset_x = CHR_OFFSET_Y, CHR_OFFSET_X
    main_screen.addstr(hex_editor.cursor_y + offset_y,
                       hex_editor.cursor_x + offset_x,
                       '',
                       )


def main(main_screen, filename):
    mode = 'r+b' if os.path.isfile(filename) else 'w+b'
    with open(filename, mode) as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)

        main_screen.keypad(True)
        curses.curs_set(1)
        main_screen.nodelay(0)
        while True:
            main_screen.clear()
            render_window(main_screen, hex_editor)
            key = main_screen.getkey()
            if key.lower() == 'q':
                break
            else:
                process_key(hex_editor, key)

            main_screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filename.")
        sys.exit(1)
    curses.wrapper(main, sys.argv[1])
