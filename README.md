# Questions

## What's `stdint.h`?

stdin.h is a header file that allows type definitions of specific widths. For example, stdin.h allows DWORD to be defined as an integer with 32 bits.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

These declarations create an integer with exact width. The 'uint8_t' means an unsigned integer of 8 bits while 'int32_t' is equivelent to an integer of exactly 32 bits.
This is helpful for creating variables that are an exact size, which is useful if you know the maximum value of a variable and whether it will need to positive and negative.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A BYTE is 8 bits or one byte. A DWORD is 4 bytes. A LONG is 4 bytes. A WORD is 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

The file is identified by the bfType which for a BMP is 0x4d42. These two bytes are the first two bytes that make up a BMP file.

## What's the difference between `bfSize` and `biSize`?

The bfSize is the file size in bytes of the entire bitmap file, meanwhile biSize returns the number of bytes required by the BITMAPINFOHEADER struct.

## What does it mean if `biHeight` is negative?

If the biHeight is negative it means that the top left corner of the image is the origin.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

There is a WORD called biBitCount that specifies the bits per pixel of the file.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If it is unable to open the file, for example if there is no file with that name or at the specified path, then fopen will return null.

## Why is the third argument to `fread` always `1` in our code?

For our purposes we only want to read one element at a time of a given size, which in our case is a single pixel.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

If bi.biWidth is 3 then padding will equal 3 because rgbtripples are 3 bytes in size and 9 % 4 = 1, so padding equals 4 - 1 which equals 3.

## What does `fseek` do?

fseek moves the position of where fread and fwrite will continue from. It repositions where in the stream we are.

## What is `SEEK_CUR`?

SEEK_CUR is a #define that is an underlying integer that when passed to fseek causes fseek to move through the file relative to the current position.
