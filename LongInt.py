class LongInt:

    def __init__(self, M: int, N: int, Signed: bool, *Digits: int):
        if N > 750: raise ValueError(f"Превышена максимальная разрядность равная 750")
        if M < 1:   raise ValueError(f"Основание системы должно быть не менее 1, получено {M}")
        if N < 1:   raise ValueError(f"Максимальная разрядность должна быть не менее 1, получено {N}")

        self.base = M
        self.max_digits = N
        self.sign = Signed

        for val in Digits:
            if not isinstance(val, int):
                raise AttributeError("Все цифры должны быть целыми числами")
            if val < 0 or val >= M:
                raise AttributeError(f"Цифра {val} выходит за пределы допустимого диапазона [0, {M - 1}]")

        self.digits = list(Digits[::-1])

        if len(self.digits) > N:
            raise AttributeError(f"Длина числа равная {len(self.digits)} превышает разрядность {N}")

        # Удаляем ведущие нули
        self._normalize()

        if not self.digits:
            self.digits = [0]
            self.sign = False

    def __str__(self):
        """Представление числа в виде строки"""
        digits_str = '|'.join(str(d) for d in self.digits[::-1])
        sign_str = '-' if self.sign and self.digits != [0] else ''
        return f"{sign_str}{digits_str} (base {self.base})"

    def __repr__(self):
        return f"LongInt({self.base}, {self.max_digits}, {self.sign}, {', '.join(str(d) for d in self.digits[::-1])})"

    def _normalize(self):
        """Нормализация числа - удаление ведущих нулей"""
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        if not self.digits:
            self.digits = [0]
            self.sign = False

    def _compare_magnitude(self, other):
        """Сравнение двух чисел, которое возвращает:
           1. Отрицательное число в случае если левый операнд меньше;
           2. Положительное число если левый операнд больше
           Функция создана для ускорения сравнения
           т.к. Полноценное вычитание необязательно для сравнения"""
        if len(self.digits) != len(other.digits):
            return len(self.digits) - len(other.digits)

        for i in range(len(self.digits) - 1, -1, -1):
            if self.digits[i] != other.digits[i]:
                return self.digits[i] - other.digits[i]
        return 0

    def _is_zero(self):
        """Проверка, является ли число нулем"""
        return len(self.digits) == 1 and self.digits[0] == 0

    def __add__(self, other):
        """Сложение двух чисел с учетом знаков"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")

        # Оба положительные
        if not self.sign and not other.sign:
            return self._add_positive(other)

        # Оба отрицательные
        if self.sign and other.sign:
            result = self._add_positive(other)
            result.sign = True
            return result

        # Разные знаки - преобразуем к вычитанию
        if self.sign and not other.sign:
            # -a + b = b - a
            return other - self._abs()
        else:
            # a + (-b) = a - b
            return self - other._abs()

    def _add_positive(self, other):
        """Сложение положительных чисел"""
        result_digits = []
        carry = 0
        max_len = max(len(self.digits), len(other.digits))

        for i in range(max_len):
            digit1 = self.digits[i] if i < len(self.digits) else 0
            digit2 = other.digits[i] if i < len(other.digits) else 0

            total = digit1 + digit2 + carry
            carry = total // self.base
            result_digits.append(total % self.base)

        if carry > 0:
            if len(result_digits) >= self.max_digits:
                raise OverflowError("Превышена максимальная разрядность")
            result_digits.append(carry)

        result = LongInt(self.base, self.max_digits, False, *result_digits[::-1])
        result._normalize()
        return result

    def __sub__(self, other):
        """Вычитание двух чисел с учетом знаков"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")

        # Оба положительные
        if not self.sign and not other.sign:
            return self._sub_positive(other)

        # Оба отрицательные
        if self.sign and other.sign:
            # -a - (-b) = -a + b = b - a
            return other._abs() - self._abs()

        if self.sign and not other.sign:
            result = self._abs()._add_positive(other)
            result.sign = True
            return result
        else:
            return self._add_positive(other._abs())

    def _sub_positive(self, other):
        """Вычитание положительных чисел"""
        comp = self._compare_magnitude(other)

        if comp < 0:
            larger, smaller = other, self
            result_sign = True
        else:
            larger, smaller = self, other
            result_sign = False

        result_digits = []
        borrow = 0

        for i in range(len(larger.digits)):
            digit_larger = larger.digits[i]
            digit_smaller = smaller.digits[i] if i < len(smaller.digits) else 0

            diff = digit_larger - digit_smaller - borrow

            if diff < 0:
                diff += self.base
                borrow = 1
            else:
                borrow = 0

            result_digits.append(diff)

        result = LongInt(self.base, self.max_digits, result_sign, *result_digits[::-1])
        result._normalize()
        return result

    def _abs(self):
        """Возвращает модуль числа"""
        return LongInt(self.base, self.max_digits, False, *self.digits[::-1])

    def __mul__(self, other):
        """Умножение двух чисел"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")

        result = LongInt(self.base, self.max_digits, False, 0)

        for i, digit1 in enumerate(self.digits):
            carry = 0
            temp_digits = [0] * i

            for digit2 in other.digits:
                product = digit1 * digit2 + carry
                carry = product // self.base
                temp_digits.append(product % self.base)

            if carry > 0:
                temp_digits.append(carry)

            temp_num = LongInt(self.base, self.max_digits, False, *temp_digits[::-1])
            result = result + temp_num

        result_sign = self.sign != other.sign
        result.sign = result_sign
        result._normalize()

        return result

    def __floordiv__(self, other):
        """Целочисленное деление с учетом знаков"""
        if self.base != other.base:
            raise ValueError("Основания систем счисления должны совпадать")

        if other._is_zero():
            raise ZeroDivisionError("Деление на ноль")

        # Остаток от разности на протяжении деления в столбик
        remaind = LongInt(self.base, self.max_digits, False, 0)
        remaind.digits.clear()

        res = LongInt(self.base, self.max_digits, False, 0)
        res.digits.clear()
        divisor = other._abs()

        for val in self.digits[::-1]:
            remaind.digits.insert(0,val)

            iterRes = 0 # Промежуточный результат за одну итерацию.
            while (not (remaind < divisor)):
                remaind = remaind - divisor
                iterRes = iterRes + 1

            if remaind._is_zero(): remaind.digits.clear()
            res.digits.insert(0,iterRes)

        if not remaind._is_zero():
            res.sign = self.sign ^ divisor.sign
        res._normalize()

        return res

    def __mod__(self, other):
        """Остаток от деления"""
        quotient = self // other
        temp = quotient * other
        remainder = self - temp
        return remainder

    def __eq__(self, other):
        """Проверка на равенство"""
        if not isinstance(other, LongInt):
            return False
        return (self.base == other.base and
                self.sign == other.sign and
                self.digits == other.digits)

    def __lt__(self, other):
        """Проверка на меньше"""
        if self.sign != other.sign:
            return self.sign > other.sign

        comp = self._compare_magnitude(other)
        if self.sign:
            return comp > 0
        else:
            return comp < 0

    def to_int(self) -> int:
        """
        Преобразует число в целое число (int).
        Внимание: может вызвать переполнение для очень больших чисел!
        """
        result = 0
        power = 1

        for digit in self.digits:
            result += digit * power
            power *= self.base

        return -result if self.sign and result != 0 else result

