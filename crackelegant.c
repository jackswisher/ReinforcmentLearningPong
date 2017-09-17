// Program that

#define _XOPEN_SOURCE       /* See feature_test_macros(7) */
#include <unistd.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>


int main(int argc, string argv[])
{
    if (argc == 2)
    {
        string hash = argv[1];

        const char available[52] = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

        char salt[3];
        salt[0] = hash[0];
        salt[1] = hash[1];
        salt[2] = '\0';

        printf("%s\n", salt);

        char password[6];
        password[5] = '\0';
        string finalPassword = "FAIL";
        char trial[6];
        trial[5] = '\0';
        bool done = false;
        int passLength = 1;

        for (int first = 0; first < 52 && !done; first++)
        {
            if(passLength == 1)
            {
                password[0] = available[first];
                password[1] = '\0';
                if (strcmp (crypt (password, salt), hash) == 0)
                {
                    finalPassword = password;
                    done = true;
                }
                else if(first == 51)
                {
                    first = 0;
                    passLength++;
                }
            }

            for (int second = 0; second < 52 && !done && passLength > 1; second++)
            {
                if(passLength == 2)
                {
                    password[0] = available[first];
                    password[1] = available[second];
                    password[2] = '\0';

                    if (strcmp (crypt (password, salt), hash) == 0)
                    {
                        finalPassword = password;
                        done = true;
                    }
                    else if(first == 51)
                    {
                        first = 0;
                        passLength++;
                    }
                }

                for (int third = 0; third < 52 && !done && passLength > 2; third++)
                {
                    if(passLength == 3)
                    {
                        password[0] = available[first];
                        password[1] = available[second];
                        password[2] = available[third];
                        password[3] = '\0';

                        if (strcmp (crypt (password, salt), hash) == 0)
                        {
                            finalPassword = password;
                            done = true;
                        }
                        else if(first == 51)
                        {
                            first = 0;
                            passLength++;
                        }
                    }

                    for (int fourth = 0; fourth < 52 && !done && passLength > 3; fourth++)
                    {
                        if(passLength == 4)
                        {
                            password[0] = available[first];
                            password[1] = available[second];
                            password[2] = available[third];
                            password[3] = available[fourth];
                            password[4] = '\0';

                            if (strcmp (crypt (password, salt), hash) == 0)
                            {
                                finalPassword = password;
                                done = true;
                            }
                            else if(first == 51)
                            {
                                first = 0;
                                passLength++;
                            }
                        }

                        for (int fifth = 0; fifth < 52 && !done && passLength > 4; fifth++)
                        {
                            password[0] = available[first];
                            password[1] = available[second];
                            password[2] = available[third];
                            password[3] = available[fourth];
                            password[4] = available[fifth];

                            if (strcmp (crypt (password, salt), hash) == 0)
                            {
                                finalPassword = password;
                                done = true;
                            }
                        }
                    }
                }
            }
        }

        if(done)
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
        // print error
        printf("%s\n", crypt ("GxAzV", "50"));
        printf ("Usage: ./crack hash\n");
        return 1;
    }
}
