"""HW 8: XOR Encoder
Kim Huynh, 2026-05-18, CS 211
"""

def xor_encrypt(plaintext, key):
    """
    Encrypts or decrypts a string using XOR.

    Each character in the plaintext is XORed
    with a character from the key. If the key
    is shorter than the plaintext, the key
    repeats cyclically.

    Parameters:
        plaintext: the message to encrypt or decrypt
        key: the secret key used for XOR encryption

    Returns:
        The encrypted or decrypted string.
    """

    result = ""

    # loop through every character in the plaintext
    for i in range(len(plaintext)):

        # current character from plaintext
        p_char = plaintext[i]

        # cycle through key using modulo operator
        k_char = key[i % len(key)]

        # XOR the ASCII/Unicode values
        xor_value = ord(p_char) ^ ord(k_char)

        # convert back into a character
        result += chr(xor_value)

    return result


if __name__ == "__main__":

    plaintext = "This is a secret message!"

    print("Plaintext:")
    print(plaintext)

    key = "beautifulIsBetterThanUgly"   # Python's Zen

    # encrypt the plaintext
    ciphertext = xor_encrypt(plaintext, key)

    print("Ciphertext:")
    print(ciphertext)

    # decrypt using the same function and key
    decrypted_text = xor_encrypt(ciphertext, key)

    print("Decrypted text:")
    print(decrypted_text)

    # verify encryption/decryption worked
    if plaintext == decrypted_text:
        print("Encryption and decryption successful!")
    else:
        print("Error: Decryption failed!")