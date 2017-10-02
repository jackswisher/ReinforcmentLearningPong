// Program recovers all JPEGs stored in a .raw file when stored back to back with the correct JPEG heading for each file.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

typedef uint8_t  BYTE;

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover infile\n");
        return 1;
    }

    char *infile = argv[1];

    // open input file
    FILE *raw_file = fopen(infile, "r");

    if (raw_file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // creates a buffer BLOCK_SIZE in length
    BYTE *buffer = malloc(BLOCK_SIZE);

    // int to keep track of whether the program is currently in a file
    int inFile = 0;

    // current file number
    int fileNum = 0;

    // the current open file
    FILE *img;

    while (fread(buffer, BLOCK_SIZE, 1, raw_file) == 1)
    {
        // At start?
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (inFile)
            {
                // close current file and create a new one
                fclose(img);

                char filename[10];

                // format file name as XXX.jpg where XXX is a number starting from 000
                sprintf(filename, "%03i.jpg", fileNum);
                img = fopen(filename, "w");
                fileNum++;
            }
            else
            {
                // create a new file
                char filename[10];

                sprintf(filename, "%03i.jpg", fileNum);
                img = fopen(filename, "w");

                fileNum++;
                inFile = 1;
            }
        }

        if (inFile)
        {
            // if currently in a JPEG, write to the image
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }

    if (img == NULL)
    {
        fprintf(stderr, "File could not be terminated!\n");
        return 3;
    }

    fclose(img);

    free(buffer);
}