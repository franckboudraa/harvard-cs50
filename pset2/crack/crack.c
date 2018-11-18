// https://docs.cs50.net/2018/x/psets/2/crack/crack.html
// Implement a program that cracks passwords

#define _XOPEN_SOURCE
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

int main(int argc, string argv[])
{
    // If user doesn't provided hashed password for argument to decrypt
    if (argc < 2 || argc > 2)
    {
        printf("Usage: ./crack hash\n");
        return 1; // error
    }

    // Password must be an alphabetical character
    string chars = "\0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string input = argv[1];
    char password[6] = "\0\0\0\0\0\0"; // init an empty string
    char salt[2]; // salt in C DES crypt function consist of string of 2 chars
    salt[0] = input[0]; // takes the 2 first characters of hashed password as salt
    salt[1] = input[1];
    const int chars_count = 57; // length hard writed because of \0 in empty string (stop strlen)

    // surely not the most fastest method but it does the job!
    for (int fifth_pos = 0; fifth_pos < chars_count; fifth_pos++)
    {
        for (int fourth_pos = 0; fourth_pos < chars_count; fourth_pos++)
        {
            for (int third_pos = 0; third_pos < chars_count; third_pos++)
            {
                for (int second_pos = 0; second_pos < chars_count; second_pos++)
                {
                    for (int first_pos = 1; first_pos < chars_count; first_pos++)
                    {
                        password[0] = chars[first_pos];
                        password[1] = chars[second_pos];
                        password[2] = chars[third_pos];
                        password[3] = chars[fourth_pos];
                        password[4] = chars[fifth_pos];

                        if (strcmp(crypt(password, salt), input) == 0) // compare the computed hash with the input
                        {
                            printf("%s\n", password); // we have found the original password
                            return 0; // houra!
                        }
                    }
                }
            }
        }
    }
    
    printf("Unable to find password\n");
    return 1;
}