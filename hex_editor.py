import os
import sys
import curses
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filename.")
        sys.exit(1)
    try:
        curses.wrapper(main, sys.argv[1])
    except KeyboardInterrupt:
        print('Bye!')
