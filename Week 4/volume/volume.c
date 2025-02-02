// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

// Function declaration
void copy_header(FILE *input, FILE *output);
void copy_samples(FILE *input, FILE *output, float factor);

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    copy_header(input, output);
    copy_samples(input, output, factor);

    // Close files
    fclose(input);
    fclose(output);
}

// Function to copy the header file
void copy_header(FILE *input, FILE *output)
{
    uint8_t header[HEADER_SIZE];

    fread(header, sizeof(header), 1, input);
    fwrite(header, sizeof(header), 1, output);
}

// Function to copy the samples by looping through the input file
void copy_samples(FILE *input, FILE *output, float factor)
{
    int16_t buffer;

    while (fread(&buffer, sizeof(int16_t), 1, input) != 0)
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }
}
