//Takes a valid number greater than 0 and determines the type of card if it is a valid credit number

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

string checkSum(string type, int digits[], int length);

int main(void)
{
    long long creditNum;
    do
    {
        //gets a number greater than 0
        creditNum = get_long_long("Number: ");
    }
    while (creditNum <= 0);

    //declaration of necessary variables, also finds the length of the cc number
    int length = floor(log10(creditNum)) + 1;
    int digits[length];
    string type = "";

    for (int i = 0; i < length; i ++)
    {
        //adds each digit seperately to an array
        digits[length - i - 1] = creditNum % 10;
        creditNum = creditNum / 10;
    }

    if (length == 15 && digits[0] == 3 && (digits[1] == 4 || digits[1] == 7))
    {
        //15 digits, begins with 34 or 37: is an AMEX unless checksum fails
        type = "AMEX";
    }
    else if ((length == 13 || length == 16) && digits[0] == 4)
    {
        //13 or 16 digits, begins with 4: is a VISA unless checksum fails
        type = "VISA";
    }
    else if (length == 16 && digits[0] == 5 && (digits[1] >= 1 && digits[1] <= 5))
    {
        //16 digits and begins with 5 and a second digit between 1 and 5: MASTERCARD
        type = "MASTERCARD";
    }
    else
    {
        //otherwise, invalid
        type = "INVALID";
    }

    if (strcmp(type, "INVALID") != 0)
    {
        type = checkSum(type, digits, length);
    }

    printf("%s \n", type);
}

string checkSum(string type, int digits[], int length)
{
    int counter = 0;
    int total = 0;
    for (int i = length - 1; i >= 0; i --)
    {
        int product;
        if (counter % 2 != 0)
        {
            product = 2 * digits[i];
            int tendigit = (product - product % 10);
            total = total + tendigit / 10 + product - tendigit;
            // printf("%i : %i \n", digits[i], total);
        }
        else
        {
            total = total + digits[i];
        }
        counter ++;
    }

    if (total % 10 != 0)
    {
        return "INVALID";
    }
    else
    {
        return type;
    }
}