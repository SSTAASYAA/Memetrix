from typing import List, SupportsInt
from matrix_exceptions import *

class Matrix:
    def __init__(self, rows: int, cols: int, elements: list[list[int]] = []) -> None:
        if not isinstance(rows, int):
            raise TypeError(f"type(rows) must be int, but ({type(rows)}) found.")
        elif not isinstance(cols, int):
            raise TypeError(f"type(cols) must be int, but ({type(cols)}) found.")
        elif rows < 1 or cols < 1:
            raise MatrixInputError("Rows and cols must be greater than 1.")
        else:
            if not isinstance(elements, (list, tuple)) or not all([isinstance(row, (list, tuple)) for row in elements]):
                raise TypeError(f"Type of elements must be list or tuple and all types of each row must be list or tuple.")
            elif not len(elements) <= cols:
                raise MatrixInputError(f"Number of rows in elements must be lower or equal {cols}, but {len(elements)} found.")
            elif not all([len(row) <= rows for row in elements]):
                raise MatrixInputError(f"Number of elements in each row mush be lower or equal {rows}, but more found.")
            elif not all([isinstance(el, SupportsInt) for row in elements for el in row]):
                raise TypeError(f"Type of each element in elements must be int or float, but another found.")

        self.cols = cols
        self.rows = rows
        self.elements = [
            *[self._extend_row(row, rows) for row in elements], 
            *[self._extend_row([], rows) for _ in range(cols - len(elements))]
        ]
    
    def __str__(self) -> str:
        return f"{self.elements}"

    def __getitem__(self, key) -> int | float:
        if isinstance(key, (list, tuple)) and len(key) == 2:
            if self.cols == 1: 
                raise IndexError(f"Can't access to the element with index {key}")
            if not 1 <= key[0] <= self.cols or not 1 <= key[1] <= self.rows:
                raise ValueError(f"Indeces must be: [1 <= {key[0]} <= {self.cols}, 1 <= {key[1]} <= {self.rows}]")
            return self.elements[key[0] - 1][key[1] - 1]
        elif isinstance(key, int):
            if self.cols == 1:
                if key < 1 or key > self.rows:
                    raise ValueError(f"Index must be 1 <= index <= {self.rows}")
                return self.elements[0][key - 1]
            else:
                return self.elements[key - 1]
        else:
            raise TypeError("Invalid index type")

    def _extend_row(self, row: list[int | float], size: int) -> list[int | float]:
        return row + [0] * (size - len(row))

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self._matrix_multiply(other)
        elif isinstance(other, (int)):
            return self._scalar_multiply(other)
        else:
            raise TypeError(f"type(other) must be Matrix or compatible with int, but ({type(other)}) found.")

    def __rmul__(self, other):
        if isinstance(other, (SupportsInt)):
            return self._scalar_multiply(other)
        elif isinstance(other, Matrix):
            return other._matrix_multiply(self)
        else:
            raise TypeError(f"type(other) must be Matrix or compatible with int, but ({type(other)}) found.")

    def _matrix_multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Размеры несовместимы: {self.rows}x{self.cols} и {other.rows}x{other.cols}")

        result_rows: int = self.rows
        result_cols: int = other.cols
        result_elems:List[List[SupportsInt]] = [[0] * result_cols for _ in range(result_rows)]
        for i in range(result_rows):
            for j in range(result_cols):
                elem: int = 0
                for k in range(result_rows):
                    elem += self.elements[i][k] * other.elements[k][j]
                result_elems[i][j] = elem

        return Matrix(result_rows, result_cols, result_elems)

    def _scalar_multiply(self, other: SupportsInt):
        result_elems:List[List[SupportsInt]] = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                result_elems[i][j] = self.elements[i][j] * other
        return Matrix(self.rows, self.cols, result_elems)
