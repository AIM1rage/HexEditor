import binascii
import os
from editor.hex_file import HexFile
from utils import get_char_from_byte

rows_count = 15

current_row_index = 0
columns_count = 16


def render_window():
    global current_row_index

    path = 'some_file'
    mode = 'r+b' if os.path.isfile(path) else 'w+b'
    with open(path, mode) as file:
        hex_file = HexFile(file)
        raw_window = hex_file.read_window(rows_count, columns_count,
                                          current_row_index)
        rows = [raw_window[columns_count * i: columns_count * (i + 1)] for i in
                range(rows_count)]
        for row in rows:
            current_row_index += 1
            print(render_string_from_bytes(row))


def move_cursor():
    ...


def render_string_from_bytes(unhex_bytes):
    hex_bytes = binascii.hexlify(unhex_bytes)

    cells = [hex_bytes[i: i + 2].decode() for i in
             range(0, len(hex_bytes), 2)]
    cells.extend('..' for _ in range(columns_count - len(cells)))
    cells_string = ' '.join(cell for cell in cells)

    bytes_decoded = [get_char_from_byte(unhex_bytes[i: i + 1]) for i in
                     range(len(unhex_bytes))]
    bytes_decoded_string = ''.join(bytes_decoded)

    row_index = hex(current_row_index * columns_count)[2:]
    row_index_string = row_index.rjust(10, '0')

    return row_index_string + '\t' + cells_string + '\t' + bytes_decoded_string


if __name__ == '__main__':
    render_window()
