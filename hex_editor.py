import os
import sys
import curses
from utils import render_string_from_bytes
from editor.hex_file import HexFile

rows_count = 8

current_row_index = 0
columns_count = 16


def main(main_screen, filename):
    global current_row_index

    # Установка режима curses
    curses.curs_set(1)
    main_screen.nodelay(0)

    # Инициализация позиции
    offset = 0

    # Пример параметров отображения
    bytes_per_row = 16
    mode = 'r+b' if os.path.isfile(filename) else 'w+b'
    with open(filename, mode) as file:
        hex_file = HexFile(file)
        raw_window = hex_file.read_window(rows_count, columns_count,
                                          current_row_index)
        rows = [raw_window[columns_count * i: columns_count * (i + 1)] for i in
                range(rows_count)]

    # stdscr.addstr()
    while True:
        # Очистка экрана
        main_screen.move(2, 1)
        curses.curs_set(1)
        main_screen.clear()

        # Отображение данных в виде шестнадцатеричного представления
        for index, row in enumerate(rows):
            current_row_index += 1
            main_screen.addstr(index + 1, 0,
                               render_string_from_bytes(row, current_row_index,
                                                   columns_count))

        # Обновление экрана
        main_screen.refresh()

        # Ожидание ввода пользователя
        key = main_screen.getch()

        # Обработка ввода пользователя
        if key == curses.KEY_UP:
            if offset - bytes_per_row >= 0:
                offset -= bytes_per_row
        elif key == curses.KEY_DOWN:
            if offset + bytes_per_row < len(file.read()):
                offset += bytes_per_row
        elif key == curses.KEY_LEFT:
            if offset - 1 >= 0:
                offset -= 1
        elif key == curses.KEY_RIGHT:
            if offset + 1 < len(file.read()):
                offset += 1
        elif key == ord('q'):
            break

    # Завершение curses
    curses.endwin()


# Входная точка программы
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filename.")
        sys.exit(1)
    curses.wrapper(main, sys.argv[1])
