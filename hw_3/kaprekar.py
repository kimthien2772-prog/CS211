"""HW 3: Kaprekar Constant
Kim Huynh, 2026-04-18, CS 211
"""

class Kaprekar:
    kaprekar_constant = 6174 # a class variable or member

    def __init__(self, number):
        # instance members
        self.number = int(number)
        self.digits = list(f"{self.number:04d}")

    def __str__(self):
        return f"Kaprekar(number={self.number:04d})"

    def __repr__(self):
        return f"Kaprekar({self.number})"

    def set_number(self, number):
        self.number = int(number)
        self.digits = list(f"{self.number:04d}")

    def is_kaprekar(self):
        return self.number == Kaprekar.kaprekar_constant

    def largest(self):
        # returns largest integer from digits
        descending_digits = sorted(self.digits, reverse = True)
        return int("".join(descending_digits))

    def smallest(self):
        # returns smallest integer from digits
        ascending_digits = sorted(self.digits)
        return int("".join(ascending_digits))

    def step(self):
        # produces one step in the Kaprekar process
        # largest number from digits - smallest number from digits
        big = self.largest()
        small = self.smallest()
        result = big - small
        
        self.set_number(result)

        return result

    def kaprekar_steps(self):
        # returns number of steps to reach Kaprekar constant
        # stop at 100 to avoid an infinite loop
        count = 0

        while not self.is_kaprekar() and count < 100:
            self.step()
            count += 1

        return count

if __name__ == "__main__":
    print(f"Kaprekar constant: {Kaprekar.kaprekar_constant}")
    n = input("Enter a 4-digit number: ")

    if len(n) != 4 or not n.isdigit():
        print("Please enter a valid 4-digit number.")
        exit(1)

    k = Kaprekar(int(n))
    print(k)

    print(f"Number of steps to reach Kaprekar constant: {k.kaprekar_steps()}")
    print(f"Is Kaprekar constant: {k.is_kaprekar()}")

    # Tests:
    # 5200 -> 7
    # 1234 -> 3
    # 8894 -> 6
    # 5757 -> 6
    # 1111 -> 100
    # 6174 -> 0