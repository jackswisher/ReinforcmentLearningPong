// Resizes a BMP file with a factor f between 0 exclusive and 100 inclusive.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize f infile outfile\n");
        return 1;
    }

    if (argv[1] == NULL || argv[2] == NULL || argv[3] == NULL)
    {
        fprintf(stderr, "A null character cannot be accepted.\n");
        return 2;
    }

    // remember filenames
    float f = atof(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (f <= 0 || f > 100)
    {
        fprintf(stderr, "%f not between 0 exclusive and 100 inclusive.\n", f);
        return 3;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 4;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 5;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 6;
    }

    // TODO: Modify bi and bf here
    // determine padding for scanlines
    int paddingin = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // int oldHeight = bi.biHeight;
    int oldWidth = bi.biWidth;

    bi.biHeight = floor(bi.biHeight * f);
    bi.biWidth = floor(bi.biWidth * f);

    int paddingout = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + paddingout) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    //calculate and store how long each line is in bytes
    int lengthofline = (oldWidth * sizeof(RGBTRIPLE)) + paddingin;

    //integer to store last line used
    int previous = 0;

    //malloc an array of RGBTRIPLEs that stores a line at a time
    RGBTRIPLE *line = malloc(lengthofline);

    for (int height = 0; height < abs(bi.biHeight); height++)
    {
        //want the corresponding height from the old image; chose to use ceiling but could also use floor
        int heightPos = floor(1.0 * height / f);

        if (heightPos > previous || height == 0)
        {
            // if it is the first line or a new line, navigate to the correct place
            fseek(inptr, (sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + (lengthofline * heightPos)),
                  SEEK_SET);

            for (int i = 0; i < oldWidth; i++)
            {
                // use pointer arithmetic to fill the array with RGBTRIPLEs
                fread((line + i), sizeof(RGBTRIPLE), 1, inptr);
            }
        }

        for (int width = 0; width < bi.biWidth; width++)
        {
            RGBTRIPLE current;
            // calculate which old pixel corresponds to the new pixel; uses ceiling but could also choose to use floor
            int widthPos = (int)floor(width / f);

            current = line[widthPos];

            fwrite(&current, sizeof(RGBTRIPLE), 1, outptr);
        }

        // skip over padding, if any
        fseek(inptr, paddingin, SEEK_CUR);

        for (int k = 0; k < paddingout; k++)
        {
            // add padding
            fputc(0x00, outptr);
        }

        // store the previous height
        previous = heightPos;
    }

    free(line);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
