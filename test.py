with open('aboba.txt', 'w+b') as file:
    file.seek(110)
    file.write(b'\xaa')