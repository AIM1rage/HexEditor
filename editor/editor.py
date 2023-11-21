import os.path
import binascii
from hex_file import HexFile


class HexEditor:
    def __init__(self, file: HexFile):
        self.file: HexFile = file


def main():
    text = '482254cec0dee8fb1caed0c4080045000028af7540008006e7dcc0a80066d5b4ccbaea7101bbe93702b37dee313950110200c3160000'
    path = 'some_file'
    mode = 'r+b' if os.path.isfile(path) else 'w+b'
    with open('some_file', mode) as file:
        file = HexFile(file)
        print(file.read())

        file.write(binascii.unhexlify(text), 3)
        print(file.read())


if __name__ == "__main__":
    main()
