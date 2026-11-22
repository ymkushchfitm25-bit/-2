#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Клас BankAccount - модель банківського рахунку з контрольованим доступом.

Демонструє:
- Приватні атрибути (__balance)
- Захищені атрибути (_transactions)
- @property з getter та setter з валідацією
- Обчислювальні властивості (read-only)
- Name mangling
"""

import re
from datetime import datetime


class BankAccount:
    """
    Клас для представлення банківського рахунку.

    Приватні атрибути __:
    - __balance: залишок коштів (доступ тільки через @property)
    - __pin: PIN-код (4 цифри)

    Захищені атрибути _:
    - _transactions: історія транзакцій
    - _owner_email: email власника
    """

    def __init__(self, account_number, owner_name, owner_email, initial_balance=0, pin="0000"):
        """
        Ініціалізація банківського рахунку.

        Args:
            account_number: Номер рахунку
            owner_name: ПІБ власника
            owner_email: Email власника
            initial_balance: Початковий баланс (за замовчуванням 0)
            pin: PIN-код (за замовчуванням "0000")
        """
        self.account_number = account_number
        self.owner_name = owner_name

        # Валідація та встановлення email (захищений атрибут)
        self._validate_email(owner_email)
        self._owner_email = owner_email

        # Валідація та встановлення приватного баланса через setter
        self.__balance = 0  # Спочатку 0
        self.balance = initial_balance  # Встановлення через setter з валідацією

        # Валідація та встановлення PIN (приватний атрибут)
        self._validate_pin(pin)
        self.__pin = pin

        # Історія транзакцій (захищений атрибут)
        self._transactions = []

        # Процентна ставка (захищена)
        self._interest_rate = 0.05  # 5% на рік

        # Записуємо початкову транзакцію
        if initial_balance > 0:
            self._transactions.append({
                'date': datetime.now(),
                'type': 'initial',
                'amount': initial_balance,
                'description': 'Відкриття рахунку'
            })

    # ========== ВАЛІДАЦІЯ ==========

    @staticmethod
    def _validate_email(email):
        """
        Валідація email адреси.

        Args:
            email: Email для перевірки

        Raises:
            ValueError: Якщо email неправильного формату
            TypeError: Якщо email не рядок
        """
        if not isinstance(email, str):
            raise TypeError(f"Email повинен бути рядком, отримано {type(email).__name__}")

        # Простий regex для перевірки email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError(f"Email '{email}' має неправильний формат")

    @staticmethod
    def _validate_pin(pin):
        """
        Валідація PIN-коду.

        Args:
            pin: PIN-код для перевірки

        Raises:
            ValueError: Якщо PIN не 4 цифри
            TypeError: Якщо PIN не рядок
        """
        if not isinstance(pin, str):
            raise TypeError(f"PIN повинен бути рядком, отримано {type(pin).__name__}")

        if not pin.isdigit() or len(pin) != 4:
            raise ValueError(f"PIN повинен містити рівно 4 цифри, отримано '{pin}'")

    @staticmethod
    def _validate_amount(amount):
        """
        Валідація суми коштів.

        Args:
            amount: Сума для перевірки

        Raises:
            ValueError: Якщо сума невалідна
            TypeError: Якщо сума не число
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Сума повинна бути числом, отримано {type(amount).__name__}")

        if amount < 0:
            raise ValueError(f"Сума не може бути від'ємною: {amount}")

        if amount > 10_000_000:
            raise ValueError(f"Сума занадто велика (максимум 10 млн): {amount}")

    # ========== PROPERTY: BALANCE (приватний атрибут) ==========

    @property
    def balance(self):
        """
        Getter для баланса.
        Доступ до приватного атрибута __balance через @property
        """
        return self.__balance

    @balance.setter
    def balance(self, value):
        """
        Setter для баланса з валідацією.

        Args:
            value: Новий баланс

        Raises:
            ValueError: Якщо баланс невалідний
            TypeError: Якщо передано неправильний тип
        """
        # Валідація суми
        self._validate_amount(value)

        # Додаткова перевірка: баланс не може бути від'ємним
        if value < 0:
            raise ValueError(f"Баланс не може бути від'ємним: {value}")

        old_balance = self.__balance
        self.__balance = value

        # Записуємо транзакцію, якщо це зміна
        if value != old_balance:
            self._transactions.append({
                'date': datetime.now(),
                'type': 'balance_adjustment',
                'amount': value - old_balance,
                'description': f'Зміна баланса з {old_balance:.2f} на {value:.2f}'
            })

    # ========== PROPERTY: EMAIL (захищений атрибут) ==========

    @property
    def owner_email(self):
        """Getter для email власника (захищений атрибут)."""
        return self._owner_email

    @owner_email.setter
    def owner_email(self, value):
        """
        Setter для email з валідацією.

        Args:
            value: Новий email

        Raises:
            ValueError: Якщо email неправильного формату
            TypeError: Якщо email не рядок
        """
        self._validate_email(value)
        old_email = self._owner_email
        self._owner_email = value

        # Записуємо событие
        self._transactions.append({
            'date': datetime.now(),
            'type': 'email_change',
            'amount': 0,
            'description': f"Email змінено з '{old_email}' на '{value}'"
        })

    # ========== PROPERTY: PIN (приватний атрибут) ==========

    @property
    def pin(self):
        """
        Getter для PIN.
        Для безпеки повертає замасковану версію.
        """
        return "*" * len(self.__pin)

    @pin.setter
    def pin(self, value):
        """
        Setter для PIN з валідацією.

        Args:
            value: Новий PIN

        Raises:
            ValueError: Якщо PIN неправильного формату
            TypeError: Якщо PIN не рядок
        """
        self._validate_pin(value)
        self.__pin = value

        self._transactions.append({
            'date': datetime.now(),
            'type': 'pin_change',
            'amount': 0,
            'description': 'PIN змінено'
        })

    # ========== ОБЧИСЛЮВАЛЬНІ ВЛАСТИВОСТІ (read-only) ==========

    @property
    def transaction_count(self):
        """
        Обчислювальна властивість: кількість транзакцій.
        Read-only - немає setter.
        """
        return len(self._transactions)

    @property
    def accrued_interest(self):
        """
        Обчислювальна властивість: нараховані відсотки на рік.
        Read-only - обчислюється з поточного баланса.
        """
        return self.__balance * self._interest_rate

    @property
    def account_info(self):
        """
        Обчислювальна властивість: повна інформація про рахунок.
        Read-only - обчислюється з кількох атрибутів.
        """
        return {
            'account_number': self.account_number,
            'owner_name': self.owner_name,
            'email': self._owner_email,
            'balance': self.__balance,
            'interest_rate': f"{self._interest_rate * 100:.1f}%",
            'accrued_interest': self.accrued_interest,
            'transactions': self.transaction_count
        }

    # ========== МЕТОДИ ОПЕРАЦІЙ ==========

    def deposit(self, amount):
        """Поповнення рахунку."""
        self._validate_amount(amount)

        if amount == 0:
            raise ValueError("Сума поповнення не може бути нулем")

        self.__balance += amount

        self._transactions.append({
            'date': datetime.now(),
            'type': 'deposit',
            'amount': amount,
            'description': f'Поповнення на {amount:.2f}'
        })

        return self.__balance

    def withdraw(self, amount):
        """Зняття коштів."""
        self._validate_amount(amount)

        if amount == 0:
            raise ValueError("Сума зняття не може бути нулем")

        if amount > self.__balance:
            raise ValueError(
                f"Недостатньо коштів. Баланс: {self.__balance:.2f}, "
                f"запит на зняття: {amount:.2f}"
            )

        self.__balance -= amount

        self._transactions.append({
            'date': datetime.now(),
            'type': 'withdraw',
            'amount': -amount,
            'description': f'Зняття {amount:.2f}'
        })

        return self.__balance

    def transfer(self, other_account, amount):
        """Переказ коштів на інший рахунок."""
        if not isinstance(other_account, BankAccount):
            raise TypeError("Одержувач повинен бути BankAccount")

        # Зняття з поточного рахунку
        self.withdraw(amount)

        # Поповнення іншого рахунку
        other_account.deposit(amount)

        self._transactions[-1]['description'] = f'Переказ {amount:.2f} на {other_account.account_number}'

    def print_transactions(self):
        """Вивести історію транзакцій."""
        print(f"\nІсторія транзакцій для рахунку {self.account_number}:")
        print(f"{'Дата':<20} {'Тип':<20} {'Сума':<12} {'Опис':<40}")
        print("-" * 92)

        for transaction in self._transactions:
            date_str = transaction['date'].strftime("%Y-%m-%d %H:%M:%S")
            amount_str = f"{transaction['amount']:>10.2f}"
            print(f"{date_str:<20} {transaction['type']:<20} {amount_str:<12} {transaction['description']:<40}")

    def __str__(self):
        """Рядкове представлення."""
        return (f"BankAccount(number={self.account_number}, "
                f"owner={self.owner_name}, "
                f"balance={self.__balance:.2f})")

    def __repr__(self):
        """Представлення для отладки."""
        return self.__str__()


