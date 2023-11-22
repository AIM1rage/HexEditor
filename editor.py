from typing import BinaryIO


class HexEditor:
    def __init__(self, file: BinaryIO):
        self.file = file


def main():
    text = 'aaaaaaa0a0a0a0dddd'
    text_aboba = 'eeee'
    with open('some_file', 'r+b') as file:
        editor = HexEditor(file)


if __name__ == "__main__":
    main()
