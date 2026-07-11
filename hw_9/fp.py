"""HW 9: Data Transformation with Functional Programming
Kim Huynh, 2026-05-26, CS 211
"""

from functools import reduce

# initial data
data = [1, 5, 8, 12, 15, 20, 23, 28, 30, 35, 40]

# 1. pure predicate function
def is_divisible_by_four(number):
    """
    Returns True if the number is perfectly divisible
    by 4, and False otherwise.
    """
    return number % 4 == 0

# 2. pure transformation function
def half_value(number):
    """
    Returns half of the given number. 
    """
    return number / 2

# 3. filter the data
filtered_data = list(filter(is_divisible_by_four, data))

# 4. transform the data
transformed_data = list(map(half_value, filtered_data))

# 5. aggregate the data
final_sum = reduce(lambda x, y: x + y, transformed_data)

# 6. print results
print("Filtered Data:", filtered_data)
print("Transformed Data:", transformed_data)
print("Final Sum:", final_sum)

# 7. reflection
    # Q - Briefly explain how your solution demonstrates the 
    #     principles of pure functions and immutability.
    # A - This program demonstrates functional programming 
    #     principles by using pure functions and higher-order 
    #     functions to process data without modifying the original 
    #     list. The functions, is_divisible_by_four() and half_value(), 
    #     are pure because they always produce the same output for 
    #     the same input and have no side effects. The program also 
    #     demonstrates immutability because the original data list 
    #     remains unchanged throughout execution. Instead of altering 
    #     existing data, filter() creates a new list containing only 
    #     numbers divisible by four, map() creates another new list 
    #     with transformed values, and reduce() combines the 
    #     transformed data into a single result. This declarative 
    #     approach focuses on what to compute rather than how to 
    #     compute it.