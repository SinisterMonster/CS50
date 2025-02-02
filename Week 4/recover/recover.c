#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for correct cmd line arg usage
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Return error if unable to open file
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    BYTE buffer[512];

    // Init vars to for filename and keeping count of imgs
    char filename[8] = {0};
    int counter = 0;
    FILE *outputImage = NULL;

    // Read while there's still data left to read from the memory card
    while (fread(buffer, sizeof(BYTE), 512, card) == 512)
    {
        // Check for JPEG header to find start of new JPEG
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) &&
            ((buffer[3] & 0xf0) == 0xe0))
        {
            // Close file if one is already open
            if (outputImage != NULL)
            {
                fclose(outputImage);
            }

            // Generate filename and increment
            sprintf(filename, "%03i.jpg", counter);
            counter++;

            // Open file to write
            outputImage = fopen(filename, "w");
        }

        // If file exists and is open write to file
        if (outputImage != NULL)
        {
            fwrite(buffer, sizeof(BYTE), 512, outputImage);
        }
    }

    // Close files
    fclose(outputImage);
    fclose(card);

    return 0;
}
