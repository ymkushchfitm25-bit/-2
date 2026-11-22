
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Клас Vector3D - тривимірний вектор з магічними методами.

Демонструє операції над векторами:
- Додавання, віднімання, множення
- Порівняння за довжиною
- Скалярне (dot product) та векторне (cross product) множення
- Доступ до компонент
"""

import math


class Vector3D:
    """
    Клас для представлення тривимірного вектора.

    Параметри:
        x, y, z: Координати вектора
    """

    def __init__(self, x=0, y=0, z=0):
        """Ініціалізація вектора."""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    # ========== ПРЕДСТАВЛЕННЯ ==========

    def __str__(self):
        """
        Людиночитне представлення вектора.
        Використовується print() та str()
        """
        return f"Vector3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __repr__(self):
        """
        Однозначне представлення для отладки.
        Повинно містити всін інформацію для відтворення об'єкта
        """
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    # ========== АРИФМЕТИЧНІ ОПЕРАЦІЇ ==========

    def __add__(self, other):
        """
        Додавання двох векторів: v1 + v2
        Магічний метод для оператора +
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"can't add Vector3D and {type(other).__name__}")
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """
        Віднімання векторів: v1 - v2
        Магічний метод для оператора -
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"can't subtract Vector3D and {type(other).__name__}")
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """
        Множення вектора на скаляр: v * 2
        Магічний метод для оператора *

        Повертає новий вектор з помноженими координатами
        """
        if isinstance(scalar, Vector3D):
            # Якщо намагаємось помножити два вектори, то це скалярне множення
            return self.dot_product(scalar)

        try:
            scalar = float(scalar)
        except (TypeError, ValueError):
            raise TypeError(f"can't multiply Vector3D by {type(scalar).__name__}")

        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        """
        Множення скаляра на вектор: 2 * v
        Магічний метод для оператора * (обернений порядок)
        """
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        """
        Ділення вектора на скаляр: v / 2
        Магічний метод для оператора /
        """
        try:
            scalar = float(scalar)
        except (TypeError, ValueError):
            raise TypeError(f"can't divide Vector3D by {type(scalar).__name__}")

        if scalar == 0:
            raise ValueError("can't divide vector by zero")

        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __neg__(self):
        """
        Протилежний вектор: -v
        Магічний метод для унарного оператора -
        """
        return Vector3D(-self.x, -self.y, -self.z)

    # ========== ПОРІВНЯННЯ ==========

    def __eq__(self, other):
        """
        Рівність векторів: v1 == v2
        Магічний метод для оператора ==

        Повертає True, якщо всі координати рівні (з точністю до epsilon)
        """
        if not isinstance(other, Vector3D):
            return False

        epsilon = 1e-9
        return (abs(self.x - other.x) < epsilon and
                abs(self.y - other.y) < epsilon and
                abs(self.z - other.z) < epsilon)

    def __ne__(self, other):
        """
        Нерівність векторів: v1 != v2
        Магічний метод для оператора !=
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Порівняння за довжиною: v1 < v2
        Магічний метод для оператора <

        v1 < v2 означає, що довжина v1 менше довжини v2
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"'<' not supported between instances of Vector3D and {type(other).__name__}")
        return abs(self) < abs(other)

    def __le__(self, other):
        """
        Менше або дорівнює за довжиною: v1 <= v2
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"'<=' not supported between instances of Vector3D and {type(other).__name__}")
        return abs(self) <= abs(other)

    def __gt__(self, other):
        """
        Більше за довжиною: v1 > v2
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"'>' not supported between instances of Vector3D and {type(other).__name__}")
        return abs(self) > abs(other)

    def __ge__(self, other):
        """
        Більше або дорівнює за довжиною: v1 >= v2
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"'>=' not supported between instances of Vector3D and {type(other).__name__}")
        return abs(self) >= abs(other)

    # ========== КОНТЕЙНЕР / ВИКЛИК ==========

    def __len__(self):
        """
        Кількість компонент вектора: len(v)
        Магічний метод для функції len()

        Завжди повертає 3 (тривимірний вектор)
        """
        return 3

    def __getitem__(self, index):
        """
        Доступ до компоненти за індексом: v[0], v[1], v[2]
        Магічний метод для оператора []

        Індекси: 0 -> x, 1 -> y, 2 -> z
        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector3D index out of range")

    def __setitem__(self, index, value):
        """
        Встановлення компоненти за індексом: v[0] = 5
        Магічний метод для присвоєння через []
        """
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise TypeError(f"can't set vector component to {type(value).__name__}")

        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Vector3D index out of range")

    def __abs__(self):
        """
        Довжина (модуль) вектора: abs(v)
        Магічний метод для функції abs()

        Повертає ||v|| = sqrt(x^2 + y^2 + z^2)
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __hash__(self):
        """
        Хеш вектора для використання у множинах та словниках.
        Дозволяє використовувати вектори як ключи.
        """
        return hash((round(self.x, 10), round(self.y, 10), round(self.z, 10)))

    # ========== ДОДАТКОВІ ОПЕРАЦІЇ ==========

    def dot_product(self, other):
        """
        Скалярне (точкове) множення: v1 . v2

        Результат: x1*x2 + y1*y2 + z1*z2 (скаляр, не вектор)
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"can't compute dot product with {type(other).__name__}")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        """
        Векторне (хресне) множення: v1 x v2

        Результат: новий вектор перпендикулярний до обох
        """
        if not isinstance(other, Vector3D):
            raise TypeError(f"can't compute cross product with {type(other).__name__}")

        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def normalize(self):
        """Отримати нормалізований вектор (довжина = 1)."""
        length = abs(self)
        if length == 0:
            raise ValueError("can't normalize zero vector")
        return self / length

    def distance_to(self, other):
        """Відстань до іншого вектора."""
        if not isinstance(other, Vector3D):
            raise TypeError(f"can't compute distance to {type(other).__name__}")
        return abs(self - other)


