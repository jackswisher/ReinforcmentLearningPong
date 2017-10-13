# Emoji

## Questions

1. Three bytes are required to store a jack-o-lantern because 1F383 can be represented in binary by 00000001 11110011 1010011 (Big Endian: least significant digit to the right).

2. A char is only one byte, so it would not be able to store a jack-o-lantern which is three bytes.

3.

```c
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
```

## Debrief

1. I used the man pages for strspn and strtol in order to figure out how to validate the input and to convert it to an integer.

2. Roughly 30 minutes
