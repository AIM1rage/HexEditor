import sys
import os
from typing import BinaryIO

HEX_CHARS = '1234567890abcdef'


class HexFile:
    def __init__(self, file: BinaryIO):
        self.file: BinaryIO = file

    @property
    def length(self) -> int:
        return sys.getsizeof(self.file)

    def read(self) -> bytes:
        self.file.seek(0, os.SEEK_SET)
        return self.file.read()

    def read_hex_char(self, position: int) -> bytes:
        return self.read_chunk(position, 1)

    def read_window(self, rows_count, columns_count, row_offset) -> bytes:
        return self.read_chunk(row_offset * columns_count,
                               rows_count * columns_count)

    def read_chunk(self, position, length) -> bytes:
        self.file.seek(position, os.SEEK_SET)
        return self.file.read(length)

    def insert(self, hex_chars: bytes, position: int):
        if not hex_chars:
            return
        self.file.seek(position)
        buffer = self.file.read()

        self.file.seek(position)
        self.file.write(hex_chars)

        self.file.seek(position + len(hex_chars))
        self.file.write(buffer)

    def write(self, hex_chars: bytes, position: int):
        self.file.seek(position, os.SEEK_SET)
        self.file.write(hex_chars)

    def delete(self, position: int):
        self.file.seek(position + 1, os.SEEK_SET)
        buffer = self.file.read()

        self.file.seek(position, os.SEEK_SET)
        self.file.truncate()

        if not buffer:
            return

        self.file.seek(position, os.SEEK_SET)
        self.file.write(buffer)

    def truncate(self, length):
        self.file.truncate(length)
