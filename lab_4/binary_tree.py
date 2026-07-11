"""Lab 4: Binary Trees
Kim Huynh, 2026-04-22, CS 211
"""

# 2.1 Class Node
class Node:
    def __init__(self, node_data: int):
        # Store the integer value in this node
        self.node_data = node_data

    def __str__(self):
        raise NotImplementedError("__str__ must be implemented by subclasses")

    def sum_node_data(self):
        raise NotImplementedError("sum_node_data must be implemented by subclasses")

# 2.2 Classes Internal and Leaf
class Leaf(Node):
    def __init__(self, node_data: int):
        # A Leaf only stores its own data
        super().__init__(node_data)

    # 2.3 Sum Subtree Data
    def sum_node_data(self):
        # Base case of the recursion:
        # a leaf has no children, so its sum is just its own value
        return self.node_data

    # 2.5 Recursive str
    def __str__(self):
        # A leaf prints as just its data
        return str(self.node_data)

class Internal(Node):
    def __init__(self, node_data: int, left: Node, right: Node):
        # An Internal node has data plus a left and right child
        super().__init__(node_data)
        self.left = left
        self.right = right

    # 2.5 Recursive str
    def __str__(self):
        # Recursive tree representation: <data, left, right>
        return f"<{self.node_data}, {self.left}, {self.right}>"

    # 2.3 Sum Subtree Data
    def sum_node_data(self):
        # Recursive case:
        # add this node's value to the sums of the left and right subtrees
        return self.node_data + self.left.sum_node_data() + self.right.sum_node_data()

# 2.4 Main
def main():
    l1 = Leaf(3)
    l2 = Leaf(6)
    l3 = Leaf(9)
    i = Internal(7, l2, l3)
    root = Internal(5, l1, i)

    print(root.sum_node_data())     # 30
    print(root)                     # <5, 3, <7, 6, 9>>

if __name__ == '__main__':
    main()