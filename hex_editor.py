import os
import sys
import curses
from utils import render_string_from_bytes, parse_input_from_clipboard
from editor.hex_file import HexFile, HEX_CHARS
from editor.editor import HexEditor
from commands.delete import DeleteCommand
from commands.write import WriteCommand
from commands.paste import PasteCommand

OFFSET_Y = 1
OFFSET_X = 24


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
            chars = parse_input_from_clipboard()
            hex_editor.execute_command(PasteCommand(hex_editor, chars))
        case _:
            if key.lower() in HEX_CHARS:
                hex_editor.execute_command(
                    WriteCommand(hex_editor, key.lower()))


def print_window(main_screen, hex_editor: HexEditor):
    position_string = hex(hex_editor.pointer)[2:].rjust(10, '0')
    title = f'{position_string}\t|\t00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f'
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
    main_screen.addstr(hex_editor.cursor_y + OFFSET_Y,
                       hex_editor.cursor_x + OFFSET_X,
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
            print_window(main_screen, hex_editor)
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
