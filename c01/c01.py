data = b'\x1F\x08\x13\x13\x04"\x0E\x11M\x0D\x18=\x1B\x11\x1C\x0F\x18P\x12\x13S\x1E\x12\x10'
for b in data:
    print(chr(b^0x7D), end='')
print()