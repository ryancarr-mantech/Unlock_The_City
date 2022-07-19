import binascii
with open("binary.jpeg", 'r') as f:
    data = f.read()

final = ''
amount = 0
for char in data:
    if char == '9':
        final += '1'
    else:
        final += '0'
    amount += 1
    if amount >=8:
        binary_int = int(final, 2)
  
        byte_number = binary_int.bit_length() + 7 // 8
        
        binary_array = binary_int.to_bytes(byte_number, "big")
    

        ascii_text = binary_array.decode()
  
        print(ascii_text, end='')
        final = ''
        #print(" ", end='')
        amount = 0