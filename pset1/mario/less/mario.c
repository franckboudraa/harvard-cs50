// https://docs.cs50.net/2018/x/psets/1/mario/less/mario.html
#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;

    // Prompt user for height between 1 and 23
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (height - (i + 1)); j++)
        {
            printf(" ");
        }
        for (int h = 0; h <= i; h++)
        {
            printf("#");
        }
        printf("#\n");
    }
}