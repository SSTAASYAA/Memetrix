from typing import List, SupportsInt
from matrix import Matrix
from rational import Rational

def input_matrix() -> Matrix:
    rows:int = 0
    cols:int = 0
    elements:List[List[SupportsInt]] = []
    while True:
        while True:
            inp:str = input("Введите размеры матрицы в формате3x3:\n")
            sizes_parts:List[SupportsInt] = inp.split("x")
            if len(sizes_parts) != 2:
                print("Некорректный формат ввода размеров!")
                continue
            r, c = [int(i) for i in sizes_parts]
            if r < 1 or c < 1:
                print("Количество строк и столбцов должно быть не меньше 1!")
                continue
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
    return Matrix(rows, cols, elements)

def show_matrix_multiplication(A_name:str, A: Matrix, b_name: str, B: Matrix, result_name: str) -> None:
    if A.cols != B.rows:
        print("Для умножения количество столбцов одной матрицы должно совпадать с количеством строк другой.")
        return

    s: str = f"Пусть {result_name} = {A_name} * {B_name}.\n\n"
    result_matrix: Matrix = A * B
    for i in range(result_matrix.rows):
        for j in range(result_matrix.cols):
            s += "- " + result_name + "_" + f"{i+1}{j+1}" + ":\n  "
            s += f"({A.elements[i][0]} \\cdot {B.elements[0][j]})"
            for k in range(1, result_matrix.rows):
                s += f" + ({A.elements[i][k]} \\cdot {B.elements[k][j]})"
            s += f"\n= {A.elements[i][0] * B.elements[0][j]}"
            for k in range(1, result_matrix.rows):
                s += f" + {A.elements[i][k] * B.elements[k][j]}"
            s += f" = {result_matrix.elements[i][j]}\n"
    s = s.replace("+ -", "- ", -1)
    s += f"\n{result_name} = {result_matrix}\n"
    print(s)

m = Matrix(1, 2, [[1, 2]])
A_name:str = input("Введите название первой матрицы:\n")
a = input_matrix()
B_name:str = input("Введите название второй матрицы:\n")
b = input_matrix()
result_name:str = input("Введите имя матрицы результата:\n")
show_matrix_multiplication(A_name, a, B_name, b, result_name)