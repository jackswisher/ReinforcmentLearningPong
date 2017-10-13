#include <cs50.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
#include <string.h>

typedef wchar_t emoji;

emoji get_emoji(string prompt);

int main(void)
{
    // Set locale according to environment variables
    setlocale(LC_ALL, "");

    // Prompt user for code point
    emoji c = get_emoji("Code point: ");

    // Print character
    printf("%lc\n", c);
}

emoji get_emoji(string prompt)
{
    string input;
    do
    {
        input = get_string("%s", prompt);
    }
    while (strlen(input) <= 2 || input[0] != 'U' || input[1] != '+' || strspn(input + 2, "0123456789ABCDEF") != (strlen(input) - 2));

    char *ptr;
    int valid = strtol(input + 2, &ptr, 16);
    emoji final = valid;
    return final;
}