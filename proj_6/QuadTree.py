"""Project 6: Quad Trees
Kim Huynh, 2026-05-06, CS 211

Class designed to represent an image as a Quad Tree.
"""

from binary_matrix import *
from math import inf as infinity

# 3.1 the QuadTree class constructor
class QuadTree:

    def __init__(self) -> None:
        """
        Initializes a new QuadTree node with default values.
        """
        self.depth = 0
        self.mean = 0
        self.size = (0, 0)

        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None

    # 3.2 the insert method
    def insert(self, bin_mat, depth=0):
        """
        Recursively inserts a binary matrix into the QuadTree, splitting it into quadrants
        if the matrix contains mixed bits.
        """
        self.depth = depth
        self.mean = matrix_mean(bin_mat)
        self.size = (len(bin_mat), len(bin_mat[0]))

        if same_bits(bin_mat):
            return

        nw, ne, se, sw = split_4(bin_mat)

        self.nw = QuadTree()
        self.ne = QuadTree()
        self.se = QuadTree()
        self.sw = QuadTree()

        self.nw.insert(nw, depth + 1)
        self.ne.insert(ne, depth + 1)
        self.se.insert(se, depth + 1)
        self.sw.insert(sw, depth + 1)

    # 3.4 image reconstruction
    def reconstruct_image(self, depth):
        """
        Reconstructs the binary matrix from the QuadTree up to a specified depth.
        """
        if self.nw is None or self.depth == depth:
            value = round(self.mean)

            matrix = []

            for i in range(self.size[0]):
                row = []

                for j in range(self.size[1]):
                    row.append(value)

                matrix.append(row)

            return matrix

        nw_matrix = self.nw.reconstruct_image(depth)
        ne_matrix = self.ne.reconstruct_image(depth)
        se_matrix = self.se.reconstruct_image(depth)
        sw_matrix = self.sw.reconstruct_image(depth)

        return stitch_matrices(nw_matrix, ne_matrix, se_matrix, sw_matrix)

    # 3.3 string representation
    def __str__(self):
        """
        Returns a string representation of the QuadTree, including its depth, mean, size,
        and child nodes.
        """
        result = ""

        result += "+" * self.depth
        result += f" (({self.depth}, {self.mean}, {self.size}))"

        if self.nw is not None:
            result += "\n" + str(self.nw)
            result += "\n" + str(self.ne)
            result += "\n" + str(self.se)
            result += "\n" + str(self.sw)

        return result


if __name__ == "__main__":
    binary_file = 'fisherman.txt'
    matrix = read_bin_matrix(binary_file)
    q_t = QuadTree()
    q_t.insert(matrix)

    # print the QuadTree structure
    print(q_t)

    # reconstruct image at full depth
    depth = infinity   # reconstructs the complete image

    rec_mat = q_t.reconstruct_image(depth)

    # plot reconstructed image
    plot_bin_matrix(rec_mat)