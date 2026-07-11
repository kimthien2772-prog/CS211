"""HW 6: Recursive Objects - Lists
Kim Huynh, 2026-05-06, CS 211
"""

"""
This module implements a simple singly linked list data structure.

Classes:
    List:
        Represents a singly linked list 
        Operations: adding, removing, finding elements, and converting the list to a string.

    ListNode:
        Represents a node in the singly linked list, 
        contains data and a reference to the next node.

Usage:
    The `List` class provides methods to manipulate the linked list:
        - `add_list(data)`: Adds a new element to the front of the list.
        - `remove_list()`: Removes the first element from the list and returns its data.
        - `find(data)`: Checks if a specific element exists in the list.
        - `__str__()`: Returns a string representation of the list.
"""


class List:
    """
    A simple implementation of a singly linked list.
    """

    def __init__(self):
        """
        Initializes a new instance of the class.
        Attributes:
            first: An attribute initialized to None
                   represents the head of the list.
        """
        self.first = None

    def add_list(self, data):
        """
        Adds a new node with the given data to the beginning of the list.
        Args:
            data: The data to be stored in the new node.
        """
        next = self.first                   # old head becomes the tail
        new_node = ListNode(data, next)     
        self.first = new_node               # update head to new node

    def remove_list(self):
        """
        Removes the first element from the list and updates the head of the list
        to the next element.
        Returns:
            The data of the removed element if the list is not empty, otherwise None.
        """
        current = self.first
        second = self.first.next if self.first else None
        self.first = second
        return current.data if current else None

    def __str__(self):
        """
        Returns a string representation of the linked list.
        Returns:
            str: A string representation of the linked list.
        """
        current = self.first
        result = ""
        while current:
            result += f"{current.data}"
            current = current.next
            result += " -> " if current else ""
        return result if result else "empty list"

    def find(self, data):
        """
        Searches for a node containing the specified data in the linked list.
        Args:
            data: The value to search for in the linked list.
        Returns:
            bool: True if a node with the specified data is found, False otherwise.
        """
        if self.first is None:
            return False

        # start recursive search at the head node
        return self.first.find(data)


class ListNode:
    """
    A class representing a node in a singly linked list.

    Attributes:
        data (any): The data stored in the node.
        next (ListNode or None): A reference to the next node in the list, or None if this is the last node.
    """

    def __init__(self, data, next_node):
        """
        Initializes a ListNode instance.

        Args:
            data (any): The data to store in the node.
            next_node (ListNode or None): The next node in the list, or None if this is the last node.
        """
        self.data = data
        self.next = next_node

    def __str__(self):
        """
        Returns a string representation of the object's data.
        Returns:
            str: A string representation of the `data` attribute.
        """
        return str(self.data)

    def __repr__(self):
        """
        Provide a string representation of the object.
        Returns:
            str: A string representation of the object's data.
        """
        return str(self.data)

    def find(self, data):
        """
        Searches for a node containing the specified data in the linked list.
        Args:
            data: The value to search for in the linked list.
        Returns:
            bool: True if a node with the specified data is found, False otherwise.
        """
        # base case: 
        # if head contains the data, return True
        if self.data == data:
            return True
        
        # base case:
        # if there is no tail left to search, the data is not in the list
        if self.next is None:
            return False
        
        # recursive call:
        # search the tail of the list
        return self.next.find(data)


if __name__ == "__main__":
    my_list = List()
    print(my_list)  # output: empty list

    my_list.add_list(1)
    my_list.add_list(2)
    my_list.add_list(3)

    print(my_list)  # output: 3 -> 2 -> 1

    removed = my_list.remove_list()
    print(f"Removed: {removed}")  # output: Removed: 3

    print(my_list)  # output: 2 -> 1

    print(f"find(2): {my_list.find(2)}")  # output: find(2): True
    print(f"find(3): {my_list.find(3)}")  # output: find(3): False

    my_list.remove_list()
    print(my_list)  # output: 1

    my_list.remove_list()
    print(my_list)  # output: empty list

    my_list.remove_list()
    print(my_list)  # output: empty list