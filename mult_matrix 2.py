from typing import SupportsInt, List, Any
from math import gcd
from typing import overload

class Rational(SupportsInt):    
    def __init__(self, numerator: int, denominator: int = 1) -> None:
        if denominator == 0:
            raise ZeroDivisionError("Знаменатель не может быть равен нулю")
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        g = gcd(abs(numerator), denominator)
        self._num = numerator // g
        self._den = denominator // g

    def numerator(self) -> int:
        return self._num
    def denominator(self) -> int:
        return self._den    

    def __add__(self, other: Any) -> Rational:
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(
            self._num * other._den + other._num * self._den,
            self._den * other._den
        )

    def __radd__(self, other: int) -> Rational:
        return self + other

    def __sub__(self, other: Any) -> Rational:
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(
            self._num * other._den - other._num * self._den,
            self._den * other._den
        )

    def __rsub__(self, other: int) -> Rational:
        return Rational(other) - self

    def __mul__(self, other: Any) -> Rational:
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        return Rational(self._num * other._num, self._den * other._den)

    def __rmul__(self, other: int) -> Rational:
        return self * other

    def __truediv__(self, other: Any) -> Rational:
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        if other._num == 0:
            raise ZeroDivisionError("Деление на ноль")
        return Rational(self._num * other._den, self._den * other._num)

    def __rtruediv__(self, other: int) -> Rational:
        return Rational(other) / self

    def __neg__(self) -> Rational:
        return Rational(-self._num, self._den)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        return self._num == other._num and self._den == other._den

    def __hash__(self) -> int:
        return hash((self._num, self._den))

    def __int__(self) -> int:
        return self._num // self._den

    def __str__(self) -> str:
        if self._den == 1:
            return str(self._num)
        if self._num == 0:
            return "0"
        
        if self._num > 0:
            return f"\\frac{{{self._num}}}{{{self._den}}}"
        else:
            return f"-\\frac{{{ -self._num}}}{{{self._den}}}"

    def __repr__(self) -> str:
        return f"Rational({self._num}, {self._den})"

class Matrix:
    name: int
    rows: int
    cols: int
    elements: List[List[SupportsInt]]
    def __init__(self, name: str, rows: int, cols: int, elements: List[List[SupportsInt]]) -> None:
        self.name = name
        self.cols = cols
        self.rows = rows
        self.elements = elements

    def __str__(self) -> str:
        s:str = self.name + " = \\begin{bmatrix}\n"
        for l in range(self.rows):
            s += str(self.elements[l][0])
            for e in range(1, self.cols):
                s += " & " + str(self.elements[l][e])
            if l != self.rows - 1:
                s += " \\\\"
            s += "\n"
        s += "\\end{bmatrix}"
        return s

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
                elem: SupportsInt = 0
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

def input_matrix() -> Matrix:
    name:str = ""
    rows:int = 0
    cols:int = 0
    elements:List[List[SupportsInt]] = []
    while True:
        while True:
            inp:str = input("Введите название и размеры матрицы в формате A=3x3:\n")
            parts = inp.split("=")
            if len(parts) != 2:
                print("Некорректный формат ввода!")
                continue
            name_part: str
            sizes_part: str
            name_part, sizes_part = parts
            sizes_parts:List[SupportsInt] = sizes_part.split("x")
            if len(sizes_parts) != 2:
                print("Некорректный формат ввода размеров!")
                continue
            r, c = [int(i) for i in sizes_parts]
            if r < 1 or c < 1:
                print("Количество строк и столбцов должно быть не меньше 1!")
                continue
            name = name_part
            rows = r
            cols = c
            break
        elems:List[List[SupportsInt]] = [[0] * cols for _ in range(rows)]
        for l in range(rows):
            while True:
                inp = input(f"Введите {l + 1}-ю строку матрицы из {cols} элементов, разделяя их пробелом, для дробей / как дробная черта:\n")
                e:List[SupportsInt] = inp.split(" ")
                if len(e) != cols:
                    print(f"Вы ввели {len(e)} элементов, а должно быть {cols}.")
                    continue
                nums: List[SupportsInt] = []
                for i in e:
                    num_parts: List[str] = i.split("/")
                    if len(num_parts) == 2:
                        nums.append(Rational(*[int(n) for n in num_parts]))
                        continue
                    nums.append(int(i))
                elems[l] = nums
                break
        elements = elems
        break
    return Matrix(name, rows, cols, elements)

def show_matrix_multiplication(A: Matrix, B: Matrix, result_name: str) -> None:
    if A.cols != B.rows:
        print("Для умножения количество столбцов одной матрицы должно совпадать с количеством строк другой.")
        return

    s: str = f"Пусть ${result_name} = {A.name} \\cdot {B.name}$.\n\n"
    result_matrix: Matrix = A * B
    result_matrix.name = result_name
    for i in range(result_matrix.rows):
        for j in range(result_matrix.cols):
            s += "- $" + result_name + "_{" + f"{i+1}{j+1}" + "}$:\n  $"
            s += f"({A.elements[i][0]} \\cdot {B.elements[0][j]})"
            for k in range(1, result_matrix.rows):
                s += f" + ({A.elements[i][k]} \\cdot {B.elements[k][j]})"
            s += " \\\\\n"
            s += f"= {A.elements[i][0] * B.elements[0][j]}"
            for k in range(1, result_matrix.rows):
                s += f" + {A.elements[i][k] * B.elements[k][j]}"
            s += f" = {result_matrix.elements[i][j]}$\n"
    s = s.replace("+ -", "- ", -1)
    s += f"\n$${result_matrix}$$\n"
    print(s)

a = input_matrix()
b = input_matrix()
result_name = input("Введите имя матрицы результата:\n")
show_matrix_multiplication(a, b, result_name)