
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ієрархія класів для предметної області: Транспортні засоби.

Схема ієрархії:
                    Vehicle (базовий клас)
                   /    |      \      \
                  /     |       \      \
                Car  Motorcycle  Truck  Boat

Базовий клас:
  - Vehicle: name, max_speed, get_travel_info(), __str__()

Підкласи:
  - Car: додає passenger_count, has_trunk
  - Motorcycle: додає has_sidecar, engine_cc
  - Truck: додає cargo_capacity_kg, num_axles
  - Boat: додає propulsion_type, max_depth
"""


class Vehicle:
    """
    Базовий клас для всіх транспортних засобів.

    Атрибути:
        name (str): Назва/модель транспортного засобу
        max_speed (float): Максимальна швидкість (км/год)
    """

    def __init__(self, name, max_speed):
        """
        Ініціалізація базового класу.

        Args:
            name: Назва транспортного засобу
            max_speed: Максимальна швидкість (км/год)
        """
        self.name = name
        self.max_speed = max_speed

    def get_travel_info(self):
        """
        Отримати інформацію про подорож.
        Цей метод буде перевизначений у підкласах (поліморфізм).
        """
        return f"Транспортний засіб: {self.name}, макс. швидкість: {self.max_speed} км/год"

    def calculate_travel_time(self, distance_km):
        """
        Обчислити час подорожі.

        Args:
            distance_km: Відстань у кілометрах

        Returns:
            Час подорожі у годинах
        """
        if self.max_speed == 0:
            return float('inf')
        return distance_km / self.max_speed

    def __str__(self):
        """Рядкове представлення об'єкта."""
        return f"Vehicle(name='{self.name}', max_speed={self.max_speed})"

    def __repr__(self):
        """Представлення для отладки."""
        return self.__str__()


class Car(Vehicle):
    """
    Клас для представлення легкового автомобіля.

    Додаткові атрибути:
        passenger_count (int): Кількість місць для пасажирів
        has_trunk (bool): Чи має багажник
    """

    def __init__(self, name, max_speed, passenger_count, has_trunk):
        """
        Ініціалізація автомобіля.

        Args:
            name: Назва/модель автомобіля
            max_speed: Максимальна швидкість
            passenger_count: Кількість місць
            has_trunk: Наявність багажника
        """
        super().__init__(name, max_speed)
        self.passenger_count = passenger_count
        self.has_trunk = has_trunk

    def get_travel_info(self):
        """
        Поліморфне перевизначення методу батька.
        """
        trunk_info = "має багажник" if self.has_trunk else "немає багажника"
        return (f"Легковий автомобіль: {self.name} (макс. швидкість {self.max_speed} км/год), "
                f"місць: {self.passenger_count}, {trunk_info}")

    def load_passengers(self, num_passengers):
        """
        Завантажити пасажирів.

        Args:
            num_passengers: Кількість пасажирів

        Returns:
            Інформація про завантаження
        """
        if num_passengers > self.passenger_count:
            return f"Не можна завантажити {num_passengers} пасажирів. Місць: {self.passenger_count}"
        return f"Завантажено {num_passengers} з {self.passenger_count} пасажирів"

    def __str__(self):
        return (f"Car(name='{self.name}', max_speed={self.max_speed}, "
                f"passenger_count={self.passenger_count}, has_trunk={self.has_trunk})")


class Motorcycle(Vehicle):
    """
    Клас для представлення мотоцикла.

    Додаткові атрибути:
        has_sidecar (bool): Чи має коляску
        engine_cc (int): Об'єм двигуна (куб. см)
    """

    def __init__(self, name, max_speed, has_sidecar, engine_cc):
        """
        Ініціалізація мотоцикла.

        Args:
            name: Назва/модель мотоцикла
            max_speed: Максимальна швидкість
            has_sidecar: Наявність коляски
            engine_cc: Об'єм двигуна
        """
        super().__init__(name, max_speed)
        self.has_sidecar = has_sidecar
        self.engine_cc = engine_cc

    def get_travel_info(self):
        """
        Поліморфне перевизначення методу батька.
        """
        sidecar_info = "з коляскою" if self.has_sidecar else "без коляски"
        return (f"Мотоцикл: {self.name} (макс. швидкість {self.max_speed} км/год), "
                f"об'єм двигуна {self.engine_cc} см³, {sidecar_info}")

    def perform_wheeling(self):
        """
        Виконати трюк - гальмування на задньому колесі.

        Returns:
            Результат трюку
        """
        if self.has_sidecar:
            return "Не можна гальмувати на задньому колесі з коляскою!"
        return f"{self.name} виконує гальмування на задньому колесі!"

    def __str__(self):
        return (f"Motorcycle(name='{self.name}', max_speed={self.max_speed}, "
                f"has_sidecar={self.has_sidecar}, engine_cc={self.engine_cc})")


