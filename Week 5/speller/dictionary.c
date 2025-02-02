// Implements a dictionary's functionality

#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>  // For strcpy
#include <strings.h> // For strcasecmp

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Function to free lists recursively
void free_child_list(node *list);

// TODO: Choose number of buckets in hash table
const unsigned int N = 256;

// Hash table
node *table[N];

// Global variable to keep track of the size of dict
int dict_size = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Get hash code of the word to be checked
    unsigned int check_word_hash = hash(word);

    // Go to the corresponding linked list in hash table and store head
    node *head = table[check_word_hash];

    // Traverse the linked list and check for word
    while (head != NULL)
    {
        if (strcasecmp(head->word, word) == 0)
        {
            return true;
        }
        else
        {
            head = head->next;
        }
    }

    return false;
}

// Hashes word to a number
int min = 5000;
int max = 0;
int min_bin = 0, max_bin = 0;
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int bin = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        bin = ((toupper(word[i]) + tolower(word[i])) - 78);
    }
    return bin;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *dict_source = fopen(dictionary, "r");

    // Create buffer word and temp var to hold hash val
    char buffer_word[LENGTH + 1];
    unsigned int hash_code;

    // Check if file opened corrrectly
    if (dict_source == NULL)
    {
        printf("Could not load dictionary file\n");
        fclose(dict_source);
        return false;
    }

    // Loop through the dict till EOF
    while (fscanf(dict_source, "%s", buffer_word) != EOF)
    {
        // Create space for a new hash table node
        node *newNode = malloc(sizeof(node));
        if (newNode == NULL)
        {
            return false;
        }
        else
        {
            newNode->next = NULL;
        }

        // Copy buffer to node
        strcpy(newNode->word, buffer_word);

        // Get hash code
        hash_code = hash(newNode->word);

        // Insert new word to start of hash table node do this by:
        // 1. Copying the ptr in the hash table to newNode->next
        newNode->next = table[hash_code];
        // 2. Insert the ptr to newNode into hashtable
        table[hash_code] = newNode;

        // Keep the dictionary size updated
        dict_size = dict_size + 1;

        printf("%s\n", newNode->word);
    }
    fclose(dict_source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Go to last element of hash table
    int n = N;
    while (n >= 0)
    {
        // Free recursively
        free_child_list(table[n - 1]);
        n--;
    }
    return true;
}

void free_child_list(node *list)
{
    // Handle base case
    if (list == NULL)
    {
        return;
    }

    // Else free nodes in list recursively
    free_child_list(list->next);

    free(list);
}
