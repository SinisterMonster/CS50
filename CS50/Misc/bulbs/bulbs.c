#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int message_array);

int main(void)
{
    // Ask user for message
    string message = get_string("Message: ");

    // Initialize an 8 x length of text array
    int length = strlen(message);
    int message_array[length][BITS_IN_BYTE];
    memset(message_array, 0, length * BITS_IN_BYTE * sizeof(int));

    // Put letters of message into array
    for (int i = 0; i < length; i++)
    {
        message_array[i][0] = message[i]; // Make the first column in each row the value of the letter. The rest of the row is zeros
    }

    // Take each letter (now a row in array) and then convert to binary
    int character_in_decimal = 0;
    int remainder = 0;
    int qoutient = 0;
    int temp = 0;

    for (int i = 0; i < length; i++)
    {
        character_in_decimal = message_array[i][0];
        message_array[i][0] = 0;
        temp = character_in_decimal;

        // Find binary and update from right to left
        int j = BITS_IN_BYTE - 1;
        do
        {
            remainder = temp % 2;
            qoutient = temp / 2;
            temp = qoutient;

            message_array[i][j] = remainder;
            j--;

            if (remainder == 1) // End condition
            {
                for (int k = j; k >= 0; k--)
                {
                    message_array[i][k] = 0;
                }
            }
        }
        while (j >= 0);
    }

    // Print bulbs
    for (int i = 0; i < length; i++)
    {
        for (int j = 0; j < BITS_IN_BYTE; j++)
        {
            print_bulb(message_array[i][j]);
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
