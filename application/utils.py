def get_char_from_byte(byte: bytes) -> str:
    try:
        char = byte.decode()
        return char if char.isprintable() else '.'
    except UnicodeDecodeError:
        return '.'
