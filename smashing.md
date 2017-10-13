# Stack Smashing

## Questions

1. A stack canary is a value or flag stored after a buffer that will be overwritten if there is a buffer overflow, and if the canary is overwritten then we know that the buffer overflowed. If the canary is untouched then no overflow occured.

2. It is called a canary because it is a reference to when canaries were brought into mines so that miners could tell if there was posionous gas or if it was safe to proceed. If the canary dies, ie. overwritten, then it is not safe!

3.
int get_myfavoriteint()
{
    char 5char[5];
    int fav = 1738;
    string toconvert = get_string("Enter a 5 character string:");
    for (int i = 0; i < 6; i++)
    {
        5char[i] = toconvert[i];
    }
    return fav;
}

## Debrief

1. The YouTube video linked on the question page.

2. 5 minutes.
