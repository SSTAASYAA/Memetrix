class MatrixMultiplicationError(Exception):
    """
    Raised when attempting to multiply two matrices with incompatible dimensions.
    For matrix multiplication A × B, the number of columns in A must equal the number of rows in B.
    """

    def __init__(self, matrix_1: "Matrix", matrix_2: "Matrix"):
        self.firstMatrix = matrix_1; self.secondMatrix = matrix_2
        self.message = f""