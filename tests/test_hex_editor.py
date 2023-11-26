import pytest
import os

from editor.editor import HexEditor, HexFile
from commands.delete import DeleteCommand
from commands.write import WriteCommand


def generate_file(size, name):
    with open(name, 'w+b') as file:
        file.seek(size - 1)
        file.write(b'\xaa')


def test_huy():
    assert True


def test_big_file_symbol_removal():
    confirmation = False
    without_confirmation = False

    generate_file(10 ** 9 + 10, 'aboba.txt')

    with open('aboba.txt', 'r+b') as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        hex_editor.set_cursor((0, 0, 0, 0))
        try:
            hex_editor.execute_command(DeleteCommand(hex_editor, False))
        except:
            confirmation = True

        hex_editor.set_cursor((10, 0, 0, 0))
        try:
            hex_editor.execute_command(DeleteCommand(hex_editor, False))
            without_confirmation = True
        except:
            without_confirmation = False
        
    os.remove('aboba.txt')
    assert confirmation and without_confirmation
        


def test_simple_symbol_add():
    generate_file(10, 'aboba.txt')
    with open('aboba.txt', 'r+b') as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        hex_editor.set_cursor((0, 10, 0, 0))
        hex_editor.execute_command(WriteCommand(hex_editor, 'a'))
        
    file_size = os.path.getsize('aboba.txt')    
    os.remove('aboba.txt')
    assert file_size == 11


def test_paste_odd_hexes():
    pass


def test_paste_nearby_eof():
    pass


def remove_last_symbol():
    generate_file(10, 'aboba.txt')
    with open('aboba.txt', 'r+b') as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        hex_editor.set_cursor((0, 10, 0, 0))
        hex_editor.execute_command(DeleteCommand(hex_editor, False))
        
    file_size = os.path.getsize('aboba.txt')    
    os.remove('aboba.txt')
    assert file_size == 9


def paste_gigabyte():
    pass