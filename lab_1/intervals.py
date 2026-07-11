"""Closed intervals of integers
Kim Huynh, 2026-04-01, CS 211
"""
# add to beginning of all assignments from now on

class Interval:
    """An interval [m..n] represents the set of integers
    from m to n."""

# 3.3 Class Constructor

    def __init__(self, low: int, high: int):
        # no matter what function you are writing in this course, 
        # always add "self" at the beginning
        """Interval(low,high) represents the
        interval [low..high]"""
        # if low > high:
        #   raise ValueError("Low should not be greater than high")
        assert high >= low, "Low should not be greater than high"
        self.low = low
        self.high = high

# 3.4 A Membership Method

    def contains(self, i: int) -> bool:
        """Integer i is within the closed interval"""
        return self.low <= i <= self.high

# 3.5 Overlapping ntervals?

    def overlaps(self, other: "Interval") -> bool:
        """i.overlaps(j) iff i and j have some elements in common"""
        return not (self.high < other.low or other.high < self.low)

# 3.6 Magic Methods

    def __eq__(self, other: "Interval") -> bool:
        """Intervals are equal if they have the same 
        low and high bounds"""
        return self.low == other.low and self.high == other.high

# 3.7 Joining Intervals

    def join(self, other: "Interval") -> "Interval":
        """Create a new Interval that contains the union of
        elements in self and other.
        Precondition: self and other must overlap.
        """
        assert self.overlaps(other)
        return Interval(min(self.low, other.low), max(self.high, other.high))

# 3.8 Prettier Intervals

    def __str__(self):
        return f"[{self.low}..{self.high}]"

    def __repr__(self):
        return f"Interval({self.low}, {self.high})"

# use instead of calling function globally from now on
if __name__ == "__main__":
    i = Interval(2, 6)
    j = Interval(0, 8)
    k = Interval(5, 7)
    m = Interval(7, 9)

    # contains tests
    print(i.contains(2))   # True  (2 is in [2..6])
    print(i.contains(4))   # True  (4 is in [2..6])
    print(i.contains(7))   # False (7 is outside)

    # overlaps tests
    print(i.overlaps(j))   # True  ([2..6] overlaps [0..8])
    print(i.overlaps(k))   # True  ([2..6] overlaps [5..7])
    print(i.overlaps(m))   # False ([2..6] does not overlap [7..9])

    # equality tests
    print(i == Interval(2, 6))  # True
    print(i == Interval(1, 3))  # False

    # join tests
    print(i.join(j))   # [0..8]
    print(i.join(k))   # [2..7]