#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// sentence_end [] = {'.', '!', '?'};

int letter_counter(string text);
int word_counter(string text);
int sentence_counter(string text);
int compute_score(int letter_count, int word_count, int sentence_count);

int main(void)
{
    // Ask user input
    string text = get_string("Text: ");

    // Compute
    int letter_count = letter_counter(text);
    int word_count = word_counter(text);
    int sentence_count = sentence_counter(text);
    int score = compute_score(letter_count, word_count, sentence_count);

    // Print grade
    if (score > 16)
    {
        printf("Grade 16+");
    }
    else if (score < 1)
    {
        printf("Before Grade 1");
    }
    else
    {
        printf("Grade %i", score);
    }
    printf("\n");
}

// Counts letters
int letter_counter(string text)
{
    int letter_count = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isalpha(text[i]))
        {
            letter_count++;
        }
    }
    return letter_count;
}

// Counts words
int word_counter(string text)
{
    int word_count = 1;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isblank(text[i]))
        {
            word_count++;
        }
    }
    return word_count;
}

// Counts sentences
int sentence_counter(string text)
{
    int sentence_count = 0;

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (!isalpha(text[i]))
        {
            if (text[i] == '.' || text[i] == '!' || text[i] == '?')
            {
                sentence_count++;
            }
        }
    }
    return sentence_count;
}

// Final reading level computation using Coleman-Liau index
int compute_score(int letter_count, int word_count, int sentence_count)
{
    float L = ((float) letter_count / word_count) * 100;
    float S = ((float) sentence_count / word_count) * 100;

    float score = round((0.0588 * L) - (0.296 * S) - 15.8);

    printf("\n-----\nL = %f S = %f\n-----\nletter_count: %d \n word_count: %d \n sentence_count: %d \n Score: %f\n", L, S,
           letter_count, word_count, sentence_count, score);
    return score;
}