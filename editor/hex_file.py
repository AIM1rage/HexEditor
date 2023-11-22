import os
from typing import BinaryIO


class HexFile:
    def __init__(self, file: BinaryIO):
        self.file: BinaryIO = file

    def read(self) -> bytes:
        self.file.seek(0, os.SEEK_SET)
        return self.file.read()

    def read_hex_char(self, position: int) -> bytes:
        self.file.seek(position, os.SEEK_SET)
        return self.file.read(1)
    
    def read_window(self, rows_count, columns_count, row_index) -> bytes:
        return self.read_chunk(row_index * columns_count, rows_count * columns_count)


    def read_chunk(self, position, length) -> bytes: 
        self.file.seek(position, os.SEEK_SET)
        return self.file.read(length)

    def insert(self, hex_char: bytes, position: int):
        self.file.seek(position)
        buffer = self.file.read()

        self.file.seek(position)
        self.file.write(hex_char)

        self.file.seek(position + len(hex_char))
        self.file.write(buffer)


    def write(self, hex_char: bytes, position: int):
        self.file.seek(position, os.SEEK_SET)
        self.file.write(hex_char)

    def delete(self, position: int):
        self.file.seek(position + 1, os.SEEK_SET)
        buffer = self.file.read()

        self.file.seek(position, os.SEEK_SET)
        self.file.truncate()

        self.file.seek(position, os.SEEK_SET)
        self.file.write(buffer)
