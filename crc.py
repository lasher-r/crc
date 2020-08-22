from random import randrange


def crc(string_int, v=False):
    polynomial_int = int("11021", 16)
    if v:
        print(bin(string_int))

    crc_remainder = string_int << 16

    while crc_remainder.bit_length() > 16:

        crc_remainder_len = crc_remainder.bit_length()

        # shift so that the polynomial is aligned with the
        # left of the message.

        # note that the bit length of crc_remainder grows smaller with each iteration
        # this has the affect of shifting the polynomial right even though we're
        # left shifting here.
        polynomial_int_shifted = polynomial_int << (
            crc_remainder_len - polynomial_int.bit_length())
        if v:
            print(bin(polynomial_int_shifted))
            print('-' * (crc_remainder_len + 2))

        # Python automatically trims leading 0s so we don't have to test that
        # the polynomial is aligned w/ a 1

        # xor the result of the last iteration with the shifted
        # polynomial. xor matches subtraction for the Galois field of two elements, GF(2).
        # this shifting and subtracting is essentially long devision.  See note below.
        crc_remainder = crc_remainder ^ polynomial_int_shifted
        if v:
            print("flip bits at polynomial 1's")
            print('-' * (crc_remainder_len + 2))
            print(bin(crc_remainder))
    return crc_remainder


if __name__ == "__main__":
    # string we're trying to send
    string = "Hello, world! this is a longer message"

    # convert the string to an int
    # Calc the crc and append it to the message
    string_int = int.from_bytes(string.encode(), "big")
    crc_sent = crc(string_int)
    message = (string_int << 16) | crc_sent

    # show the complete message as binary
    print(bin(message))

    # imagine now that message is sent over a wire

    # message is if their is no corrupted data
    # corrupted will randomly corrupt the data
    corrupted = message | randrange(message)
    print(bin(corrupted))

    # calculate the crc for the received data
    crc_received = crc(message)

    # if the crc is 0 the message is not corrupted
    # convert the message to an ascii string (ignoring the last two [crc] bytes)
    if crc_received == 0:
        bin_array = message.to_bytes(
            (message.bit_length() + 7) // 8, "big")[:-2]
        print(bin_array.decode())
    else:
        print("message corrupted")

    # calculate the crc for the received data
    crc_received_corrupted = crc(corrupted)

    # if the crc is 0 the message is not corrupted
    # convert the message to an ascii string (ignoring the last two [crc] bytes)
    bin_array_c = corrupted.to_bytes(
        (corrupted.bit_length() + 7) // 8, "big")[:-2]
    print(bin_array_c.decode())


'''


long devision with GF(2):

this example uses a 3rd degree polynomial, we use a 16th degree polynomial.

11010011101100 000 <--- input right padded by 3 bits
1011               <--- divisor
01100011101100 000 <--- result (note the first four bits are the XOR with the divisor beneath, the rest of the bits are unchanged)
 1011              <--- divisor ...
00111011101100 000
  1011
00010111101100 000
   1011
00000001101100 000 <--- note that the divisor moves over to align with the next 1 in the dividend (since quotient for that step was zero)
       1011             (in other words, it doesn't necessarily move one bit per iteration)
00000000110100 000
        1011
00000000011000 000
         1011
00000000001110 000
          1011
00000000000101 000
           101 1
-----------------
00000000000000 100 <--- remainder (3 bits).  Division algorithm stops here as dividend is equal to zero.
'''

'''
"polynomial"

for the division operation to work it isn't being done on the value of the binary.
Instead the binary is represented as a polynomial where each term is Value*X^(place)

i.e. 
the value of 'h', 01001000, is   0*2^7 + 1*2^6 + 0*2^5 + 0*2^4 + 1*2^3 + 0*2^2 + 0*2^1 + 0*2^0 or 72
the polynomial representation is 0*X^7 + 1*X^6 + 0*X^5 + 0*X^4 + 1*X^3 + 0*X^2 + 0*X^1 + 0*X^0 
which we write as '01001000' which is handy because it's just the binary representation of the number.

x^6 + x^2
      X^2

X^6
1000000

Using the polynomial allows us to add (and importantly, subtract) terms w/o carrying.
'''

'''
0x11021

This is just a well known, common CRC polynomial that you get off a list.

'''
