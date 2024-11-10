#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height
    int height;

    do
    {
        height = get_int("Enter height: ");
    }
    while (height > 8 || height < 1);

    // The loops
    for (int i = 0; i < height; i++)            //Newline
    {
        for (int j = height - i - 1; j > 0; j--)  //Spaces
        {
            printf(" ");
        }

        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}