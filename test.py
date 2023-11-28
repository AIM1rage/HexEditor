with open('aboba.txt', 'w+b') as file:
    file.seek(60)
    file.write(b'\xaa')