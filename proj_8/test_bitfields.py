"""Project 8: Bit Field Packing and Unpacking
Kim Huynh, 2026-05-21, CS 211

Tests for bitfield.py
"""

import unittest
from bitfield import BitField


class TestBitFields(unittest.TestCase):

    def test_low_order(self):
        low_4 = BitField(0, 3)
        # A value that fits snugly in the first 4 bits
        self.assertEqual(low_4.insert(13, 0), 13)
        # A value that doesn't fit; some high bits lost
        self.assertEqual(low_4.insert(21, 0), 5)
        # Extract unsigned
        self.assertEqual(low_4.extract(15), 15)
        # Or convert negative numbers
        self.assertEqual(low_4.extract_signed(15), -1)
        # Doesn't clobber other bits
        higher = 15 << 4
        self.assertEqual(low_4.insert(13, higher), 13 + higher)
        # Extraction is masked
        packed = low_4.insert(13, higher)
        self.assertEqual(low_4.extract(packed), 13)

    def test_middle_bits(self):
        mid_4 = BitField(4, 7)
        # A value that fits snugly in4 bits
        self.assertEqual(mid_4.insert(13, 0), 13 << 4)
        # A value that doesn't fit; some high bits lost
        self.assertEqual(mid_4.insert(21, 0), 5 << 4)
        # Extract unsigned
        self.assertEqual(mid_4.extract(15 << 4), 15)
        # Or convert negative numbers
        self.assertEqual(mid_4.extract_signed(15 << 4), -1)

    def test_invert(self):
        lowpart = BitField(0, 3)
        midpart = BitField(4, 6)
        highpart = BitField(7, 9)
        for v in range(8):
            packed = 0
            packed = lowpart.insert(v, packed)
            packed = midpart.insert(v, packed)
            packed = highpart.insert(v, packed)
            self.assertEqual(lowpart.extract(packed), v)
            self.assertEqual(midpart.extract(packed), v)
            self.assertEqual(highpart.extract(packed), v)

    def test_replace(self):
        """Test replacing an existing field of bits."""
        packed = 0x0f0  # 11110000  --- we want to clobber those ones
        newval = 0x005  # 00000101  --- and replaced them with 0101
        field = BitField(4, 7)  # ____xxxx  --- in positions 4..7
        packed = field.insert(newval, packed)
        self.assertEqual(packed, 0x50)  # 01010000 --- some zeros replaced 1s
        # Note 0x50 == 0b01010000 == 80

    def test_width(self):
        """Make sure we are masking out any bits that don't fit in 
        the field. 
        """
        second_nibble = BitField(4, 7)
        value = 0xff  # A full byte; two nibbles
        packed = second_nibble.insert(value, 0)
        self.assertEqual(packed, 0xf0)
        # Note 0xf0 == 240


class TestAdditionalBitFields(unittest.TestCase):

    def test_single_bit_field(self):
        """Test inserting and extracting a one-bit field."""
        bit = BitField(5, 5)

        packed = bit.insert(1, 0)
        self.assertEqual(packed, 0b100000)
        self.assertEqual(bit.extract(packed), 1)

        packed = bit.insert(0, packed)
        self.assertEqual(packed, 0)
        self.assertEqual(bit.extract(packed), 0)

    def test_insert_does_not_change_other_bits(self):
        """Replacing one field should preserve bits outside the field."""
        field = BitField(8, 11)

        word = 0xffff
        packed = field.insert(0, word)

        self.assertEqual(field.extract(packed), 0)
        self.assertEqual(packed, 0xf0ff)

    def test_extract_from_high_bits(self):
        """Test extraction from bits near the top of a 32-bit word."""
        high = BitField(28, 31)

        word = 0xf0000000
        self.assertEqual(high.extract(word), 0xf)

    def test_insert_into_high_bits(self):
        """Test inserting into bits near the top of a 32-bit word."""
        high = BitField(28, 31)

        packed = high.insert(0xa, 0)
        self.assertEqual(packed, 0xa0000000)
        self.assertEqual(high.extract(packed), 0xa)

    def test_signed_positive_high_bit_zero(self):
        """A signed field with high bit 0 should stay positive."""
        field = BitField(4, 7)

        packed = field.insert(0b0110, 0)
        self.assertEqual(field.extract_signed(packed), 6)

    def test_signed_negative_not_all_ones(self):
        """A signed field with high bit 1 should become negative."""
        field = BitField(4, 7)

        packed = field.insert(0b1011, 0)
        self.assertEqual(field.extract_signed(packed), -5)

    def test_negative_insert_and_signed_extract(self):
        """Negative values should insert correctly when masked."""
        field = BitField(8, 11)

        packed = field.insert(-3, 0)
        self.assertEqual(field.extract(packed), 0b1101)
        self.assertEqual(field.extract_signed(packed), -3)

    def test_multiple_non_overlapping_fields(self):
        """Different bitfields should not interfere with each other."""
        low = BitField(0, 3)
        mid = BitField(4, 7)
        high = BitField(8, 11)

        packed = 0
        packed = low.insert(0b0011, packed)
        packed = mid.insert(0b1010, packed)
        packed = high.insert(0b0101, packed)

        self.assertEqual(low.extract(packed), 0b0011)
        self.assertEqual(mid.extract(packed), 0b1010)
        self.assertEqual(high.extract(packed), 0b0101)

# class TestSignExtension(unittest.TestCase):
#     """Testing the sign extension function.  If you move sign extension into
#     the BitFields class, you may want to remove this test class.
#     """

#     def test_extend_neg(self):
#         """0b111 in a 3-bit field is negative 1"""
#         self.assertEqual(bitfield.sign_extend(7, 3), -1)

#     def test_extend_pos(self):
#         """0b0111 in a 4-bit field is positive 7"""
#         self.assertEqual(bitfield.sign_extend(7, 4), 7)

#     def test_not_all_neg(self):
#         """For good measure, make sure it works for an integer that
#         is not all 1s.
#         """
#         self.assertEqual(bitfield.sign_extend(11, 4), -5)
#         self.assertEqual(bitfield.sign_extend(11, 5), 11)
#         self.assertEqual(bitfield.sign_extend(13, 4), -3)
#         self.assertEqual(bitfield.sign_extend(13, 5), 13)


if __name__ == '__main__':
    unittest.main()