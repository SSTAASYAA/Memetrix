from typing import Any, SupportsInt
from math import gcd

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
            return f"{self._num}/{self._den}"
        else:
            return f"-{ -self._num}/{self._den}"

    def __repr__(self) -> str:
        return f"Rational({self._num}, {self._den})"
