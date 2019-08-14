# https://docs.cs50.net/2019/x/psets/6/sentimental/mario/less/mario.html
# Implement a program that prints out a half-pyramid of a specified height.

import cs50

# initializing var for user input
height = ""

# prompt the user for number between 1 and 8
while height.isdigit() == False or int(height) < 1 or int(height) > 8:
    height = cs50.get_string("Height: ")

# drawing pyramid
for i in range(0, int(height)):
    for j in range(0, int(height) - (i + 1)):
        print(" ", end='')

    for h in range(0, i):
        print("#", end='')

    print("#\n", end='')