class Truck(Vehicle):
    """
    Клас для представлення вантажівки.

    Додаткові атрибути:
        cargo_capacity_kg (float): Вантажопідйомність (кг)
        num_axles (int): Кількість осей
    """

    def __init__(self, name, max_speed, cargo_capacity_kg, num_axles):
        """
        Ініціалізація вантажівки.

        Args:
            name: Назва/модель вантажівки
            max_speed: Максимальна швидкість
            cargo_capacity_kg: Вантажопідйомність
            num_axles: Кількість осей
        """
        super().__init__(name, max_speed)
        self.cargo_capacity_kg = cargo_capacity_kg
        self.num_axles = num_axles

    def get_travel_info(self):
        """
        Поліморфне перевизначення методу батька.
        """
        return (f"Вантажівка: {self.name} (макс. швидкість {self.max_speed} км/год), "
                f"вантажопідйомність {self.cargo_capacity_kg} кг, осей: {self.num_axles}")

    def load_cargo(self, cargo_mass_kg):
        """
        Завантажити вантаж.

        Args:
            cargo_mass_kg: Маса вантажу (кг)

        Returns:
            Результат завантаження
        """
        if cargo_mass_kg > self.cargo_capacity_kg:
            return (f"Вантаж занадто важкий! Вміщується: {self.cargo_capacity_kg} кг, "
                    f"вантаж: {cargo_mass_kg} кг")
        return f"Успішно завантажено {cargo_mass_kg} кг вантажу"

    def __str__(self):
        return (f"Truck(name='{self.name}', max_speed={self.max_speed}, "
                f"cargo_capacity_kg={self.cargo_capacity_kg}, num_axles={self.num_axles})")


class Boat(Vehicle):
    """
    Клас для представлення лодки/судна.

    Додаткові атрибути:
        propulsion_type (str): Тип руху ("весла", "мотор", "вітрила")
        max_depth_m (float): Максимальна глибина (метри)
    """

    def __init__(self, name, max_speed, propulsion_type, max_depth_m):
        """
        Ініціалізація лодки.

        Args:
            name: Назва лодки
            max_speed: Максимальна швидкість
            propulsion_type: Тип руху
            max_depth_m: Максимальна глибина
        """
        super().__init__(name, max_speed)
        self.propulsion_type = propulsion_type
        self.max_depth_m = max_depth_m

    def get_travel_info(self):
        """
        Поліморфне перевизначення методу батька.
        """
        return (f"Лодка: {self.name} (макс. швидкість {self.max_speed} км/год), "
                f"рух: {self.propulsion_type}, макс. глибина: {self.max_depth_m} м")

    def dive(self, depth_m):
        """
        Занурити судно на заданну глибину.

        Args:
            depth_m: Глибина (метри)

        Returns:
            Результат занурення
        """
        if depth_m > self.max_depth_m:
            return f"Занадто глибоко! Макс. глибина: {self.max_depth_m} м"
        return f"Зануренню на {depth_m} метрів успішно виконано"

    def __str__(self):
        return (f"Boat(name='{self.name}', max_speed={self.max_speed}, "
                f"propulsion_type='{self.propulsion_type}', max_depth_m={self.max_depth_m})")


