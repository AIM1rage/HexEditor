import os
from typing import BinaryIO


class HexFile:
    def __init__(self, file: BinaryIO):
        self.file: BinaryIO = file

    def read(self) -> bytes:
        self.file.seek(0, os.SEEK_SET)
        return self.file.read()

    def read_char(self, position):
        self.file.seek(0, os.SEEK_SET)
        return self.file.read(1)

    def insert(self, char: bytes, position: int):
        self.file.seek(position)
        buffer = self.file.read()

        self.file.seek(position)
        self.file.write(char)

        self.file.seek(position + 1)
        self.file.write(buffer)

    def write(self, char: bytes, position: int):
        self.file.seek(position, os.SEEK_SET)
        self.file.write(char)

    def delete(self, position: int):
        self.file.seek(position, os.SEEK_SET)
        buffer = self.file.read()

        self.file.seek(position, os.SEEK_SET)
        self.file.truncate()

        self.file.seek(position, os.SEEK_SET)
        self.file.write(buffer[1:])
