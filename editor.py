import os.path
from hex_file import HexFile


class HexEditor:
    def __init__(self, file: HexFile):
        self.file: HexFile = file


def main():
    text = 'aaaaaaa0a0a0a0dddd'
    text_aboba = 'eeee'
    path = 'some_file'
    mode = 'r+b' if os.path.isfile(path) else 'w+b'
    with open('some_file', mode) as file:
        file = HexFile(file)
        print(file.read())

        file.write(b'\xdd', 5)
        file.write(b'\xdd', 6)
        file.write(b'\xdd', 7)
        file.write(b'\xdd', 8)
        print(file.read())

        file.delete(5)
        print(file.read())


if __name__ == "__main__":
    main()
