"""Project 6: Quad Trees
Kim Huynh, 2026-05-06, CS 211
"""

"""
Module designed to produce, read and plot binary files from images.
"""
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from statistics import mean
    
def read_bin_matrix(file_name):
    """Read a file text and convert its contents to a matrix"""
    matrix = []
    with open(file_name, "r") as text_file:
        while (line := text_file.readline()):
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix
        
def write_matrix(matrix, file_name):
    """
    Write a matrix to a text file. Using loops for illustration purposes.
    Exercise: eliminate the loops.
    """
    with open(file_name, "w") as text_file:
        for row in matrix:
            for el in row:
                text_file.write(str(el) + " ")
            text_file.write('\n')

def plot_bin_matrix(matrix):
    """
    Plotting a binary matrix using matplotlib. 
    The matrix must be converted to gray levels before plotting.
    """
    gray_matrix = [list(map(gray, x)) for x in matrix]
    plt.matshow(gray_matrix)
    plt.show()

def binarize_number(x):
    """convert a number from gray level [0 - 255] to binary {0, 1}"""
    return 0 if x < 128 else 1

def binarize_RGB(color):
    """convert a number from an RGB triplet to binary {0, 1}"""
    return binarize_number(sum(color)/3)

def gray(n):
    """convert a number from binary {0, 1} to gray level [0 - 255]"""
    return n*255

def binarize_matrix(matrix):
    """Combination of list comprehension and map to properly traverse a matrix"""
    bin_mat = [list(map(binarize_number, row)) for row in matrix]
    return bin_mat

def image_to_matrix(image_file):
    """numpy does all the work"""
    img = Image.open(image_file)
    numpydata = np.asarray(img)
    bin_data = binarize_matrix(numpydata)
    return bin_data

def flatten(a_list):
    """non-rec flatten for nested lists of depth 2"""
    flatlist=[element for sublist in a_list for element in sublist]
    return flatlist

def split_list(data, size):
    """splits a list on chunks of length size"""
    return [data[i:i+size] for i in range(0, len(data), size)]

# 2.2
def submatrix(matrix, r_loc, c_loc):
    """returns the submatrix of matrix delimited by rows in r_loc=(r1, r2) and columns in c_loc=(c1, c2)"""
    r1, r2 = r_loc
    c1, c2 = c_loc

    result = []

    for row in matrix[r1:r2]:
        result.append(row[c1:c2])

    return result

# 2.3
def split_4(matrix):
    """
    Splits matrix in 4 submatrices, assuming matrix is square and its size is 
    a power of 2. 
    The result is returned in order [nw, ne, se, sw] where the original matrix
    is in order
    [[nw ne]
     [sw se]].
    """
    n = len(matrix)
    new_n = n//2
    masks_1d = [(i*new_n, (i+1)*new_n) for i in range(2)] # These tuples define the ranges for indexing the rows and columns of the submatrices.
    masks = [(a, b) for a in masks_1d for b in masks_1d] # creates a list of tuples representing the ranges for indexing all four submatrices. 
    [nw, ne, sw, se] = [submatrix(matrix, m[0], m[1]) for m in masks] # The submatrix function is called with the current mask's row and column ranges, and the resulting submatrix is stored in the respective variable (nw, ne, sw, se).
    return [nw, ne, se, sw]

# 2.5 
def same_bits(bin_mat):
    """Returns true if all elements of bin_mat contain the same value"""
    flat_mat = flatten(bin_mat)
    first = flat_mat[0]

    for value in flat_mat:
        if value != first:
            return False
    return True

# 2.6
def matrix_mean(matrix):
    """Computes the mean of matrix's elements"""
    flat_mat = flatten(matrix)
    return mean(flat_mat)

# 2.4
def stitch_vertical(top, bottom):
    """stitches the matrices together, according to axis 0"""
    return top + bottom

# 2.4
def stitch_horizontal(left, right):
    """stitches the matrices together, according to axis 1"""
    result = []
    
    for i in range(len(left)):
        result.append(left[i] + right[i])

    return result

# 2.4
def stitch_matrices(nw, ne, se, sw):
    """Stitches the two matrices together"""
    top = stitch_horizontal(nw, ne)
    bottom = stitch_horizontal(sw, se)
    return stitch_vertical(top, bottom)


if __name__ == "__main__":
    # test matrix from lab instructions
    matrix = [
        [0, 0, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ]

    # print original matrix
    print("Original Matrix:")
    print(matrix)

    # testing submatrix
    print("\nTesting submatrix:")
    print(submatrix(matrix, (1, 3), (0, 2)))

    # testing split_4
    print("\nTesting split_4:")

    m_4 = split_4(matrix)

    for x in m_4:
        print("--")
        print(x)

    # testing same_bits
    print("\nTesting same_bits:")

    print(same_bits(m_4[0]))   # expected False
    print(same_bits(m_4[1]))   # expected True

    # testing matrix_mean
    print("\nTesting matrix_mean:")

    m = [[1, 1], [0, 1]]
    print(f"mean = {matrix_mean(m)}")

    # testing stitching
    print("\nTesting stitching:")

    [nw, ne, se, sw] = m_4

    stitched = stitch_matrices(nw, ne, se, sw)

    print(stitched)