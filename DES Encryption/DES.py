"""
Jason Ketterer

Implements the DES symmetric encryption security algorithm.

The program in this file is the individual work of Jason Ketterer.
"""

import random

IP = (58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7)

IP_1 = (40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25)

E = (32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1)

PC_2 = (14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32)

P = (16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25)

Sboxes = {0: [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
              [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
              [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
              [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

          1: [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
              [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
              [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
              [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

          2: [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
              [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
              [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
              [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

          3: [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
              [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
              [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
              [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

          4: [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
              [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
              [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
              [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

          5: [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
              [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
              [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
              [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

          6: [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
              [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
              [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
              [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

          7: [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
              [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
              [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
              [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]}


'''Divide text into 8 character (64 bit) blocks and then construct a
64 bit integer.  Pads with 0's if text is not a multiple of 8 characters'''
def generate_blocks(text):

    # calculate number of blocks and padding needed
    num_blocks, padding = divmod(len(text), 8)

    # generate substring blocks of 8 chars
    blocks = [text[i * 8:i * 8 + 8] for i in range(0, num_blocks)]

    if padding:
        blocks.append(text[num_blocks * 8:].ljust(8, '0'))

    # convert each block to 64-bit int
    blocks_64bitints = []
    for blk in blocks:
        b = 0
        for i in range(0, len(blk)):
            b = b << 8 | ord(blk[i])
        blocks_64bitints.append(b)

    return blocks_64bitints

'''Converts 64 bit number n to string'''
def convertToStr(n):

    n_bitstr = "{0:0>64b}".format(n)
    n_int_list = [int(n_bitstr[i * 8:i * 8 + 8], 2) for i in range(0, 8)]
    n_str = ""
    for i in n_int_list:
        n_str += chr(i)

    return n_str

'''Cyclic left shift by 1 bit.  Assumes 56-bit key.
Converts the key to the string, performs the cyclic left
shift, and then converts the string back to an int because
the goddamn fucking bit shift operator kept adding an extra bit
every iteration for some reason i couldn't figure out.
Was trying to just simply do "key << 1 | key >> 55"'''
def cyclicLeftShift(key):

    key_str = "{0:0>56b}".format(key)
    k = [c for c in key_str]
    t = k.pop(0)
    k.append(t)
    key_str = ""
    for c in k:
        key_str += c
    # n_str = "{0:0>56b}".format(key_str)
    n = int(key_str,2)
    return n

'''Returns a 48-bit subkey from a 56-bit key'''
def applyPC2(key):

    key_str = "{0:0>56b}".format(key)
    round_key = [key_str[PC_2[i]-1] for i in range(0,48)]
    rk = int("".join(round_key),2)
    return rk

'''Generate 16 round keys to use with one iteration of DES'''
def generate_round_keys(key):

    round_keys = []
    for i in range(0,16):
        key_left_shifted = cyclicLeftShift(key)
        key = key_left_shifted  # prepare for next round
        rk = applyPC2(key_left_shifted)
        round_keys.append(rk)
    return round_keys

'''Perform permutation on an n-bit block using table'''
def permutation(block, n, table):

    formatter = "{0:0>" + str(n) + "b}"
    block_str = formatter.format(block)
    permuted_block = [block_str[table[i]-1] for i in range(0,len(table))]
    return int("".join(permuted_block),2)

def split_number(n):

    return n >> 32, n & (2**32 - 1)

def applySBox(R_block):

    # split block into 8 blocks of 6 bits
    ri = "{0:0>48b}".format(R_block)
    Ri = [ri[6 * i:6 * i + 6] for i in range(0, 8)]

    # apply Sboxes to generate 4 bit strings
    substitutions = []
    for i, blk in enumerate(Ri):
        row = int(blk[0] + blk[5], 2)
        col = int(blk[1:5], 2)
        substitutions.append(Sboxes[i][row][col])

    # concatenate all the substring substitutions
    Ri = ""
    for s in substitutions:
        Ri += "{0:0>4b}".format(s)
    Ri = int(Ri, 2)

    return Ri

def round_function(block, round_keys, decrypt):

    for i in range(0,16):

        # split block into 32 bit halves
        L_half, R_half = split_number(block)

        # left half for next round is the right half
        L_next = R_half

        # apply expansion permutation to right half to make it 48 bits
        R_expanded = permutation(R_half, 32, E)

        # xor with round key
        R_expanded ^= round_keys[i]

        # use S-Box to shrink right half back to 32 bits
        R_half = applySBox(R_expanded)

        # perform intermediary permutation
        R_half = permutation(R_half, 32, P)

        # xor with left half
        R_half = L_half ^ R_half

        # concatenate (next) L_half with R_half
        block = L_next << 32 | R_half

    # 32-bit swap
    L_half, R_half = split_number(block)
    block = R_half << 32 | L_half


    return block


def DES(msg, keys):

    # initial permutation of text
    block = permutation(msg, 64, IP)

    # apply 16 iterations of round function
    block = round_function(block, keys, decrypt)

    # final permutation
    block = permutation(block, 64, IP_1)

    return block

def encrypt(plain_text, key):

    blocks = generate_blocks(plain_text)
    round_keys = generate_round_keys(key)

    cipher_text = ""
    for b in blocks:
        n = DES(b, round_keys)
        cipher_text += convertToStr(n)

    return cipher_text

def decrypt(cipher_text, key):

    blocks = generate_blocks(cipher_text)
    round_keys = generate_round_keys(key)
    round_keys.reverse()

    plain_text = ""
    for b in blocks:
        n = DES(b, round_keys)
        plain_text += convertToStr(n)

    plain_text = plain_text.rstrip('0')

    return plain_text

def main():

    random.seed() # seeds with system time by default

    print("DES Implementation:")
    plain_text = input("Enter text to encrypt (\"Exit\" to quit): ")

    while not (plain_text == "Exit" or plain_text == "exit"):

        key = random.getrandbits(56)

        cipher_text = encrypt(plain_text, key)
        plain_text = decrypt(cipher_text, key)

        print("Encrypted text:\t \'{}\'".format(cipher_text))
        print("Decrypted text:\t \'{}\'".format(plain_text))

        plain_text = input("Next text (\"Exit\" to quit): ")

if __name__ == "__main__":
    main()