def print_section(title):
    """Виведення розділювача."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")


def demonstrate_valid_creation():
    """Демонстрація коректного створення."""
    print_section("1. КОРЕКТНЕ СТВОРЕННЯ РАХУНКУ")

    try:
        account = BankAccount(
            account_number="123456789",
            owner_name="Іван Петренко",
            owner_email="ivan.petren@example.com",
            initial_balance=1000.00,
            pin="1234"
        )

        print(f"\nРахунок успішно створено:")
        print(f"  Номер: {account.account_number}")
        print(f"  Власник: {account.owner_name}")
        print(f"  Email: {account.owner_email}")
        print(f"  Баланс: {account.balance:.2f}")
        print(f"  PIN (замаскований): {account.pin}")
        print(f"\nРахунок: {account}")

    except Exception as e:
        print(f"Помилка: {e}")


def demonstrate_invalid_email():
    """Демонстрація спроби встановлення неправильного email."""
    print_section("2. СПРОБА ВСТАНОВЛЕННЯ НЕПРАВИЛЬНОГО EMAIL")

    account = BankAccount(
        account_number="123456789",
        owner_name="Іван Петренко",
        owner_email="ivan@example.com",
        initial_balance=1000.00
    )

    print(f"\nПочатковий email: {account.owner_email}")

    # Спроба 1: Email без @
    print("\nСпроба 1: Встановити email без '@'")
    try:
        account.owner_email = "invalid_email"
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    # Спроба 2: Email не рядок
    print("\nСпроба 2: Встановити email як число")
    try:
        account.owner_email = 12345
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    print(f"\nEmail залишився без змін: {account.owner_email}")


def demonstrate_invalid_balance():
    """Демонстрація спроб встановлення неправильного баланса."""
    print_section("3. СПРОБА ВСТАНОВЛЕННЯ НЕПРАВИЛЬНОГО БАЛАНСА")

    account = BankAccount(
        account_number="987654321",
        owner_name="Марія Коваленко",
        owner_email="maria@example.com",
        initial_balance=500.00
    )

    print(f"\nПочатковий баланс: {account.balance:.2f}")

    # Спроба 1: Від'ємний баланс
    print("\nСпроба 1: Встановити від'ємний баланс")
    try:
        account.balance = -100
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    # Спроба 2: Баланс не числом
    print("\nСпроба 2: Встановити баланс як рядок")
    try:
        account.balance = "1000"
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    # Спроба 3: Баланс занадто великий
    print("\nСпроба 3: Встановити баланс занадто великий")
    try:
        account.balance = 11_000_000
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    print(f"\nБаланс залишився без змін: {account.balance:.2f}")


def demonstrate_invalid_pin():
    """Демонстрація спроб встановлення неправильного PIN."""
    print_section("4. СПРОБА ВСТАНОВЛЕННЯ НЕПРАВИЛЬНОГО PIN")

    account = BankAccount(
        account_number="555666777",
        owner_name="Петро Сидоренко",
        owner_email="petro@example.com",
        initial_balance=2000.00,
        pin="1111"
    )

    print(f"\nПочатковий PIN (замаскований): {account.pin}")

    # Спроба 1: PIN не 4 цифри
    print("\nСпроба 1: Встановити PIN з 3 цифр")
    try:
        account.pin = "123"
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    # Спроба 2: PIN містить букви
    print("\nСпроба 2: Встановити PIN з букв")
    try:
        account.pin = "abcd"
        print("  Успіх (помилка, не повинна бути)")
    except ValueError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")
    except TypeError as e:
        print(f"  ПЕРЕХОПЛЕНА ПОМИЛКА: {e}")

    print(f"\nPIN залишився без змін: {account.pin}")


def demonstrate_calculated_properties():
    """Демонстрація обчислювальних властивостей."""
    print_section("5. ОБЧИСЛЮВАЛЬНІ ВЛАСТИВОСТІ (read-only)")

    account = BankAccount(
        account_number="111222333",
        owner_name="Олена Іванівна",
        owner_email="olena@example.com",
        initial_balance=5000.00,
        pin="2222"
    )

    print(f"\nРахунок: {account}")

    # Обчислювальна властивість 1: transaction_count
    print(f"\nОбчислювальна властивість 1: transaction_count")
    print(f"  account.transaction_count = {account.transaction_count}")
    print(f"  (читає з _transactions - захищеного атрибута)")

    # Обчислювальна властивість 2: accrued_interest
    print(f"\nОбчислювальна властивість 2: accrued_interest")
    print(f"  account.accrued_interest = {account.accrued_interest:.2f}")
    print(f"  Обчислення: {account.balance:.2f} * 0.05 = {account.accrued_interest:.2f}")

    # Обчислювальна властивість 3: account_info
    print(f"\nОбчислювальна властивість 3: account_info (read-only рідбіння)")
    info = account.account_info
    for key, value in info.items():
        print(f"  {key}: {value}")

    # Демонстрація оновлення обчислювальних властивостей
    print(f"\n--- Після операцій з рахунком ---")
    account.deposit(1000)
    print(f"\nПосле deposit(1000):")
    print(f"  Новий баланс: {account.balance:.2f}")
    print(f"  Нові відсотки: {account.accrued_interest:.2f}")
    print(f"  Нова кількість транзакцій: {account.transaction_count}")


def demonstrate_private_attribute_access():
    """Демонстрація приватних атрибутів та name mangling."""
    print_section("6. ПРИВАТНІ АТРИБУТИ (__) ТА NAME MANGLING")

    account = BankAccount(
        account_number="444555666",
        owner_name="Андрій Борисович",
        owner_email="andry@example.com",
        initial_balance=3000.00,
        pin="3333"
    )

    print(f"\nРахунок: {account}")

    # Спроба 1: Прямий доступ до __balance
    print("\nСпроба 1: Прямий доступ до приватного атрибута __balance")
    try:
        balance = account.__balance
        print(f"  account.__balance = {balance}  (помилка, не повинна робити!)")
    except AttributeError as e:
        print(f"  ATTRIBUTEERROR: {e}")
        print(f"  Це очікувано - приватний атрибут недоступний напряму")

    # Спроба 2: Доступ через name mangling
    print("\nСпроба 2: Доступ через name mangling (_BankAccount__balance)")
    try:
        balance = account._BankAccount__balance
        print(f"  account._BankAccount__balance = {balance}")
        print(f"  Це повинна робити! Name mangling дозволяє доступ до приватних атрибутів")
    except AttributeError as e:
        print(f"  ПОМИЛКА: {e}")

    # Спроба 3: Прямий доступ до __pin
    print("\nСпроба 3: Прямий доступ до приватного атрибута __pin")
    try:
        pin = account.__pin
        print(f"  account.__pin = {pin}  (помилка, не повинна робити!)")
    except AttributeError as e:
        print(f"  ATTRIBUTEERROR: {e}")

    # Спроба 4: Доступ до __pin через name mangling
    print("\nСпроба 4: Доступ до __pin через name mangling")
    try:
        pin = account._BankAccount__pin
        print(f"  account._BankAccount__pin = '{pin}'")
        print(f"  Успішно - дійсний PIN прихований, але доступний через name mangling")
    except AttributeError as e:
        print(f"  ПОМИЛКА: {e}")

    # Спроба 5: Доступ до захищеного атрибута _
    print("\nСпроба 5: Доступ до захищеного атрибута _owner_email")
    try:
        email = account._owner_email
        print(f"  account._owner_email = '{email}'")
        print(f"  Успішно - захищений атрибут доступний з одним підкресленням")
    except AttributeError as e:
        print(f"  ПОМИЛКА: {e}")

    # Спроба 6: Доступ до _transactions
    print("\nСпроба 6: Доступ до захищеної historie _transactions")
    try:
        trans_count = len(account._transactions)
        print(f"  len(account._transactions) = {trans_count}")
        print(f"  Успішно - це внутрішній атрибут, але більш доступний ніж __")
    except AttributeError as e:
        print(f"  ПОМИЛКА: {e}")


def demonstrate_operations():
    """Демонстрація операцій над рахунком."""
    print_section("7. ОПЕРАЦІЇ НА РАХУНКОМ (deposit, withdraw, transfer)")

    account1 = BankAccount(
        account_number="100001",
        owner_name="Юлія Килимник",
        owner_email="julia@example.com",
        initial_balance=1000.00,
        pin="1234"
    )

    account2 = BankAccount(
        account_number="200002",
        owner_name="Максим Роман",
        owner_email="maxim@example.com",
        initial_balance=500.00,
        pin="5678"
    )

    print(f"\nРахунок 1: {account1}")
    print(f"Рахунок 2: {account2}")

    # Deposit
    print("\n--- Поповнення рахунку 1 на 500 ---")
    new_balance = account1.deposit(500)
    print(f"Новий баланс: {new_balance:.2f}")

    # Withdraw
    print("\n--- Зняття з рахунку 1 200 ---")
    new_balance = account1.withdraw(200)
    print(f"Новий баланс: {new_balance:.2f}")

    # Transfer
    print(f"\n--- Переказ з рахунку 1 на рахунок 2 300 ---")
    account1.transfer(account2, 300)
    print(f"Баланс рахунку 1: {account1.balance:.2f}")
    print(f"Баланс рахунку 2: {account2.balance:.2f}")

    # Некоректні операції
    print("\n--- Спроба зняти більше, ніж на рахунку ---")
    try:
        account2.withdraw(1000)
    except ValueError as e:
        print(f"ПОМИЛКА: {e}")

    print(f"Баланс рахунку 2: {account2.balance:.2f} (без змін)")

    # Вивести історію
    account1.print_transactions()


def demonstrate_differences():
    """Пояснення різниці між _ та __"""
    print_section("8. РІЗНИЦЯ МІЖ _ та __ АТРИБУТАМИ")

    print("""
