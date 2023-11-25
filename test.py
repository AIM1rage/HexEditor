with open("aboba.txt", "w+b") as file:
    file.seek(10**9 + 10)
    file.write(b'\xaa')

