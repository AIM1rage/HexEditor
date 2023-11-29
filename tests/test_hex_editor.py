import pytest
import os

from editor.editor import HexEditor, HexFile
from commands.delete import DeleteCommand
from commands.write import WriteCommand


def test_big_file_symbol_removal():
    is_confirmed = False
    with open(f'test_cache', 'w+b') as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        hex_editor.cursors[0].set_cursor((10 ** 8, 0, 0, 0))
        hex_editor.execute_command(WriteCommand(hex_editor, '0'))
        try:
            hex_editor.cursors[0].set_cursor((0, 0, 0, 0))
            hex_editor.execute_command(DeleteCommand(hex_editor, False))
        except UserWarning:
            is_confirmed = True
    assert is_confirmed


def test_simple_symbol_add():
    length = 10
    with open(f'test_cache', 'w+b') as file:
        hex_file = HexFile(file)
        hex_editor = HexEditor(hex_file)
        hex_editor.cursors[0].set_cursor((0, length, 0, 0))
        hex_editor.execute_command(WriteCommand(hex_editor, 'a'))
    file_size = os.path.getsize('test_cache')
    assert file_size == length + 1