ЗАХИЩЕНІ АТРИБУТИ (_single underscore):
  - Конвенція: "Не точайте цього з-поза класу, це внутрішне"
  - Доступ: Легко доступні (ніякої обфускації)
  - Використання: Для внутрішніх деталей при раширенні класу
  - Name mangling: НЕ застосовується - атрибут повністю видимий
  - Приклад: _transactions, _interest_rate, _owner_email
  - Коли обирати: Коли хочемо сказати "це внутрішнє, не змінюйте прямо"

---

ПРИВАТНІ АТРИБУТИ (__double underscore):
  - Konvention: "Ці дані helt privat - не доступні без særlig grund"
  - Доступ: Скважинований через name mangling
  - Name mangling: Python перетворює __attr на _ClassName__attr
  - Використання: Для справління конфлікту імен у класах-спадкоємцях
  - Приклад: __balance, __pin
  - Коли обирати: Коли дійсно потрібна приватність і захист від наслідування

---

PYTHON НЕ ЗА СПРАВЖНЬО ЛИШАЄ ВИГЛЯДАТИ ПРИВАТНІ ЗМІННІ:
  - Можна все-таки отримати доступ через name mangling
  - Це досяжи скорупи, а не кровь буквальної приватності
  - Це залежить від конвенцій програміста
  - Мета: Запобігти *випадковим* конфліктам, не запобігти керованому доступу

