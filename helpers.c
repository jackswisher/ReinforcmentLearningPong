// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    if (strlen(fraction) != 3)
    {
        return 1;
    }
    int numerator = fraction[0] - '0';
    int denominator = fraction[2] - '0';

    return numerator * (8 / denominator);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    double semitone = 0;
    if (note[0] != 'A' && note[0] != 'B')
    {
        //note is to the left of A; should be negative
        int distancetoa = 7 - (note[0] - 'A');
        semitone = -2 * distancetoa;

        if (distancetoa > 2)
        {
            //correct for only one semitone between E and F
            semitone++;
        }
    }
    else
    {
        //note is either A or B
        semitone = 2 * (note[0] - 'A');
    }

    //take into account octave
    semitone = semitone + 12 * (note[strlen(note) - 1] - '0' - 4);

    if (strlen(note) == 3)
    {
        //if the note has an accidental change semitone accordingly
        if (note[1] == '#')
        {
            semitone++;
        }
        else
        {
            semitone--;
        }
    }

    return round(pow(2, semitone / 12) * 440);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    return strcmp(s, "") == 0;
}
