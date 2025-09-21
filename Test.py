from LongInt import LongInt

def test_operations(base, *digits_list, title=""):
    """Тестирует все операции для заданной системы счисления"""
    print(f"\n{'=' * 60}")
    print(f"{title} (Система счисления {base})")
    print(f"{'=' * 60}")

    # Создаем числа
    numbers = []
    for i, digits in enumerate(digits_list):
        num = LongInt(base, 100, False, *digits)
        numbers.append(num)
        print(f"Число {i + 1}: {num}")

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
    [1, 0, 1, 1],  # 1011₂ = 11 десятичное
    [1, 1, 0],  # 110₂ = 6 десятичное
    title="ДВОИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для двоичной системы
print("Дополнительные двоичные примеры:")
bin1 = LongInt(2, 100, False, 1, 1, 1, 1)  # 1111₂ = 15
bin2 = LongInt(2, 100, False, 1, 0, 1)  # 101₂ = 5
print(f"1111₂ + 101₂ = {bin1 + bin2}")  # 10100₂ = 20
print(f"1111₂ * 101₂ = {bin1 * bin2}")  # 1001011₂ = 75
print()

# ===== СИСТЕМА СЧИСЛЕНИЯ 10 (ДЕСЯТИЧНАЯ) =====
test_operations(
    10,
    [1, 2, 3],  # 123
    [4, 5],  # 45
    title="ДЕСЯТИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для десятичной системы
print("Дополнительные десятичные примеры:")
dec1 = LongInt(10, 100, False, 9, 9, 9)  # 999
dec2 = LongInt(10, 100, False, 1)  # 1
print(f"999 + 1 = {dec1 + dec2}")  # 1000
print(f"999 * 2 = {dec1 * LongInt(10, 100, False, 2)}")  # 1998
print()

# Пример с отрицательными числами
dec_neg = LongInt(10, 100, True, 5, 0)  # -50
dec_pos = LongInt(10, 100, False, 3, 0)  # 30
print(f"Отрицательные: {-50} + {30} = {dec_neg + dec_pos}")  # -20
print(f"Отрицательные: {-50} * {30} = {dec_neg * dec_pos}")  # -1500
print()

# ===== СИСТЕМА СЧИСЛЕНИЯ 16 (ШЕСТНАДЦАТЕРИЧНАЯ) =====
test_operations(
    16,
    [10, 11, 12],  # ABC₁₆ = 2748 десятичное (10*256 + 11*16 + 12)
    [5, 15],  # 5F₁₆ = 95 десятичное (5*16 + 15)
    title="ШЕСТНАДЦАТЕРИЧНАЯ СИСТЕМА"
)

# Дополнительные примеры для шестнадцатеричной системы
print("Дополнительные шестнадцатеричные примеры:")
hex1 = LongInt(16, 100, False, 15, 15)  # FF₁₆ = 255
hex2 = LongInt(16, 100, False, 1)  # 1₁₆ = 1
print(f"FF₁₆ + 1₁₆ = {hex1 + hex2}")  # 100₁₆ = 256
print(f"FF₁₆ * 2₁₆ = {hex1 * LongInt(16, 100, False, 2)}")  # 1FE₁₆ = 510

# Пример с буквенными обозначениями (A=10, B=11, C=12, D=13, E=14, F=15)
hex_a = LongInt(16, 100, False, 10)  # A₁₆ = 10
hex_b = LongInt(16, 100, False, 11)  # B₁₆ = 11
print(f"A₁₆ + B₁₆ = {hex_a + hex_b}")  # 15₁₆ = 21 (но в 16-ричной: 15 = F)
print()

# ===== СЛОЖНЫЕ ПРИМЕРЫ =====
print("=" * 60)
print("СЛОЖНЫЕ ПРИМЕРЫ С РАЗНЫМИ СИСТЕМАМИ")
print("=" * 60)

# Сравнение производительности в разных системах
numbers_to_test = [
    ([2], [1, 0, 1, 1], [1, 1, 0]),  # Двоичная
    ([10], [1, 2, 3], [4, 5]),  # Десятичная
    ([16], [10, 11, 12], [5, 15]),  # Шестнадцатеричная
]

for base, num1_digits, num2_digits in numbers_to_test:
    base_val = base[0]
    num1 = LongInt(base_val, 100, False, *num1_digits)
    num2 = LongInt(base_val, 100, False, *num2_digits)

    print(f"\nСистема {base_val}:")
    print(f"{num1} + {num2} = {num1 + num2}")
    print(f"{num1} * {num2} = {num1 * num2}")