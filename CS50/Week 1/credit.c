#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int main(void)
{
    // Get input
    long card;
    card = get_long("Number: ");

    // Length of card number
    int card_length = floor(log10(card)) + 1;

    // Get starting 2 digits
    long starting_digits = card;
    do
    {
        starting_digits = starting_digits / 10;
    }
    while (starting_digits > 100);


    // Checksum calculation
    long card_copy = card;
    int sum_multiplied_by_two = 0;
    int sum_not_multiplied_by_two = 0;
    int total_sum = 0;
    int remainder = 0;
    int last_num = 0;
    int temp1 = 0;
    int temp2 = 0;

    do
    {
        //Get last # (odd), add that to the sum_not_multiplied_by_two, remove the last # from card
        last_num = card_copy % 10;
        sum_not_multiplied_by_two = sum_not_multiplied_by_two + last_num;
        card_copy = card_copy / 10;

        // Get second last digit (even) now the last num, add to sum_multiplied_by_two, then remove that from card
        last_num = (card_copy % 10) * 2;
        // Doing this since instructions says: "'add those products’ digits (i.e., not the products themselves) together"
        temp1 = last_num % 10;
        temp2 = last_num / 10;

        sum_multiplied_by_two = sum_multiplied_by_two + temp1 + temp2;
        card_copy = card_copy / 10;
    }
    while (card_copy > 0);

    total_sum = sum_multiplied_by_two + sum_not_multiplied_by_two;

    // Check
    // Luhn check
    if ((total_sum % 10 != 0) || (card_length != 13 && card_length != 15 && card_length != 16))
    {
        printf("INVALID\n");
    }
    else
        // Checks based on length and starting digits to classify card issuer
    {
        if ((card_length == 15) && ((starting_digits == 34) || (starting_digits == 37)))
        {
            printf("AMEX\n");
        }
        else if (card_length == 16)
        {
            if ((starting_digits >= 51) && (starting_digits <= 55))
            {
                printf("MASTERCARD\n");
            }
            else if (starting_digits / 10 == 4)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if ((card_length == 13) && (starting_digits % 10 == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
}