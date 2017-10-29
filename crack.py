# Brute force cracking of short passwords

import crypt
import sys

MAX_LEN = 5
SALT_LEN = 2
NULL_TERMINATOR = '1'


def main():
    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' <hash>')
        return 1

    hash = sys.argv[1]
    salt = hash[0: SALT_LEN]

    # Create a string to store guesses with the character that we define as not part of the password
    cur_guess = NULL_TERMINATOR

    increment_location = 0
    rolling_over = False

    # Repeat until we have checked every possible password
    while increment_location < MAX_LEN:
        # Not currently rolling over
        rolling_over = False

        # Store char that we are checking
        cur_char = cur_guess[increment_location]

        # Advance through the characters
        if cur_char == NULL_TERMINATOR:
            # NULL_TERMINATOR goes to 'a'
            cur_guess = cur_guess[:increment_location] + 'a' +
                cur_guess[increment_location + 1:]
        elif cur_char == 'z':
            # 'z' goes to 'A'
            cur_guess = cur_guess[:increment_location] + 'A' +
                cur_guess[increment_location + 1:]
        elif cur_char == 'Z':
            # 'Z' rolls over and resets current position to 'a'
            cur_guess = cur_guess[:increment_location] + 'a' +
                cur_guess[increment_location + 1:]
            increment_location += 1

            if increment_location == len(cur_guess):
                # Need to increase the length of the passwords we are checking
                cur_guess += NULL_TERMINATOR

            rolling_over = True
        else:
            # Increment the ASCII value of the char we are incrementing
            cur_guess = cur_guess[:increment_location] +
                chr(ord(cur_char) + 1) + cur_guess[increment_location + 1:]

        # Unless we are rolling over, check guess
        if not rolling_over:
            # If our guess is the same as the hash, then it is cracked
            if crypt.crypt(cur_guess, salt) == hash:
                print(cur_guess)
                return 0

            # Reset to incrementing far left, roll over is done
            increment_location = 0

    # Not able to crack
    print('Unable to crack this password')
    return 2


if __name__ == "__main__":
    main()
