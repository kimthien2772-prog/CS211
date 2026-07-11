"""Lab 9: Functions As Arguments
Kim Huynh, 2026-05-27, CS 211
"""

import math
from typing import List, Callable

def total_sum(list1: List[int]):
    return sum(list1)


def apply(fun: Callable, list1: List[int]):
    return [fun(i) for i in list1]


def square(list1: List[int]):
    return apply(lambda x: x ** 2, list1)


def magnitude(vector: List[int]):
    squared_values = square(vector)
    return math.sqrt(total_sum(squared_values))


class FunctionDispatcher:

    def __init__(self, dispatch_table: dict):
        self.dispatch_table = dispatch_table

    def process_command(self, key: int, list1: List[int]):
        function = self.dispatch_table[key]
        return function(list1)


if __name__ == '__main__':
    dispatch_table = {
        # complete the dispatch dictionary
        1: total_sum,
        2: square,
        3: magnitude
    }

    fd = FunctionDispatcher(dispatch_table)

    print(fd.process_command(1, [3, 4]))
    print(fd.process_command(2, [3, 4]))
    print(fd.process_command(3, [3, 4]))