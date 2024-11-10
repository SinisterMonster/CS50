#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Temp var to hold grey value
    int gray_value = 0;

    // Loop through image px by px
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate average and round it
            gray_value =
                round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0);

            // Assign it back to image px
            image[i][j].rgbtRed = gray_value;
            image[i][j].rgbtBlue = gray_value;
            image[i][j].rgbtGreen = gray_value;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Temp vars to hold grey value
    int sepiaRed = 0, sepiaGreen = 0, sepiaBlue = 0;

    // Loop through image px by px
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate sepia and round it
            sepiaRed = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen +
                             0.189 * image[i][j].rgbtBlue);
            sepiaGreen = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen +
                               0.168 * image[i][j].rgbtBlue);
            sepiaBlue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen +
                              0.131 * image[i][j].rgbtBlue);

            // Limit the px calculated above to 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Assign it back to image px
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Temp var to hold value
    RGBTRIPLE temp_img[height][width];

    // Loop through image px by px
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp_img[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Assign it back to image
            image[i][j] = temp_img[i][width - j - 1];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // Create a copy of image
    RGBTRIPLE image_copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_copy[i][j] = image[i][j];
        }
    }

    // Filter implementation
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int counter = 0, avgBlue = 0, avgRed = 0, avgGreen = 0;

            // Take value from k-1, k and k+1 rows
            for (int row = (i - 1); row <= (i + 1); row++)
            {
                // Take value from l-1, l and l+1 column
                for (int col = (j - 1); col <= (j + 1); col++)
                {
                    if (row >= 0 && row < height && col >= 0 && col < width)
                    {
                        counter++;
                        avgBlue = avgBlue + image_copy[row][col].rgbtBlue;
                        avgGreen = avgGreen + image_copy[row][col].rgbtGreen;
                        avgRed = avgRed + image_copy[row][col].rgbtRed;
                    }
                }
            }

            // Write back to original image
            image[i][j].rgbtBlue = round(avgBlue / (float) counter);
            image[i][j].rgbtGreen = round(avgGreen / (float) counter);
            image[i][j].rgbtRed = round(avgRed / (float) counter);
        }
    }

    return;
}