def demonstrate_inheritance():
    """Демонстрація ієрархії та успадкування."""
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦІЯ ІЄРАРХІЇ КЛАСІВ")
    print("="*80)

    print("\nСХЕМА ІЄРАРХІЇ:")
    print("""
                        Vehicle (базовий клас)
                       /    |      \\      \\
                      /     |       \\      \\
                    Car  Motorcycle  Truck  Boat
    """)

    print("\nБазовий клас Vehicle:")
    print("  Атрибути: name, max_speed")
    print("  Методи: get_travel_info(), calculate_travel_time(), __str__()")

    print("\nПідклас Car:")
    print("  Додаткові атрибути: passenger_count, has_trunk")
    print("  Перевизначений метод: get_travel_info()")
    print("  Новий метод: load_passengers()")

    print("\nПідклас Motorcycle:")
    print("  Додаткові атрибути: has_sidecar, engine_cc")
    print("  Перевизначений метод: get_travel_info()")
    print("  Новий метод: perform_wheeling()")

    print("\nПідклас Truck:")
    print("  Додаткові атрибути: cargo_capacity_kg, num_axles")
    print("  Перевизначений метод: get_travel_info()")
    print("  Новий метод: load_cargo()")

    print("\nПідклас Boat:")
    print("  Додаткові атрибути: propulsion_type, max_depth_m")
    print("  Перевизначений метод: get_travel_info()")
    print("  Новий метод: dive()")


def demonstrate_polymorphism():
    """Демонстрація поліморфізму."""
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦІЯ ПОЛІМОРФІЗМУ")
    print("="*80)

    # Створення об'єктів різних типів
    vehicles = [
        Car("Toyota Camry", 180, 5, True),
        Motorcycle("Harley-Davidson", 200, False, 1750),
        Truck("Volvo FH16", 120, 25000, 3),
        Boat("Яхта Дельфін", 40, "вітрила", 100),
        Car("Honda Civic", 190, 5, True),
        Motorcycle("Yamaha YZF-R1", 230, True, 1000),
    ]

    print("\nСписок об'єктів:")
    for i, vehicle in enumerate(vehicles, 1):
        print(f"  {i}. {vehicle}")

    print("\n" + "-"*80)
    print("ПОЛІМОРФНИЙ ОБХІД - виклик get_travel_info():")
    print("-"*80)

    for vehicle in vehicles:
        print(f"\n{vehicle.get_travel_info()}")

    print("\n" + "-"*80)
    print("ОБЧИСЛЕННЯ ЧАСУ ПОДОРОЖІ (1000 км):")
    print("-"*80)

    distance = 1000
    for vehicle in vehicles:
        travel_time = vehicle.calculate_travel_time(distance)
        if travel_time == float('inf'):
            print(f"{vehicle.name}: не можливо (швидкість 0)")
        else:
            hours = int(travel_time)
            minutes = int((travel_time - hours) * 60)
            print(f"{vehicle.name}: {distance} км за {hours}г {minutes}хв (при макс. швидкості)")


def demonstrate_type_checking():
    """Демонстрація перевірки типів (isinstance, issubclass)."""
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦІЯ isinstance() І issubclass()")
    print("="*80)

    # Створення об'єктів
    car = Car("Tesla Model 3", 225, 5, True)
    motorcycle = Motorcycle("BMW S1000RR", 250, False, 999)
    truck = Truck("MAN TGX", 130, 30000, 4)
    boat = Boat("Катамаран", 50, "мотор", 500)

    vehicles = [car, motorcycle, truck, boat]

    print("\nПЕРЕВІРКА isinstance():")
    print("\nОб'єкти та їх типи:")

    for vehicle in vehicles:
        print(f"\n{vehicle.name}:")
        print(f"  isinstance(obj, Car): {isinstance(vehicle, Car)}")
        print(f"  isinstance(obj, Motorcycle): {isinstance(vehicle, Motorcycle)}")
        print(f"  isinstance(obj, Truck): {isinstance(vehicle, Truck)}")
        print(f"  isinstance(obj, Boat): {isinstance(vehicle, Boat)}")
        print(f"  isinstance(obj, Vehicle): {isinstance(vehicle, Vehicle)}")

    print("\n" + "-"*80)
    print("ПЕРЕВІРКА issubclass():")
    print("-"*80)

    classes = [Car, Motorcycle, Truck, Boat, Vehicle]

    print("\nВідносини між класами:")
    for cls in classes:
        print(f"\n{cls.__name__}:")
        print(f"  issubclass(Car, Vehicle): {issubclass(Car, Vehicle)}")
        print(f"  issubclass(Motorcycle, Vehicle): {issubclass(Motorcycle, Vehicle)}")
        print(f"  issubclass(Truck, Vehicle): {issubclass(Truck, Vehicle)}")
        print(f"  issubclass(Boat, Vehicle): {issubclass(Boat, Vehicle)}")
        print(f"  issubclass(Vehicle, Vehicle): {issubclass(Vehicle, Vehicle)}")
        print(f"  issubclass(Car, Car): {issubclass(Car, Car)}")