def print_section(title):
    """Виведення розділювача."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def demonstrate_representation():
    """Демонстрація методів представлення."""
    print_section("1. ПРЕДСТАВЛЕННЯ (__str__ та __repr__)")

    v = Vector3D(3, 4, 5)

    print("\n--- __str__() через print() ---")
    print(f"print(v) -> {v}")
    print(f"str(v)   -> {str(v)}")

    print("\n--- __repr__() через repr() ---")
    print(f"repr(v)  -> {repr(v)}")
    print(f"v        -> {repr(v)}")  # При введенні в інтерпретаторі

    print("\nРізниця:")
    print("  __str__(): людиночитне, з округленням")
    print("  __repr__(): точне, для отладки та відтворення")


def demonstrate_arithmetic():
    """Демонстрація арифметичних операцій."""
    print_section("2. АРИФМЕТИЧНІ ОПЕРАЦІЇ (+, -, *, /)")

    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(2, 3, 4)

    print(f"\nv1 = {v1}")
    print(f"v2 = {v2}")

    print("\n--- Додавання: v1 + v2 (__add__) ---")
    v_sum = v1 + v2
    print(f"v1 + v2 = {v_sum}")
    print(f"Тип результату: {type(v_sum).__name__}")

    print("\n--- Віднімання: v1 - v2 (__sub__) ---")
    v_diff = v1 - v2
    print(f"v1 - v2 = {v_diff}")

    print("\n--- Множення на скаляр: v1 * 2 (__mul__) ---")
    v_mult = v1 * 2
    print(f"v1 * 2 = {v_mult}")

    print("\n--- Множення скаляра на вектор: 3 * v1 (__rmul__) ---")
    v_rmult = 3 * v1
    print(f"3 * v1 = {v_rmult}")

    print("\n--- Ділення на скаляр: v1 / 2 (__truediv__) ---")
    v_div = v1 / 2
    print(f"v1 / 2 = {v_div}")

    print("\n--- Унарний мінус: -v1 (__neg__) ---")
    v_neg = -v1
    print(f"-v1 = {v_neg}")


def demonstrate_comparison():
    """Демонстрація операцій порівняння."""
    print_section("3. ОПЕРАЦІЇ ПОРІВНЯННЯ (==, <, >, <=, >=)")

    v1 = Vector3D(3, 4, 0)  # Довжина 5
    v2 = Vector3D(5, 0, 0)  # Довжина 5
    v3 = Vector3D(1, 2, 3)  # Довжина sqrt(14) ≈ 3.74

    print(f"\nv1 = {v1}  |v1| = {abs(v1):.2f}")
    print(f"v2 = {v2}  |v2| = {abs(v2):.2f}")
    print(f"v3 = {v3}  |v3| = {abs(v3):.2f}")

    print("\n--- Рівність: v1 == v2 (__eq__) ---")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 == v1: {v1 == v1}")
    print("Порівнюються координати (не довжини)")

    print("\n--- Лексикографічне порівняння довжин ---")
    print(f"v1 < v2  (__lt__):  {v1 < v2} (довжина v1 < довжина v2?)")
    print(f"v3 < v1  (__lt__):  {v3 < v1} (довжина v3 < довжина v1?)")
    print(f"v1 > v3  (__gt__):  {v1 > v3} (довжина v1 > довжина v3?)")
    print(f"v1 <= v2 (__le__):  {v1 <= v2} (довжина v1 <= довжина v2?)")
    print(f"v1 != v3 (__ne__):  {v1 != v3}")


def demonstrate_container():
    """Демонстрація контейнерних операцій."""
    print_section("4. КОНТЕЙНЕРНІ ОПЕРАЦІЇ (__len__, __getitem__, __abs__)")

    v = Vector3D(3, 4, 5)

    print(f"\nВектор: v = {v}")

    print("\n--- Кількість компонент: len(v) (__len__) ---")
    print(f"len(v) = {len(v)}")
    print("Завжди повертає 3 для тривимірного вектора")

    print("\n--- Доступ до компонент: v[i] (__getitem__) ---")
    print(f"v[0] = {v[0]}  (x-компонента)")
    print(f"v[1] = {v[1]}  (y-компонента)")
    print(f"v[2] = {v[2]}  (z-компонента)")

    print("\n--- Встановлення компоненти: v[i] = value (__setitem__) ---")
    v_copy = Vector3D(3, 4, 5)
    print(f"v_copy = {v_copy}")
    v_copy[1] = 10
    print(f"v_copy[1] = 10  ->  v_copy = {v_copy}")

    print("\n--- Довжина вектора: abs(v) (__abs__) ---")
    print(f"v = {v}")
    print(f"abs(v) = {abs(v):.4f}")
    print(f"Обчислення: sqrt(3² + 4² + 5²) = sqrt(50) = {abs(v):.4f}")


def demonstrate_advanced():
    """Демонстрація додаткових операцій."""
    print_section("5. ДОДАТКОВІ ОПЕРАЦІЇ (скалярне, векторне множення)")

    v1 = Vector3D(1, 0, 0)  # Одиничний вектор по X
    v2 = Vector3D(0, 1, 0)  # Одиничний вектор по Y
    v3 = Vector3D(1, 1, 1)

    print(f"\nv1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v3 = {v3}")

    print("\n--- Скалярне множення: v1.dot_product(v2) ---")
    dot_12 = v1.dot_product(v2)
    dot_13 = v1.dot_product(v3)
    print(f"v1 · v2 = {dot_12}  (перпендикулярні, результат 0)")
    print(f"v1 · v3 = {dot_13}  (мають спільну компоненту)")

    print("\n--- Векторне множення: v1.cross_product(v2) ---")
    cross = v1.cross_product(v2)
    print(f"v1 × v2 = {cross}")
    print(f"Результат перпендикулярний до обох векторів")

    print("\n--- Нормалізація: v.normalize() ---")
    v_norm = v3.normalize()
    print(f"v3 = {v3}  |v3| = {abs(v3):.4f}")
    print(f"normalize(v3) = {v_norm}")
    print(f"|normalize(v3)| = {abs(v_norm):.4f}  (завжди 1)")

    print("\n--- Відстань між точками: v1.distance_to(v3) ---")
    dist = v1.distance_to(v3)
    print(f"distance(v1, v3) = {dist:.4f}")


def demonstrate_type_safety():
    """Демонстрація типобезпеки."""
    print_section("6. ТИПОБЕЗПЕКА (обробка помилок)")

    v = Vector3D(1, 2, 3)

    print(f"\nВектор: v = {v}")

    print("\n--- Спроба додавання вектора до числа ---")
    try:
        result = v + 5
    except TypeError as e:
        print(f"ПОМИЛКА: {e}")

    print("\n--- Спроба множення на неправильний тип ---")
    try:
        result = v * "abc"
    except TypeError as e:
        print(f"ПОМИЛКА: {e}")

    print("\n--- Спроба порівняння з іншим типом ---")
    try:
        result = v < 5
    except TypeError as e:
        print(f"ПОМИЛКА: {e}")

    print("\n--- Спроба доступу до індексу за межами ---")
    try:
        value = v[5]
    except IndexError as e:
        print(f"ПОМИЛКА: {e}")


def demonstrate_magic_methods_table():
    """Таблиця відповідності магічних методів."""
    print_section("ТАБЛИЦЯ МАГІЧНИХ МЕТОДІВ")

    table_data = [
        ("__str__", "str(v), print(v)", "Людиночитне представлення"),
        ("__repr__", "repr(v)", "Однозначне представлення"),
        ("__add__", "v1 + v2", "Додавання векторів"),
        ("__sub__", "v1 - v2", "Віднімання векторів"),
        ("__mul__", "v * 2, 3 * v", "Множення на скаляр"),
        ("__rmul__", "3 * v", "Множення скаляра на вектор"),
        ("__truediv__", "v / 2", "Ділення на скаляр"),
        ("__neg__", "-v", "Унарний мінус (протилежний вектор)"),
        ("__eq__", "v1 == v2", "Рівність"),
        ("__ne__", "v1 != v2", "Нерівність"),
        ("__lt__", "v1 < v2", "Менше за довжиною"),
        ("__le__", "v1 <= v2", "Менше або дорівнює за довжиною"),
        ("__gt__", "v1 > v2", "Більше за довжиною"),
        ("__ge__", "v1 >= v2", "Більше або дорівнює за довжиною"),
        ("__len__", "len(v)", "Кількість компонент"),
        ("__getitem__", "v[0], v[1]", "Доступ до компоненти"),
        ("__setitem__", "v[0] = 5", "Встановлення компоненти"),
        ("__abs__", "abs(v)", "Довжина (модуль) вектора"),
        ("__hash__", "hash(v)", "Хеш для множин/словників"),
    ]

    print(f"\n{'Магічний метод':<20} {'Оператор/Функція':<25} {'Описання':<40}")
    print("-" * 85)

    for method, operator, description in table_data:
        print(f"{method:<20} {operator:<25} {description:<40}")


def main():
    """Головна функція."""
    print("\n" + "="*70)
    print("КЛАС Vector3D З МАГІЧНИМИ МЕТОДАМИ")
    print("Демонстрація перевантаження операторів")
    print("="*70)

    demonstrate_representation()
    demonstrate_arithmetic()
    demonstrate_comparison()
    demonstrate_container()
    demonstrate_advanced()
    demonstrate_type_safety()
    demonstrate_magic_methods_table()

    print_section("ВИСНОВКИ")

    print("""
Магічні методи дозволяють:

1. ПРЕДСТАВЛЕННЯ:
   - __str__() для зручного вивода користувачу
   - __repr__() для точного представлення розробнику

2. АРИФМЕТИЧНІ ОПЕРАЦІЇ:
   - Вектор + Вектор = Вектор
   - Вектор * Число = Вектор
   - Число * Вектор = Вектор
   - Вектор / Число = Вектор

3. ПОРІВНЯННЯ:
   - Порівняння за довжиною вектора
   - Рівність за координатами

4. КОНТЕЙНЕР:
   - Доступ до компонент через індекс
   - Кількість компонент
   - Довжина (модуль) вектора

5. ТИПОБЕЗПЕКА:
   - Перевірка типів в операціях
   - Вивід зрозумілих повідомлень про помилки

6. ВИКОРИСТАННЯ В МІСТКИХ СТРУКТУРАХ:
   - Вектори можна додавати в множини (через __hash__)
   - Вектори можна використовувати як ключі в словниках
    """)

    print("="*70)
    print("Програма завершена.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
