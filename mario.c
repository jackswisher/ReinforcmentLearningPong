//Prints a pyramid with a gap of two spaces for a height between 0 and 23

#include <cs50.h>
#include <stdio.h>
#include <string.h>

//designates the three additional methods
void printPyramid(int height);
void printLeft(int numspaces, int numblocks);
void printRight(int numblocks);

int main(void)
{
    int height;
    do
    {
        //Get a height between 0 and 23 inclusive.
        height = get_int("Enter a height between 0 and 23: ");
    }
    while (height < 0 || height > 23);

    //calls printPyramid for desired height
    printPyramid(height);
}

//prints the entire pyramid for a given height
void printPyramid(int height)
{
    //initial values to print pyramid
    int numspaces = height - 1;
    int numblocks = 1;

    for (int row = 0; row < height; row ++)
    {
        //print left side of pyramid for current row
        printLeft(numspaces, numblocks);
        //print "gap" for current row
        printf("  ");
        //print right side of pyramid
        printRight(numblocks);
        //modify numblocks and numspaces accordingly
        numblocks ++;
        numspaces --;
        //end row and begin a new line
        printf("\n");
    }
}

void printLeft(int numspaces, int numblocks)
{
    for (int i = 0; i < numspaces; i ++)
    {
        printf(" ");
    }

    for (int col = 0; col < numblocks; col ++)
    {
        printf("#");
    }
}

void printRight(int numblocks)
{
    for (int col = 0; col < numblocks; col ++)
    {
        printf("#");
    }
}