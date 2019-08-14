# https://docs.cs50.net/2019/x/psets/6/bleep/bleep.html
# Implement a program that censors messages that contain words that appear on a list of supplied "banned words."

from cs50 import get_string
from sys import argv

if len(argv) < 2 or len(argv) > 2:
    print("Usage: python bleep.py dictionary")
    exit(1)

# user input filename
filename = argv[1]

# open file
file = open(filename, mode='r')  # R for Read
text = file.read()
file.close()

# split the file content into an array of words
words = text.split("\n")

for word in words:
    word = word.lower()

input = get_string("What message would you like to censor?\n")

# split the user input into an array of words
inputWords = input.split(" ")

result = ""

for inputWord in inputWords:
    if str(inputWord).lower() in words:
        inputWordLength = len(inputWord)

        for i in range(0, inputWordLength):
            result = result + "*"
        result = result + " "
    else:
        result = result + inputWord + " "

print(result)

'''
def main():


if __name__ == "__main__":
    main()
'''