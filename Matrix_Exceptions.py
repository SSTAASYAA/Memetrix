class MatrixMultiplicationError(Exception):
    """
    Raised when attempting to multiply two matrices with incompatible dimensions.
    For matrix multiplication A × B, the number of columns in A must equal the number of rows in B.
    """

    def __init__(self, matrix_1: "Matrix", matrix_2: "Matrix"):
        self.firstMatrix = matrix_1
        self.secondMatrix = matrix_2
        self.message = (
            f"Cannot multiply matrices: {self.firstMatrix.rows} and {self.secondMatrix.cols} are incompatible. " 
            f"Columns of first ({self.firstMatrix.cols}) must equal rows of second ({self.secondMatrix.rows})."
        )
        super().__init__(self.message)


class MatrixDimensionError(Exception):
    """
    Raised when attempting to add or subtract matrices with incompatible dimensions.
    For matrix addition/subtraction A ± B, both matrices must have the same dimensions.
    """

    def __init__(self, matrix_1: "Matrix", matrix_2: "Matrix", operation: str = "addition"):
        self.firstMatrix = matrix_1
        self.secondMatrix = matrix_2
        self.message = (
            f"Cannot perform {operation}: matrices have different dimensions ({self.firstMatrix.rows}x{self.firstMatrix.cols}) and ({self.secondMatrix.rows}x{self.secondMatrix.cols})"
        )
        super().__init__(self.message)