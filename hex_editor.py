import os
import curses
import argparse
from editor.file import HexFile
from editor.editor import HexEditor
from application import HexApplication


def main(main_window, filename):
    mode = 'r+b' if os.path.isfile(filename) else 'w+b'
    main_window.keypad(True)
    curses.curs_set(0)
    main_window.nodelay(False)
    with open(filename, mode) as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        application = HexApplication(hex_editor, main_window)
        application.run_event_loop()
        curses.endwin()


usage = '''
To run program enter:
python hex_editor.py [filename]

Combinations:
Ctrl + , - undo
Ctrl + . - redo
Ctrl + P - paste string from clipboard
Ctrl + Up - add upper cursor
Ctrl + Down - add lower cursor
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Hex Editor',
                                     usage=usage,
                                     description='Simple hex editor with a console interface',
                                     )
    parser.add_argument('filename',
                        type=str,
                        help='Absolute or relative path to the file',
                        )
    args = parser.parse_args()
    curses.wrapper(main, args.filename)
