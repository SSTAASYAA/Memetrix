from typing import List
#from Matrix_Exceptions import *

class Matrix:
    def __init__(self, name: str, rows: int, cols: int, elements: List[List[int]]) -> None:
        # if not all(isinstance(name, str), isinstance(rows, int), isinstance(elements, list)):
        #     raise TypeError("DIBIL")
        self.name = name
        self.cols = cols
        self.rows = rows
        self.elements = elements

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self._matrix_multiply(other)
        elif isinstance(other, (int)):
            return self._scalar_multiply(other)
        else:
            raise TypeError(f"Нельзя умножить Matrix на {type(other)}")

    def __rmul__(self, other):
        if isinstance(other, (int)):
            return self._scalar_multiply(other)
        elif isinstance(other, Matrix):
            return other._matrix_multiply(self)
        else:
            raise TypeError(f"Нельзя умножить {type(other)} на Matrix")

    def _matrix_multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(f"Размеры несовместимы: {self.rows}x{self.cols} и {other.rows}x{other.cols}")

        result_name: str = f"{self.name} \\cdot {other.name}"
        result_rows: int = self.rows
        result_cols: int = other.cols
        result_elems:List[List[SupportsInt]] = [[0] * result_cols for _ in range(result_rows)]
        for i in range(result_rows):
            for j in range(result_cols):
                elem: int = 0
                for k in range(result_rows):
                    elem += self.elements[i][k] * other.elements[k][j]
                result_elems[i][j] = elem

        return Matrix(result_name, result_rows, result_cols, result_elems)

    def _scalar_multiply(self, other: int):
        result_name: str = f"{other} {self.name}"
        result_elems:List[List[SupportsInt]] = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                result_elems[i][j] = self.elements[i][j] * other
        return Matrix(result_name, self.rows, self.cols, result_elems)