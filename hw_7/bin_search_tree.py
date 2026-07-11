"""Homework 7: BST Find Min and Max
Kim Huynh, 2026-05-11, CS 211

Implements a Binary Search Tree to find
the minimum and maximum values.
"""

# credits: slides from class


class Tree:
    def __init__(self):
        self.root = None

    def find_min(self):
        """
        Finds the minimum value in the binary search tree.
        Returns:
        The node with the minimum value.
        """
        if self.root is None:
            return None

        # delegate work to Node method
        return self.root.find_min()

    def find_max(self):
        """
        Finds the maximum value in the binary search tree.
        Returns:
        The node with the maximum value.
        """
        if self.root is None:
            return None

        # delegate work to Node method
        return self.root.find_max()


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def find_min(self):
        """
        Recursively finds the minimum value in the subtree 
        rooted at the current node.
        Returns:
        The node with the minimum value.
        """
        # minimum is always the leftmost node
        if self.left is None:
            return self
        return self.left.find_min()

    def find_max(self):
        """
        Recursively finds the maximum value in the subtree rooted 
        at the current node.
        Returns:
        The node with the maximum value.
        """
        # maximum is always the rightmost node
        if self.right is None:
            return self
        return self.right.find_max()


if __name__ == "__main__":

    # create nodes manually for testing
    tree = Tree()

    tree.root = Node(50)
    tree.root.left = Node(30)
    tree.root.right = Node(70)

    tree.root.left.left = Node(20)
    tree.root.left.right = Node(40)

    tree.root.right.left = Node(60)
    tree.root.right.right = Node(80)

    # find minimum and maximum
    min_node = tree.find_min()
    max_node = tree.find_max()

    print("Minimum value:", min_node.value)
    print("Maximum value:", max_node.value)


# notes:
# Tree uses delegation:
# -> Tree asks the root Node to do the recursive work
# Node handles the actual recursion:
# -> move left to find minimum
# -> move right to find maximum
# BST property:
# -> smallest value = farthest left node
# -> largest value = farthest right node