# More comfortable mario: prints a pyramid of specified height

from cs50 import get_int


def main():
    height = get_int('Enter a height between 0 and 23: ')

    while not (0 <= height <= 23):
        # Keep getting input if height is not between 0 and 23
        height = get_int('Enter a height between 0 and 23: ')

    numspaces = height - 1
    numblocks = 1

    for row in range(height):
        # Create a string with the finished row
        final = string_repeated(' ', numspaces) + string_repeated('#', numblocks)
        final = final + '  ' + string_repeated('#', numblocks)
        print(final)

        # Update numspaces and numblocks
        numspaces -= 1
        numblocks += 1


# Return a string with a repeated number of characters
def string_repeated(char, numtimes):
    string = ""

    for i in range(numtimes):
        string = string + char

    return string


if __name__ == "__main__":
    main()
