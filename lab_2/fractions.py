"""Lab 2: Fractions
Kim Huynh, 2026-04-08, CS 211
"""

import math

# GCD (Euclidean alogrithm)
def gcd(a, b):
    if b == 0:
        return a
    if a == 0:
        return b

    if a > b: 
        return gcd(b, a)
    return gcd(b - a, a)

class Fraction:
# 2.2 Class Constructor
    def __init__(self, num, den: int):
        assert isinstance(num, int) and isinstance(den, int)
        assert num >= 0 and den > 0

        self.num = num
        self.den = den
        self.simplify()

# 2.3 String Representation Methods
#__str__ num/den
#__repr__ Fraction(num,den)

    def __str__(self) -> str:
        return f"{self.num}/{self.den}"

    def __repr__(self) -> str:
        return f"Fraction({self.num}, {self.den})"

# if __name__ == "__main__":
    # if = Fraction(3,5)
    # print(f"f = {f}")

    # prints f = 3/5

# 3. Multiply and Add Magic Methods
    def __add__(self, other):
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Fraction(new_num, new_den)

    def __mul__(self, other):
        new_num = self.num * other.num
        new_den = self.den * other.den

# 4. Fraction Simplification
    def simplify(self):
        divisor = gcd(self.num, self.den)

        if divisor != 0:
            self.num = self.num // divisor
            self.den = self.den // divisor


if __name__ == "__main__":  
    f1 = Fraction(3, 5)
    f2 = Fraction(1, 2)

    print(f"{f1} + {f2} = {f1 + f2}")   # 3/5 + 1/2 = 11/10
    print(f"{f1} * {f2} = {f1 * f2}")   # 3/5 * 1/2 = 3/10  
    
    f = Fraction(6, 10)
    print(f)                            # simplifies 6/10 to 3/5