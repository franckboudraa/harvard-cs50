# https://docs.cs50.net/2019/x/psets/6/sentimental/hello/hello.html
# Implement a program that prints out a simple greeting to the user.

import cs50

# Asking user for input
s = cs50.get_string("What is your name ?\n")

# Print user answer
print("Hello, {}".format(s))