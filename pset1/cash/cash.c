// https://docs.cs50.net/2018/x/psets/1/cash/cash.html

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <cs50.h>

// Format money from float to int
// Example : 20.50 = 2050
int format_money(float n)
{
    return (int) round(n * 100);
}

int main(void)
{
    float change;
    int change_left;
    int coins = 0;
    float coins_types[] = {0.25, 0.10, 0.05, 0.01}; // our coins types
    size_t coins_types_count = sizeof(coins_types) / sizeof(coins_types[0]);
    
    do
    {
        change = get_float("Change owed: "); // ask user for input
    }
    while (change <= 0);
    
    change_left = format_money(change);
    
    do
    {
        for (int i = 0; i < coins_types_count; i++)
        {
            if (format_money(coins_types[i]) <= change_left)
            {
                coins++;
                change_left -= format_money(coins_types[i]);
                break;
            }
        }
    
    }
    while (change_left > 0);
    
    printf("%i\n", coins);
}