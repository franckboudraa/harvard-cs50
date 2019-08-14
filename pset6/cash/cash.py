# https://docs.cs50.net/2019/x/psets/6/sentimental/cash/cash.html
# Implement a program that calculates the minimum number of coins required to give a user change.

import cs50


def format_money(n):
    return int(round(n * 100))


change = float(0)
coins = 0
# our coins types
coins_types = [0.25, 0.10, 0.05, 0.01]
coins_types_count = len(coins_types)

while(change <= 0):
    # ask user for input
    change = cs50.get_float("Change owed: ")

change_left = format_money(change)

while(change_left > 0):
    for i in range(0, coins_types_count):
        if format_money(coins_types[i]) <= change_left:
            coins += 1
            change_left -= format_money(coins_types[i])
            break

print(coins)