---

ПРАКТИЧНІ РЕКОМЕНДАЦІЇ:
  1. Використовуйте _ для найпростіших внутрішніх деталей
  2. Використовуйте __ тільки коли дійсно потрібна обфускація
  3. Завжди обіспечуйте @property для доступу до приватних атрибутів
  4. Добре задокументуйте поведінку в docstring
    """)


def main():
    """Головна функція."""
    print("\n" + "="*80)
    print("КЛАС BankAccount З КОНТРОЛЬОВАНИМ ДОСТУПОМ")
    print("Демонстрація приватних та захищених атрибутів")
    print("="*80)

    demonstrate_valid_creation()
    demonstrate_invalid_email()
    demonstrate_invalid_balance()
    demonstrate_invalid_pin()
    demonstrate_calculated_properties()
    demonstrate_private_attribute_access()
    demonstrate_operations()
    demonstrate_differences()

    print_section("ВИСНОВКИ")

    print("""
РЕАЛІЗОВАНО:

1. ПРИВАТНІ АТРИБУТИ (__):
   - __balance: Баланс рахунку
   - __pin: PIN-код
   - Доступ тільки через @property та name mangling

2. ЗАХИЩЕНІ АТРИБУТИ (_):
   - _transactions: Історія транзакцій
   - _owner_email: Email власника
   - _interest_rate: Процентна ставка

3. @PROPERTY (Getters/Setters з валідацією):
   - balance: Числовий діапазон, неотримання від'ємних значень
   - owner_email: Формат email
   - pin: Точно 4 цифри
   - Все з інформативними повідомленнями про помилки

4. ОБЧИСЛЮВАЛЬНІ ВЛАСТИВОСТІ (read-only):
   - transaction_count: Кількість записів
   - accrued_interest: Проценти на рік
   - account_info: Повна інформація про рахунок

5. ДЕМОНСТРАЦІЯ:
   - Коректне створення
   - Спроби встановлення некоректних значень
   - Перехоплення винятків ValueError та TypeError
   - Прямий доступ до __ (приходить до AttributeError)
   - Доступ через name mangling (_BankAccount__attr)
   - Захищений доступ до _ атрибутів
   - Функціональність рахунку (deposit, withdraw, transfer)
    """)

    print("="*80)
    print("Програма завершена.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
