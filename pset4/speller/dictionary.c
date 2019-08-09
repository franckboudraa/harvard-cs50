// https://docs.cs50.net/2019/x/psets/4/speller/trie/speller.html
// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

node *root; // represents a trie
int dictionnarySize = 0;

// loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // initialize trie
    root = malloc(sizeof(node));

    if (root == NULL)
    {
        return false;
    }

    root->is_word = false;

    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // open dictionary
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        unload();
        return false;
    }

    // buffer for a word
    char word[LENGTH + 1];

    // current node && adequate child node
    node *cur = root;

    // loop through dictionnary for inserting words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // start from root node on each word
        cur = root;

        for (int i = 0, l = strlen(word); i < l; i++)
        {
            // if node already exist
            if (cur->children[getIndex(word[i])] != NULL)
            {
                // move the cursor on the next node
                cur = cur->children[getIndex(word[i])];
            }
            else
            {
                // create node
                cur->children[getIndex(word[i])] = malloc(sizeof(node));

                // move the cursor on our new node
                cur = cur->children[getIndex(word[i])];
                cur->is_word = false;

                for (int m = 0; m < N; m++)
                {
                    cur->children[m] = NULL;
                }
            }

            // if we are on the last char of the word, flag node as a word
            if (i-l == -1)
            {
                cur->is_word = true;
                dictionnarySize++;
            }
        }
    }

    // close dictionary
    fclose(file);

    // indicate success
    return true;
}

// returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dictionnarySize;
}

// returns true if word is in dictionary, else false
bool check(const char *word)
{
    // current node && adequate child node
    node *cur = root;
    bool knownWord = true;

    // must be case insensitive
    for (int i = 0, l = strlen(word); i < l; i++)
    {
        if (cur->children[getIndex(word[i])] != NULL)
        {
            // node child exist for this char, continue
            cur = cur->children[getIndex(word[i])];
        }
        else
        {
            knownWord = false;
            break;
        }

         if (i-l == -1)
         {
             if (cur->is_word == true)
             {
                break; // knownWord = true
             }
             else
             {
                knownWord = false;
                break;
             }
         }
    }

    return knownWord;
}

// unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    freeNode(root);

    return true;
}

// returns the array index by char
int getIndex(char c)
{
    switch(tolower(c))
    {
        case '\'':
            return 26;
        default:
            return tolower(c) - 97;
    }
}

// free node memory
bool freeNode(node *node)
{
    for (int i = 0; i < N; i++)
    {
        // if node child doesn't exist
        if (node->children[i] != NULL)
        {
            freeNode(node->children[i]);
        }
    }

    free(node);

    return true;
}