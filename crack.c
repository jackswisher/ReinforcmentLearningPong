// Program that uses nested for loops to crack a DES hash of up to five alphabetical characters, upper and lower case

#define _XOPEN_SOURCE
#include <unistd.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>


int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // retrieve hash from command line argument
        string hash = argv[1];

        const char alpha[52] = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                               };

        // retrieve salt for crpyt
        char salt[3];
        salt[0] = hash[0];
        salt[1] = hash[1];
        salt[2] = '\0';

        char password[6];
        password[5] = '\0';

        string finalPassword = "FAIL";
        char trial[6];
        trial[5] = '\0';

        bool done = false;

        int passLength = 1;

        // fairly ugly way of iterating through possible passwords
        for (int first = 0; first < 52 && !done; first++)
        {
            if (passLength == 1)
            {
                // fills up password with generated char and makes sure that it has a null char in right location
                password[0] = alpha[first];
                password[1] = '\0';

                if (strcmp (crypt (password, salt), hash) == 0)
                {
                    // password found!
                    finalPassword = password;
                    done = true;
                }
                else if (first == 51)
                {
                    // no password found so restart loop and increment password length to check
                    first = 0;
                    passLength++;
                }
            }

            for (int second = 0; second < 52 && !done && passLength > 1; second++)
            {
                if (passLength == 2)
                {
                    //checking for length 2 passwords
                    password[0] = alpha[first];
                    password[1] = alpha[second];
                    password[2] = '\0';

                    if (strcmp (crypt (password, salt), hash) == 0)
                    {
                        //password found!
                        finalPassword = password;
                        done = true;
                    }
                    else if (first == 51)
                    {
                        // no password found so restart loop and increment password length to check
                        first = 0;
                        passLength++;
                    }
                }

                for (int third = 0; third < 52 && !done && passLength > 2; third++)
                {
                    if (passLength == 3)
                    {
                        //checking for length 3 passwords
                        password[0] = alpha[first];
                        password[1] = alpha[second];
                        password[2] = alpha[third];
                        password[3] = '\0';

                        if (strcmp (crypt (password, salt), hash) == 0)
                        {
                            //password found!
                            finalPassword = password;
                            done = true;
                        }
                        else if (first == 51)
                        {
                            // no password found so restart loop and increment password length to check
                            first = 0;
                            passLength++;
                        }
                    }

                    for (int fourth = 0; fourth < 52 && !done && passLength > 3; fourth++)
                    {
                        if (passLength == 4)
                        {
                            //checking for length 4 passwords
                            password[0] = alpha[first];
                            password[1] = alpha[second];
                            password[2] = alpha[third];
                            password[3] = alpha[fourth];
                            password[4] = '\0';

                            if (strcmp (crypt (password, salt), hash) == 0)
                            {
                                //password found
                                finalPassword = password;
                                done = true;
                            }
                            else if (first == 51)
                            {
                                // no password found so restart loop and increment password length to check
                                first = 0;
                                passLength++;
                            }
                        }

                        for (int fifth = 0; fifth < 52 && !done && passLength > 4; fifth++)
                        {
                            //not a 1, 2, 3, or 4 letter password; checking for length 5
                            password[0] = alpha[first];
                            password[1] = alpha[second];
                            password[2] = alpha[third];
                            password[3] = alpha[fourth];
                            password[4] = alpha[fifth];

                            if (strcmp (crypt (password, salt), hash) == 0)
                            {
                                //password found!
                                finalPassword = password;
                                done = true;
                            }
                        }
                    }
                }
            }
        }

        if (done)
        {
            printf("Success! You cracked the hash: %s and found the password: %s\n", hash, finalPassword);
        }
        else
        {
            printf("Failure. Unable to crack the hash!\n");
        }


    }
    else
    {
        // print error and return 1
        printf ("Usage: ./crack hash\n");
        return 1;
    }
}
