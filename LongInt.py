class LongInt:
    alphabet = "-0123456789abcdefghijklmnopqrstuvwxyz"

    def __init__(self, num_str: str, M: int, N: int):
        if len(num_str) > N:
            raise AttributeError(f"Число больше допустимой разрядности {N}")

        if M < 2 or M > (len(LongInt.alphabet)-1):
            raise AttributeError(
                f"Дозволенные разрядности: 2 - {len(LongInt.alphabet) - 1}")

        self.M = M
        self.N = N
        _fact_alphabet = LongInt.alphabet[1:M+1]

        if num_str.startswith('-'):
            self.sign = -1
            num_str = num_str[1:]
        else:
            self.sign = 1

        for char in num_str:
            if char not in _fact_alphabet:
                raise AttributeError(
                    f"Цифра '{char}' недопустима в системе счисления {M}.")

        num_str = num_str.lstrip('0') or '0'

        self.digits = []
        for char in num_str[::-1]:
            self.digits.append(LongInt.alphabet.index(char) - 1)

        self._normalize()

    def _normalize(self) -> None:
        """Удаление ведущих нулей и нормализация"""
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()

        if len(self.digits) == 1 and self.digits[0] == 0:
            self.sign = 1

    def __str__(self) -> str:
        """Преобразование в строку"""
        if len(self.digits) == 1 and self.digits[0] == 0:
            return "0"

        chars = []
        for digit in reversed(self.digits):
            chars.append(LongInt.alphabet[digit + 1])

        result = ''.join(chars)
        if self.sign == -1 and result != "0":
            result = '-' + result

        return result

    def _compare_absolute(self, other) -> int:
        """Сравнение абсолютных значений"""
        if len(self.digits) > len(other.digits):
            return 1
        elif len(self.digits) < len(other.digits):
            return -1

        for i in range(len(self.digits)-1, -1, -1):
            if self.digits[i] > other.digits[i]:
                return 1
            elif self.digits[i] < other.digits[i]:
                return -1

        return 0

    def _is_zero(self) -> bool:
        """Проверка на ноль"""
        return len(self.digits) == 1 and self.digits[0] == 0

    def __add__(self, other):
        """Сложение"""
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        if self.sign != other.sign:
            if self.sign == -1:
                return other - LongInt(self.__str__()[1:], self.M, self.N)
            else:
                return self - LongInt(other.__str__()[1:], self.M, self.N)

        result = LongInt("0", self.M, self.N)
        result.sign = self.sign

        max_len = max(len(self.digits), len(other.digits))
        carry = 0

        for i in range(max_len):
            digit1 = self.digits[i] if i < len(self.digits) else 0
            digit2 = other.digits[i] if i < len(other.digits) else 0

            total = digit1 + digit2 + carry
            carry = total // self.M
            digit = total % self.M

            if i < len(result.digits):
                result.digits[i] = digit
            else:
                result.digits.append(digit)

        if carry > 0:
            if len(result.digits) >= self.N:
                raise OverflowError("Превышена максимальная разрядность")
            result.digits.append(carry)

        result._normalize()
        return result

    def __sub__(self, other):
        """Вычитание"""
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        if self.sign != other.sign:
            if self.sign == -1:
                # -a - b = -(a + b)
                temp = LongInt(self.__str__()[1:], self.M, self.N) + other
                temp.sign = -1
                return temp
            else:
                # a - (-b) = a + b
                return self + LongInt(other.__str__()[1:], self.M, self.N)

        if self.sign == -1:
            positive_other = LongInt(other.__str__()[1:], self.M, self.N)
            positive_self = LongInt(self.__str__()[1:], self.M, self.N)
            return positive_other - positive_self

        cmp = self._compare_absolute(other)

        if cmp == 0:
            return LongInt("0", self.M, self.N)

        if cmp < 0:
            result = other._subtract_absolute(self)
            result.sign = -1
            return result
        else:
            return self._subtract_absolute(other)

    def _subtract_absolute(self, other):
        """Вычитание абсолютных значений (self >= other)"""
        result = LongInt("0", self.M, self.N)
        borrow = 0

        for i in range(len(self.digits)):
            digit1 = self.digits[i]
            digit2 = other.digits[i] if i < len(other.digits) else 0

            diff = digit1 - digit2 - borrow

            if diff < 0:
                diff += self.M
                borrow = 1
            else:
                borrow = 0

            if i < len(result.digits):
                result.digits[i] = diff
            else:
                result.digits.append(diff)

        result._normalize()
        return result

    def __mul__(self, other):
        """Умножение"""
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        if self._is_zero() or other._is_zero():
            return LongInt("0", self.M, self.N)

        result = LongInt("0", self.M, self.N)
        result.sign = self.sign * other.sign

        for i, digit1 in enumerate(self.digits):
            carry = 0
            temp_digits = [0] * i  # Сдвиг на i разрядов

            for digit2 in other.digits:
                product = digit1 * digit2 + carry
                carry = product // self.M
                temp_digits.append(product % self.M)

            if carry > 0:
                if len(temp_digits) >= self.N:
                    raise OverflowError("Превышена максимальная разрядность")
                temp_digits.append(carry)

            temp_num = LongInt("0", self.M, self.N)
            temp_num.digits = temp_digits
            temp_num._normalize()

            result = result + temp_num

        result._normalize()
        return result

    def __floordiv__(self, other):
        """Целочисленное деление"""
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        if other._is_zero():
            raise ZeroDivisionError("Деление на ноль")

        if self._is_zero():
            return LongInt("0", self.M, self.N)

        cmp = self._compare_absolute(other)
        if cmp < 0:
            return LongInt("0", self.M, self.N)

        if cmp == 0:
            result = LongInt("1", self.M, self.N)
            result.sign = self.sign * other.sign
            return result

        result = LongInt("0", self.M, self.N)
        result.sign = self.sign * other.sign

        dividend = LongInt(self.__str__(), self.M, self.N)
        dividend.sign = 1
        divisor = LongInt(other.__str__(), self.M, self.N)
        divisor.sign = 1

        quotient_digits = []
        current = LongInt("0", self.M, self.N)

        for i in range(len(dividend.digits)-1, -1, -1):
            current = current * LongInt(str(self.M), self.M, self.N)
            current = current + \
                LongInt(str(dividend.digits[i]), self.M, self.N)

            digit = 0
            left, right = 0, self.M - 1

            while left <= right:
                mid = (left + right) // 2
                temp = divisor * LongInt(str(mid), self.M, self.N)

                if temp._compare_absolute(current) <= 0:
                    digit = mid
                    left = mid + 1
                else:
                    right = mid - 1

            quotient_digits.append(digit)
            subtract = divisor * LongInt(str(digit), self.M, self.N)
            current = current - subtract

        result.digits = quotient_digits[::-1]

        result._normalize()

        if result.sign == 1:
            result = result - LongInt("1", self.M, self.N)
        else:
            result = result + LongInt("1", self.M, self.N)

        return result

    def __eq__(self, other):
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        return (self.sign == other.sign and
                len(self.digits) == len(other.digits) and
                all(a == b for a, b in zip(self.digits, other.digits)))

    def __lt__(self, other):
        if not isinstance(other, LongInt):
            raise AttributeError(
                f"Переданный параметр не принадлежит классу f{self.__class__}")

        if other.M != self.M:
            raise AttributeError(
                f"Переданный параметр имеет другую систему счисления: {self.M} | {other.M}")

        if self.sign != other.sign:
            return self.sign < other.sign

        cmp = self._compare_absolute(other)
        if self.sign == 1:
            return cmp < 0
        else:
            return cmp > 0

    def to_int(self) -> int:
        """Преобразование в обычное целое число"""
        result = 0
        for i, digit in enumerate(self.digits):
            result += digit * (self.M ** i)
        return result * self.sign


# Пример использования и тестирования
if __name__ == "__main__":
    # Тестирование в 10-ричной системе
    print("Тестирование в 10-ричной системе:")
    a = LongInt("123", 10, 100)
    b = LongInt("45", 10, 100)

    print(f"a = {a}, b = {b}")
    print(f"a + b = {a + b}")      # 168
    print(f"a - b = {a - b}")      # 78
    print(f"b - a = {b - a}")      # -78
    print(f"a * b = {a * b}")      # 5535
    print(f"a // b = {a // b}")    # 2

    # Тестирование в 16-ричной системе
    print("\nТестирование в 16-ричной системе:")
    hex_a = LongInt("a1f", 16, 100)
    hex_b = LongInt("2b", 16, 100)

    print(f"hex_a = {hex_a} (в десятичной: {hex_a.to_int()})")
    print(f"hex_b = {hex_b} (в десятичной: {hex_b.to_int()})")
    print(f"hex_a + hex_b = {hex_a + hex_b}")  # a4a
    print(f"hex_a - hex_b = {hex_a - hex_b}")  # 9f4
    print(f"hex_a * hex_b = {hex_a * hex_b}")  # 1b8d5
    print(f"hex_a // hex_b = {hex_a // hex_b}")  # 3c
