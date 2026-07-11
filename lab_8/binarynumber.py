"""Lab 8: Binary Number Class
Kim Huynh, 2026-05-20, CS 211
"""

from typing import List

class BinaryNumber:

    def __init__(self, bits: List[int]):
        assert all(bit == 0 or bit == 1 for bit in bits)
        self.bits = bits

    def __str__(self):
        return f"0b{self.bits}"

    def __or__(self, other):
        assert len(self.bits) == len(other.bits)

        bitArray = []
        for i in range(len(self.bits)):
            bitArray.append(self.bits[i] | other.bits[i])

        return BinaryNumber(bitArray)

    def __and__(self, other):
        assert len(self.bits) == len(other.bits)

        bitArray = []
        for i in range(len(self.bits)):
            bitArray.append(self.bits[i] & other.bits[i])

        return BinaryNumber(bitArray)

    def left_shift(self):
        self.bits = self.bits[1:] + [0]

    def right_shift(self):
        self.bits = [0] + self.bits[:-1]

    def extract(self, start: int, end: int):
        assert 0 <= start < end
        assert start < end <= len(self.bits)

        maskBits = [0 for _ in range(len(self.bits))]

        left = len(self.bits) - end
        right = len(self.bits) - 1 - start

        for i in range(left, right + 1):
            maskBits[i] = 1

        mask = BinaryNumber(maskBits)
        value = self & mask

        for _ in range(start):
            value.right_shift()

        return value


if __name__ == "__main__":
    # execute and verify

    bn = BinaryNumber([1, 0, 1, 0, 1])
    bn2 = BinaryNumber([1, 1, 1, 0, 0])
    print("1st binary number =", bn)

    print("2nd binary number =", bn2)

    print("AND", bn & bn2)
    print("OR", bn | bn2)

    bn.right_shift()
    print("1st number right-shifted =", bn)

    bn.left_shift()
    print("1st number left-shifted =", bn)

    bn = BinaryNumber([1, 0, 0, 1, 0, 1, 1, 1])
    extracted = bn.extract(2, 4)
    print(extracted)