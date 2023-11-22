import binascii


def get_char_from_byte(byte: bytes) -> str:
    try:
        char = byte.decode()
        return char if char.isprintable() else '.'
    except UnicodeDecodeError:
        return '.'


def render_string_from_bytes(unhex_bytes, current_row_index, columns_count):
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

    return '\t'.join(
        (row_index_string, '|', cells_string, bytes_decoded_string))
