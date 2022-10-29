import binascii

encoded = 'AFAAADEBAEAAECA4BAAFAEAA8AC0A7B0BC9ABAA5A5BAAFB89DB8F9AE9DABB4BCB6'\
    'B3909AA8'

key = 0xC7

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

encodedbytes = binascii.a2b_hex(encoded)[::-1]

str = ""
tmp = 0
for i in range(37):
    tmp2 = tmp & 3
    str += chr((encodedbytes[i] - rol(1, tmp2, 8) - 1)^key)
    tmp += encodedbytes[i]

print(str)
