# https://docs.cs50.net/2019/x/psets/6/sentimental/caesar/caesar.html
# Implement a program that encrypts messages using Caesar’s cipher.

import cs50
from sys import argv

ALPHABET_LENGTH = 26

if len(argv) < 2 or len(argv) > 2:
    print("You forgot to provide an argument: key integer for encryption!")
    exit(1)

# convert arg to an integer
key = int(argv[1])

# prompt user for a text to encrypt
input = cs50.get_string("plaintext: ")
inputLength = len(input)
result = ""

for i in range(0, inputLength):
    if input[i].isalpha():
        if input[i].isupper():
            # apply to the char the caesar formula for upper char
            result = result + chr(65 + (ord(input[i]) - 65 + key) % ALPHABET_LENGTH)
        elif input[i].islower():
            # apply to the char the caesar formula for lower char
            result = result + chr(97 + (ord(input[i]) - 97 + key) % ALPHABET_LENGTH)
    else:
        result = result + input[i]

print("ciphertext:", result)