def demonstrate_method_usage():
    """Демонстрація використання спеціалізованих методів."""
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦІЯ СПЕЦІАЛІЗОВАНИХ МЕТОДІВ")
    print("="*80)

    print("\n--- Car.load_passengers() ---")
    car = Car("BMW 5 Series", 220, 5, True)
    print(car.get_travel_info())
    print(car.load_passengers(4))
    print(car.load_passengers(6))

    print("\n--- Motorcycle.perform_wheeling() ---")
    moto1 = Motorcycle("Kawasaki Ninja", 250, False, 650)
    print(moto1.get_travel_info())
    print(moto1.perform_wheeling())

    moto2 = Motorcycle("Ural", 120, True, 750)
    print("\n" + moto2.get_travel_info())
    print(moto2.perform_wheeling())

    print("\n--- Truck.load_cargo() ---")
    truck = Truck("Scania R440", 135, 20000, 3)
    print(truck.get_travel_info())
    print(truck.load_cargo(15000))
    print(truck.load_cargo(25000))

    print("\n--- Boat.dive() ---")
    boat = Boat("Підводний батискаф", 30, "мотор", 5000)
    print(boat.get_travel_info())
    print(boat.dive(1000))
    print(boat.dive(6000))


def demonstrate_inheritance_chain():
    """Демонстрація ланцюга успадкування."""
    print("\n" + "="*80)
    print("ДЕМОНСТРАЦІЯ ЛАНЦЮГА УСПАДКУВАННЯ (MRO)")
    print("="*80)

    print("\nМетод Resolution Order (MRO) для кожного класу:")

    classes = [Car, Motorcycle, Truck, Boat]

    for cls in classes:
        print(f"\n{cls.__name__}:")
        print(f"  MRO: {[c.__name__ for c in cls.__mro__]}")

    print("\n" + "-"*80)
    print("ВИЗИТКА super().__init__():")
    print("-"*80)

    car = Car("Avantime", 190, 5, True)
    print("\nПри виклику Car.__init__():")
    print("  1. super().__init__(name, max_speed)")
    print("     -> Vehicle.__init__() встановлює name, max_speed")
    print("  2. self.passenger_count = passenger_count")
    print("  3. self.has_trunk = has_trunk")
    print("\nРезультат:")
    print(f"  car.name = {car.name}")
    print(f"  car.max_speed = {car.max_speed}")
    print(f"  car.passenger_count = {car.passenger_count}")
    print(f"  car.has_trunk = {car.has_trunk}")


def main():
    """Головна функція."""
    print("\n" + "="*80)
    print("ІЄРАРХІЯ КЛАСІВ: ТРАНСПОРТНІ ЗАСОБИ")
    print("="*80)

    demonstrate_inheritance()
    demonstrate_polymorphism()
    demonstrate_type_checking()
    demonstrate_method_usage()
    demonstrate_inheritance_chain()

    print("\n" + "="*80)
    print("ВИСНОВКИ")
    print("="*80)

    print("""
1. УСПАДКУВАННЯ (Inheritance):
   - Базовий клас Vehicle визначає спільну поведінку
   - Кожен підклас добавляє свою специфіку
   - super().__init__() забезпечує правильну ініціалізацію

2. ПОЛІМОРФІЗМ (Polymorphism):
   - Однойменний метод get_travel_info() працює по-різному для кожного типу
   - Один цикл обходить об'єкти різних типів
   - Правильна версія методу викликається в залежності тип об'єкта

3. ІНКАПСУЛЯЦІЯ (Encapsulation):
   - Атрибути та методи групуються у класи
   - Кожна відповідає за свою семантику

4. МОДУЛЬНІСТЬ:
   - Легко додати новий тип (наприклад, Helicopter)
   - Не потрібно змінювати існуючий код
   - Кожен клас має чітку відповідальність

5. ДОТРИМАННЯ ПРАВИЛ OOP:
   - Кожен підклас має власні атрибути
   - Кожен підклас перевизначає хоча б один метод батька
   - Демонстрація поліморфного обходу
   - Використання isinstance() і issubclass()
    """)

    print("\n" + "="*80)
    print("Програма завершена.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
