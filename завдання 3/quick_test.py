#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Швидка перевірка всіх програм без стиків."""

def test_list_operations():
    """Тест операцій зі списками."""
    print("\nТест 1: Операції зі списками")
    lst = [10, 20, 30, 40, 50]
    print(f"  Список: {lst}")
    print(f"  lst[0] = {lst[0]}")
    print(f"  lst[-1] = {lst[-1]}")
    print(f"  lst[1:4] = {lst[1:4]}")
    print(f"  lst[::2] = {lst[::2]}")
    print("  OK")

def test_tuple_operations():
    """Тест операцій з кортежами."""
    print("\nТест 2: Кортежі")
    record = (1, "Іван", "IT", ["AI", "ML"], 45)
    author_id, name, dept, pubs, citations = record
    print(f"  Розпакований: id={author_id}, ім'я={name}")
    print(f"  Доступ: record[1] = {record[1]}")
    print(f"  Кортеж іммутабельний: {type(record)}")
    print("  OK")

def test_dict_operations():
    """Тест операцій зі словниками."""
    print("\nТест 3: Словник частот")
    text = "hello world hello"
    freq = {}
    for word in text.lower().split():
        freq[word] = freq.get(word, 0) + 1
    print(f"  Текст: {text}")
    print(f"  Частити: {freq}")
    filtered = {k: v for k, v in freq.items() if v >= 1}
    print(f"  Фільтровано: {filtered}")
    print("  OK")

def test_set_operations():
    """Тест операцій з множинами."""
    print("\nТест 4: Множини")
    set1 = {1, 2, 3, 4, 5}
    set2 = {3, 4, 5, 6, 7}
    print(f"  set1 = {set1}")
    print(f"  set2 = {set2}")
    print(f"  Перетин: {set1 & set2}")
    print(f"  Об'єднання: {set1 | set2}")
    print(f"  Різниця: {set1 - set2}")
    print("  OK")

def test_vector():
    """Тест Vector3D."""
    print("\nТест 7: Vector3D з магічними методами")
    from vector_magic_methods import Vector3D

    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(2, 3, 4)

    print(f"  v1 = {v1}")
    print(f"  v2 = {v2}")
    print(f"  v1 + v2 = {v1 + v2}")
    print(f"  v1 * 2 = {v1 * 2}")
    print(f"  abs(v1) = {abs(v1):.2f}")
    print(f"  v1[0] = {v1[0]}")
    print(f"  len(v1) = {len(v1)}")
    print("  OK")

def main():
    """Запуск всіх тестів."""
    print("\n" + "="*50)
    print("ШВИДКА ПЕРЕВІРКА ВСІХ ПРОГРАМ")
    print("="*50)

    try:
        test_list_operations()
        test_tuple_operations()
        test_dict_operations()
        test_set_operations()
        test_vector()

        print("\n" + "="*50)
        print("ВСІ ТЕСТИ ПРОЙДЕНІ УСПІШНО")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\nОшибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
