// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

#define HASH_LENGTH 500000

typedef struct linked_list node;

struct linked_list
{
    char word[LENGTH + 1];
    node *next;
};

node *table[HASH_LENGTH];
int numElements = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // prepare to make newword a lower case version of word
    char newword[LENGTH + 1];
    int i = 0;

    // convert word to lower case using bitwise opperator
    while (word[i] != '\0')
    {
        newword[i] = (word[i] | 0x20);
        i++;
    }

    // terminate word
    newword[i] = '\0';

    // retrieve first node
    node *current = table[hash(word)];

    // check if the linked list contains the word
    return contains(current, newword);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // uses file I/O to read in the dictionary
    FILE *dictionary_file = fopen(dictionary, "r");

    if (dictionary_file == NULL)
    {
        // couldn't be loaded
        return false;
    }

    // create an array to read word into
    char word[LENGTH + 1];

    while (fscanf(dictionary_file, "%s", word) != EOF)
    {
        // find index in hashtable for where to store word
        unsigned long index = hash(word);

        // create a new node and copy the word into the new node
        node *newnode = malloc(sizeof(node));
        strcpy(newnode->word, word);

        newnode->next = table[index];

        // store new word
        table[index] = newnode;

        // update counter
        numElements++;
    }

    // successfully finished reading file
    fclose(dictionary_file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return numElements;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASH_LENGTH; i++)
    {
        // free each linked list
        if (!freeNode(table[i]))
        {
            return false;
        }
    }
    return true;
}

// recursive function that checks if a linked list contains a matching word
bool contains (node *current, const char *word)
{
    if (current == NULL)
    {
        return false;
    }

    if (strcmp(current->word, word) == 0)
    {
        return true;
    }

    return contains(current->next, word);
}

// recursive function that frees each node in a linked list
bool freeNode(node *current)
{
    if (current == NULL)
    {
        // at the end of the linked list
        return true;
    }

    // store next node, free current node, and proceed to next node
    node *next = current->next;
    free(current);
    return freeNode(next);
}

// dbj2 hash function obtained from: http://www.cse.yorku.ca/~oz/hash.html
unsigned long hash(const char *str)
{
    unsigned long hash = 5381;
    int c;

    while ((c = *str++))
    {
        hash = ((hash << 5) + hash) + (c | 0x20);
    }

    // returns a valid index in the table
    return (hash % HASH_LENGTH);
}
