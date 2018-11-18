// https://docs.cs50.net/2018/x/psets/2/caesar/caesar.html
// Implement a program that encrypts messages using Caesar’s cipher

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#define ALPHABET_LENGTH 26

int main(int argc, string argv[])
{
    // If user doesn't provided key integer for argument to encrypt
    if (argc < 2 || argc > 2)
    {
        printf("You forgot to provide an argument: key integer for encryption!\n");
        return 1; // error
    }
    
    // convert string to integer
    int key = atoi(argv[1]);
    
    // ask user for text to encrypt
    string input = get_string("plaintext: ");
    
    for (int i = 0, len = strlen(input); i < len; i++)
    {
        if (isupper(input[i]))
        {
            // apply to the char the caesar formula for upper char
            input[i] = 65 + (input[i] - 65 + key) % ALPHABET_LENGTH;
        }
        else if (islower(input[i]))
        {
            // apply to the char the caesar formula for lower char
            input[i] = 97 + (input[i] - 97 + key) % ALPHABET_LENGTH;
        }
        else
        {
            // is char is not a letter, do nothing on it
        }
        
    }
    
    printf("ciphertext: %s\n", input);
    
    return 0; // everything ok
}