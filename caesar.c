// Program that uses a cipher key to encode a message, perserves upper and lower case

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // assumes nonnegative number for key
        int key = atoi (argv[1]) % 26;

        string plaintext = get_string ("plaintext: ");
        int length = strlen (plaintext);

        char ciphertext[length + 1];

        for (int i = 0; i < length; i++)
        {
            // if the character is alphabetical, applies cipher
            // otherwise, leaves character unchanged
            char current = plaintext[i];
            if (current >= 'a' && current <= 'z')
            {
                // character is lowercase
                current = 'a' + (current - 'a' + key) % 26;
            }
            else if (current >= 'A' && current <= 'Z')
            {
                // character is uppercase
                current = 'A' + (current - 'A' + key) % 26;
            }
            ciphertext[i] = current;
        }
        ciphertext[length] = '\0';

        printf("ciphertext: ");
        printf ("%s\n", ciphertext);
    }
    else
    {
        // print error
        printf ("Usage: ./caesar k\n");
        return 1;
    }
}