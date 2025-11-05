"""
Magic Square Core Constraint
This module generates and validates the fundamental self-balancing units of the quantum network.
"""

import numpy as np

def generate_magic_square_3x3():
    """
    Generates a classic 3x3 magic square.
    In our theory, this is the simplest non-trivial unit of a self-balancing spacetime network.
    Returns:
        np.array: A 3x3 magic square matrix.
    """
    # This is a standard Lo Shu square. We will later generalize to NxN and higher-dimensional "tensors".
    return np.array([[8, 1, 6],
                     [3, 5, 7],
                     [4, 9, 2]])

def is_magic_square(matrix, magic_constant=None):
    """
    Validates if a given NxN matrix satisfies the magic square condition.

    Args:
        matrix (np.array): An NxN matrix to validate.
        magic_constant (int, optional): The expected sum. If None, it's calculated from the first row.

    Returns:
        bool: True if the matrix is a magic square.
    """
    n = matrix.shape[0]
    if magic_constant is None:
        magic_constant = np.sum(matrix[0, :])

    # Check rows and columns
    for i in range(n):
        if np.sum(matrix[i, :]) != magic_constant or np.sum(matrix[:, i]) != magic_constant:
            return False

    # Check diagonals
    if np.sum(np.diag(matrix)) != magic_constant or np.sum(np.diag(np.fliplr(matrix))) != magic_constant:
        return False

    return True

def calculate_imbalance(matrix):
    """
    Calculates the total "imbalance" of a matrix.
    This function will be CRUCIAL later when we relax the perfect constraint and allow for quantum "fluctuations" or "information residual".
    The imbalance might correspond to energy or information density.

    Args:
        matrix (np.array): An NxN matrix.

    Returns:
        float: A measure of the matrix's deviation from a perfect magic square.
    """
    n = matrix.shape[0]
    magic_constant = np.sum(matrix) / n  # The ideal sum for a row/column/diagonal

    imbalance = 0
    for i in range(n):
        imbalance += abs(np.sum(matrix[i, :]) - magic_constant)
        imbalance += abs(np.sum(matrix[:, i]) - magic_constant)

    imbalance += abs(np.sum(np.diag(matrix)) - magic_constant)
    imbalance += abs(np.sum(np.diag(np.fliplr(matrix))) - magic_constant)

    return imbalance

if __name__ == "__main__":
    # Let's test our fundamental building block.
    ms = generate_magic_square_3x3()
    print("Our First Spacetime Quantum (3x3 Magic Square):")
    print(ms)
    print(f"Is it magical? {is_magic_square(ms)}")
    print(f"Its magic constant: {np.sum(ms[0, :])}")
    print(f"Its imbalance (should be 0): {calculate_imbalance(ms)}")

    # Test a non-magical matrix
    test_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\nA chaotic matrix imbalance: {calculate_imbalance(test_matrix)}")
