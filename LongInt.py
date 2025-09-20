class LongInt:
    def __init__(self, M: int, N: int, Signed: bool, *Digits: int):
        if M < 1:
            raise ValueError(f"Основание системы должно быть не менее 1, получено {M}")
        if N < 1:
            raise ValueError(f"Максимальная разрядность должна быть не менее 1, получено {N}")
        
        self.base = M
        self.max_digits = N
        self.sign = Signed
        
        for i in Digits:
            if not isinstance(i, int):
                raise AttributeError("Все цифры должны быть целыми числами")
            if i < 0 or i >= M:
                raise AttributeError(f"Цифра {i} выходит за пределы допустимого диапазона [0, {M-1}]")
        
        self.digits = list(Digits[::-1])
        
        # Удаляем ведущие нули
        while len(self.digits) > 1 and self.digits[-1] == 0:
            self.digits.pop()
        
        if not self.digits:
            self.digits = [0]
            self.sign = False  # Ноль всегда положительный
    
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
        """Сравнение модулей двух чисел (без учета знака)"""
        if len(self.digits) != len(other.digits):
            return len(self.digits) - len(other.digits)
        
        for i in range(len(self.digits)-1, -1, -1):
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
        result = LongInt(self.base, self.max_digits, False, *self.digits[::-1])
        return result
    
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
        
        abs_self = self._abs()
        abs_other = other._abs()
        
        quotient = LongInt(self.base, self.max_digits, False, 0)
        remainder = LongInt(self.base, self.max_digits, False, *abs_self.digits[::-1])
        
        one = LongInt(self.base, self.max_digits, False, 1)
        
        while remainder._compare_magnitude(abs_other) >= 0:
            remainder = remainder - abs_other
            quotient = quotient + one
        
        quotient.sign = self.sign != other.sign
        quotient._normalize()
        
        return quotient
    
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

def test_operations(base, *digits_list, title=""):
    """Тестирует все операции для заданной системы счисления"""
    print(f"\n{'='*60}")
    print(f"{title} (Система счисления {base})")
    print(f"{'='*60}")
    
    # Создаем числа
    numbers = []
    for i, digits in enumerate(digits_list):
        num = LongInt(base, 100, False, *digits)
        numbers.append(num)
        print(f"Число {i+1}: {num}")
    
    print()
    
    # Тестируем все операции
    a, b = numbers[0], numbers[1]
    
    # Сложение
    try:
        result = a + b
        print(f"Сложение: {a} + {b} = {result}")
    except Exception as e:
        print(f"Ошибка сложения: {e}")
    
    # Вычитание
    try:
        result = a - b
        print(f"Вычитание: {a} - {b} = {result}")
    except Exception as e:
        print(f"Ошибка вычитания: {e}")
    
    # Умножение
    try:
        result = a * b
        print(f"Умножение: {a} * {b} = {result}")
    except Exception as e:
        print(f"Ошибка умножения: {e}")
    
    # Деление
    try:
        result = a // b
        print(f"Деление: {a} // {b} = {result}")
    except Exception as e:
        print(f"Ошибка деления: {e}")
    
    # Остаток
    try:
        result = a % b
        print(f"Остаток: {a} % {b} = {result}")
    except Exception as e:
        print(f"Ошибка остатка: {e}")
    
    print()

# ===== СИСТЕМА СЧИСЛЕНИЯ 2 (ДВОИЧНАЯ) =====
test_operations(
    2,
    [1, 0, 1, 1],   # 1011₂ = 11 десятичное
    [1, 1, 0],      # 110₂ = 6 десятичное
    title="ДВОИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для двоичной системы
print("Дополнительные двоичные примеры:")
bin1 = LongInt(2, 100, False, 1, 1, 1, 1)    # 1111₂ = 15
bin2 = LongInt(2, 100, False, 1, 0, 1)       # 101₂ = 5
print(f"1111₂ + 101₂ = {bin1 + bin2}")       # 10100₂ = 20
print(f"1111₂ * 101₂ = {bin1 * bin2}")       # 1001011₂ = 75
print()

# ===== СИСТЕМА СЧИСЛЕНИЯ 10 (ДЕСЯТИЧНАЯ) =====
test_operations(
    10,
    [1, 2, 3],      # 123
    [4, 5],         # 45
    title="ДЕСЯТИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для десятичной системы
print("Дополнительные десятичные примеры:")
dec1 = LongInt(10, 100, False, 9, 9, 9)      # 999
dec2 = LongInt(10, 100, False, 1)            # 1
print(f"999 + 1 = {dec1 + dec2}")            # 1000
print(f"999 * 2 = {dec1 * LongInt(10, 100, False, 2)}")  # 1998
print()

# Пример с отрицательными числами
dec_neg = LongInt(10, 100, True, 5, 0)       # -50
dec_pos = LongInt(10, 100, False, 3, 0)      # 30
print(f"Отрицательные: {-50} + {30} = {dec_neg + dec_pos}")  # -20
print(f"Отрицательные: {-50} * {30} = {dec_neg * dec_pos}")  # -1500
print()

# ===== СИСТЕМА СЧИСЛЕНИЯ 16 (ШЕСТНАДЦАТЕРИЧНАЯ) =====
test_operations(
    16,
    [10, 11, 12],   # ABC₁₆ = 2748 десятичное (10*256 + 11*16 + 12)
    [5, 15],        # 5F₁₆ = 95 десятичное (5*16 + 15)
    title="ШЕСТНАДЦАТЕРИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для шестнадцатеричной системы
print("Дополнительные шестнадцатеричные примеры:")
hex1 = LongInt(16, 100, False, 15, 15)       # FF₁₆ = 255
hex2 = LongInt(16, 100, False, 1)            # 1₁₆ = 1
print(f"FF₁₆ + 1₁₆ = {hex1 + hex2}")         # 100₁₆ = 256
print(f"FF₁₆ * 2₁₆ = {hex1 * LongInt(16, 100, False, 2)}")  # 1FE₁₆ = 510

# Пример с буквенными обозначениями (A=10, B=11, C=12, D=13, E=14, F=15)
hex_a = LongInt(16, 100, False, 10)          # A₁₆ = 10
hex_b = LongInt(16, 100, False, 11)          # B₁₆ = 11
print(f"A₁₆ + B₁₆ = {hex_a + hex_b}")        # 15₁₆ = 21 (но в 16-ричной: 15 = F)
print()

# ===== СЛОЖНЫЕ ПРИМЕРЫ =====
print("="*60)
print("СЛОЖНЫЕ ПРИМЕРЫ С РАЗНЫМИ СИСТЕМАМИ")
print("="*60)

# Сравнение производительности в разных системах
numbers_to_test = [
    ([2], [1, 0, 1, 1], [1, 1, 0]),          # Двоичная
    ([10], [1, 2, 3], [4, 5]),               # Десятичная
    ([16], [10, 11, 12], [5, 15]),           # Шестнадцатеричная
]

for base, num1_digits, num2_digits in numbers_to_test:
    base_val = base[0]
    num1 = LongInt(base_val, 100, False, *num1_digits)
    num2 = LongInt(base_val, 100, False, *num2_digits)
    
    print(f"\nСистема {base_val}:")
    print(f"{num1} + {num2} = {num1 + num2}")
    print(f"{num1} * {num2} = {num1 * num2}")