# credit.py
# Determine whether a credit card number is valid

from cs50 import get_int

# Constants related to each type of card
AMEX_1 = 34
AMEX_2 = 37
AMEX_LENGTH = 15

FIRST_MC = 51
LAST_MC = 55
MC_LENGTH = 16

FIRST_VISA = 40
LAST_VISA = 49
VISA_LENGTH1 = 13
VISA_LENGTH2 = 16


def main():
    # Request number
    cc_no = get_int('Number: ')

    checksum = 0
    first_two_digits = 0
    mult_by_two = False
    cc_no_length = 0

    while cc_no > 0:
        cur_digit = cc_no % 10

        # Add new digit to checksum, double if necessary
        if mult_by_two:
            if cur_digit < 5:
                # Normal case: don't have to worry about digits
                checksum += cur_digit * 2
            else:
                # Number is >= 5, so we must subtract 9 to get the sum of the digits
                checksum += (cur_digit * 2 - 9)

        else:
            checksum += cur_digit

        # Keep track of first two digits
        first_two_digits = cur_digit * 10 + (first_two_digits // 10)

        # Update state and drop last digit
        mult_by_two = not mult_by_two
        cc_no = cc_no // 10
        cc_no_length += 1

    # Validade checksum, first two digits, and the length
    if checksum % 10 != 0:
        print('INVALID')
    elif cc_no_length == AMEX_LENGTH and (first_two_digits == AMEX_1 or first_two_digits == AMEX_2):
        print('AMEX')
    elif first_two_digits >= FIRST_VISA and first_two_digits <= LAST_VISA and (cc_no_length == VISA_LENGTH1 or cc_no_length == VISA_LENGTH2):
        print('VISA')
    elif first_two_digits >= FIRST_MC and first_two_digits <= LAST_MC and cc_no_length == MC_LENGTH:
        print('MASTERCARD')
    else:
        print('INVALID')


if __name__ == "__main__":
    main()
