
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema obrobky zamovlen z abstraktnym bazovym klasom (ABC) ta kompozyciyeyu.

Arhitektura:
- AbstractOrderComponent (ABC) - kontraktrequest dlya vsih komponentiv zamovlennia
- OrderItem, Discount, ShippingMethod (is-a AbstractOrderComponent) - konkretn pid klasy
- Order (has-a OrderItem[], Discount[], ShippingMethod) - kompozycya z deleguvanniam

Is-a: OrderItem, Discount, ShippingMethod USADKOVUYUTSIA vid AbstractOrderComponent
Has-a: Order MISTYT komponenty yak objekty (kompozycya), ne usadkovuye yikh

Obhruntuvannia has-a vmist is-a:
- Order ne ye OrderItem, Discount abo ShippingMethod
- Order lyshе VIROBNIKhuje i DLEHUYUЄ yim
- Kozhna pozycya, znyzka, dostavka - vidokremi entity z vlasnoyuy logikoyuy
- Order orhanizuye yih VZAYEMODIYEYUVATNNIA
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


# ========== ABSTRAKTNYY BAZOVYY KLAS (KONTRAKТ) ==========

class AbstractOrderComponent(ABC):
    """
    Abstraktnyy bazovyy klas dlya vsih komponentiv systemy zamovlen.

    Vyznachayes kontrakт (interfeys) dlia:
    - calculate() - rozrahuje vartist/znachennia komponenty
    - get_description() - ponizuye opys komponenty
    - component_type - abstraktna vlastyvist (read-only)
    - validate() - konkretnyy metod (usim dostupnyy, yenokh realizovanyy v baza)
    """

    def __init__(self, name):
        """
        Inicializaciya komponenty.

        Args:
            name: Nazva komponenty
        """
        self.name = name

    @abstractmethod
    def calculate(self):
        """
        Rozrahuyutь vartist abo znachennia komponenty.

        Returns:
            float: Rozrakhovane znachennia
        """
        pass

    @abstractmethod
    def get_description(self):
        """
        Povertaye detalnyyopys komponenty.

        Returns:
            str: Opys komponenty
        """
        pass

    @property
    @abstractmethod
    def component_type(self):
        """
        Abstraktna vlastyvist: typ komponenty.

        Returns:
            str: Tip komponenty (napr. 'item', 'discount', 'shipping')
        """
        pass

    def validate(self):
        """
        Konkretnyymetod dlia validacyy danyh komponenty.
        Dostupnyy vsim pid klasam, implementovanyy v baza.

        Returns:
            bool: True yakshcho dani pravilni
        """
        if not self.name or len(self.name) == 0:
            raise ValueError("Nazva komponenty ne mozhe buty pustomu")
        return True


# ========== KONKRETN KLASY (IS-A USADKOVUVANNIA) ==========

class OrderItem(AbstractOrderComponent):
    """
    Konkretnyy pid klas: Pozycya v zamovlenni.

    IS-A: OrderItem ye AbstractOrderComponent
    """

    def __init__(self, name, price, quantity):
        """
        Inicializaciya pozycyy.

        Args:
            name: Nazva tovary
            price: Cina za odinyvycy
            quantity: Kilkist odinyvyc
        """
        super().__init__(name)
        self.price = price
        self.quantity = quantity

    def calculate(self):
        """
        Rozrahuyutь zagalnu vartist pozycyy.

        Returns:
            float: price * quantity
        """
        self.validate()
        if self.price < 0:
            raise ValueError("Cina ne mozhe buty vid'yemnoyu")
        if self.quantity <= 0:
            raise ValueError("Kilkist povynna buty dodatnoyu")
        return self.price * self.quantity

    def get_description(self):
        """Ponizuye opys pozycyy."""
        return "{} x{} po {:.2f} = {:.2f}".format(
            self.name, self.quantity, self.price, self.calculate())

    @property
    def component_type(self):
        """Tip komponenty: 'item'."""
        return "item"


class Discount(AbstractOrderComponent):
    """
    Konkretnyy pid klas: Znyzka.

    IS-A: Discount ye AbstractOrderComponent
    """

    def __init__(self, name, discount_type, value):
        """
        Inicializaciya znyzky.

        Args:
            name: Nazva znyzky
            discount_type: 'percent' abo 'fixed'
            value: Znachennia znyzky (0-100 dlia procentiv abo suma dlia fixed)
        """
        super().__init__(name)
        self.discount_type = discount_type
        self.value = value

    def calculate(self):
        """
        Rozrahuyutь sumu znyzky.

        Povertaye:
            float: Suma znyzky (u valyuty)

        Zvertaye 0, oskilky sama znyzka ne ma vartosti - 
        vyukoristuetsya dlya rozrahunku v Order.apply_discounts().
        """
        self.validate()
        if self.discount_type not in ['percent', 'fixed']:
            raise ValueError("Nedopustymyy typ znyzky: {}".format(self.discount_type))
        if self.value < 0:
            raise ValueError("Znyshennia ne mozhe buty vid'yemnym")
        return self.value

    def get_description(self):
        """Ponizuye opys znyzky."""
        if self.discount_type == 'percent':
            return "{}: {}%".format(self.name, self.value)
        else:
            return "{}: -{:.2f}".format(self.name, self.value)

    @property
    def component_type(self):
        """Tip komponenty: 'discount'."""
        return "discount"

    def apply_to_amount(self, amount):
        """
        Zazhodovuye znyzku do sumy.

        Args:
            amount: Vyhidna suma

        Returns:
            float: Suma pislia prymenennia znyzky
        """
        self.validate()
        if self.discount_type == 'percent':
            return amount * (1 - self.value / 100)
        else:
            return max(0, amount - self.value)


class ShippingMethod(AbstractOrderComponent):
    """
    Konkretnyy pid klas: Metod dostavky.

    IS-A: ShippingMethod ye AbstractOrderComponent
    """

    def __init__(self, name, base_price, acceleration_factor=1.0):
        """
        Inicializaciya metody dostavky.

        Args:
            name: Nazva metody (napr. 'Standard', 'Express')
            base_price: Bazova cina dostavky
            acceleration_factor: Koeficiyent (1.0 - zvychayne, 2.0 - priskorysh)
        """
        super().__init__(name)
        self.base_price = base_price
        self.acceleration_factor = acceleration_factor

    def calculate(self):
        """
        Rozrahuyutь vartist dostavky.

        Returns:
            float: base_price * acceleration_factor
        """
        self.validate()
        if self.base_price < 0:
            raise ValueError("Bazova cina dostavky ne mozhe buty vid'yemnoyu")
        if self.acceleration_factor <= 0:
            raise ValueError("Koeficiyentускоренnia povynen buty dodatnym")
        return self.base_price * self.acceleration_factor

    def get_description(self):
        """Ponizuye opys dostavky."""
        base = self.calculate()
        return "{}: {:.2f} (koef. {})".format(self.name, base, self.acceleration_factor)

    @property
    def component_type(self):
        """Tip komponenty: 'shipping'."""
        return "shipping"

    def get_delivery_days(self):
        """Povertaye pryblyznу kilkist dniv dostavky."""
        if self.acceleration_factor >= 2.0:
            return 1
        elif self.acceleration_factor >= 1.5:
            return 2
        else:
            return 5


# ========== KOMPOZYCYA: ORDER Z DELEGUVANNYAM ==========

class Order:
    """
    Klas Order, yaky MISTYT (has-a) komponenty.

    HAS-A:
    - Order.items: List[OrderItem] - pozycyy
    - Order.discounts: List[Discount] - znyzky
    - Order.shipping: ShippingMethod - dostavka

    Order NE ye AbstractOrderComponent - vin orhanizuye komponenty 
    i DLEHUYUЄ yim (vyukoristovuye yihni metody).

    Vyukoristovuye pattern Composite: Order mozhe obrablyaty nabir komponentiv.
    """

    def __init__(self, order_number, customer_email):
        """
        Inicializaciya zamovlennia.

        Args:
            order_number: Nomer zamovlennia
            customer_email: Email kliyenta
        """
        self.order_number = order_number
        self.customer_email = customer_email
        self.created_at = datetime.now()

        # Kompozycya: Order MISTYT komponenty
        self.items: List[OrderItem] = []
        self.discounts: List[Discount] = []
        self.shipping: ShippingMethod = None

    def add_item(self, item: OrderItem):
        """
        Dodaye pozycyu do zamovlennia.

        Delehuvannia: Order vyukoristovuye metod calculate() pozycyy.

        Args:
            item: Ob'ekt OrderItem
        """
        if not isinstance(item, OrderItem):
            raise TypeError("Pozycya povynna buty OrderItem, otrymano {}".format(type(item).__name__))
        item.validate()  # Delehuvannia validacyy
        self.items.append(item)

    def add_discount(self, discount: Discount):
        """
        Dodaye znyzku do zamovlennia.

        Delehuvannia: Order vyukoristovuye metod calculate() znyzky.

        Args:
            discount: Ob'ekt Discount
        """
        if not isinstance(discount, Discount):
            raise TypeError("Znyzka povynna buty Discount, otrymano {}".format(type(discount).__name__))
        discount.validate()  # Delehuvannia validacyy
        self.discounts.append(discount)

    def set_shipping(self, shipping: ShippingMethod):
        """
        Vstanovlyuye metod dostavky.

        Delehuvannia: Order vyukoristovuye metod calculate() dostavky.

        Args:
            shipping: Ob'ekt ShippingMethod
        """
        if not isinstance(shipping, ShippingMethod):
            raise TypeError("Dostavka povynna buty ShippingMethod, otrymano {}".format(type(shipping).__name__))
        shipping.validate()  # Delehuvannia validacyy
        self.shipping = shipping

    def calculate_subtotal(self):
        """
        Rozrahuyutь pidytohy (bez znyzok i dostavky).

        Delehuvannia: vydalyuye calculate() metodiv vsih OrderItem.

        Returns:
            float: Suma vsih pozyciy
        """
        if not self.items:
            return 0.0
        return sum(item.calculate() for item in self.items)

    def calculate_total(self):
        """
        Rozrahuyutь zagalnu vartist zamovlennia.

        Delehuvannia:
        - Vedalyuye calculate() metodiv vsuh OrderItem
        - Vedalyuye apply_to_amount() metodiv vsuh Discount
        - Vedalyuye calculate() metody ShippingMethod

        Returns:
            float: Zagalna vartist
        """
        total = self.calculate_subtotal()

        # Delehuvannia: zastosovuyemo znyzky
        for discount in self.discounts:
            total = discount.apply_to_amount(total)

        # Delehuvannia: dodayemo dostavku
        if self.shipping:
            total += self.shipping.calculate()

        return max(0, total)

    def get_order_summary(self):
        """
        Povertaye detalnyyopys zamovlennia.

        Returns:
            str: Formatovanyy opys
        """
        summary = "=" * 70 + "\n"
        summary += "Zamovlennia {} | Kliyent: {}\n".format(self.order_number, self.customer_email)
        summary += "="*70 + "\n"

        summary += "\nPozycyy:\n"
        if self.items:
            for item in self.items:
                summary += "  - {}\n".format(item.get_description())
        else:
            summary += "  (brak pozyciy)\n"

        summary += "\nZnyzky:\n"
        if self.discounts:
            for discount in self.discounts:
                summary += "  - {}\n".format(discount.get_description())
        else:
            summary += "  (bez znyzok)\n"

        summary += "\nDostavka:\n"
        if self.shipping:
            summary += "  - {} ({} dniv)\n".format(
                self.shipping.get_description(),
                self.shipping.get_delivery_days()
            )
        else:
            summary += "  (ne vybrany)\n"

        summary += "\n" + "-"*70 + "\n"
        summary += "Pidrakhunok: {:.2f}\n".format(self.calculate_subtotal())
        summary += "Zagalom: {:.2f}\n".format(self.calculate_total())
        summary += "="*70

        return summary


# ========== DEMONSTRUVANNIA ==========

def demonstrate_abstract_instantiation():
    """Demonstruvannia sproby stvorennia ekzempliary abstraktnoho klasu."""
    print("\n" + "="*70)
    print("1. SPRO​BA STVOREN​NIA EKZEMPLIARY ABSTRAKTNOHO KLASU")
    print("="*70)

    try:
        abstract_component = AbstractOrderComponent("Test")
        print("[ERR] Neochikuvanyy uspikh: {}".format(abstract_component))
    except TypeError as e:
        print("[OK] TypeError perekhopleno:")
        print("     {}".format(e))


def demonstrate_concrete_subclasses():
    """Demonstruvannia stvoren​nia konkretnykh pohklass."""
    print("\n" + "="*70)
    print("2. STVORENNIA KONKRETNYKH POHKLASSIV")
    print("="*70)

    # OrderItem
    item1 = OrderItem("Laptop", 999.99, 1)
    print("[OK] OrderItem stvoveno: {}".format(item1.get_description()))
    print("     Typ: {}, Vartist: {:.2f}".format(item1.component_type, item1.calculate()))

    # Discount
    discount1 = Discount("Black Friday", "percent", 15)
    print("\n[OK] Discount stvoveno: {}".format(discount1.get_description()))
    print("     Typ: {}".format(discount1.component_type))

    # ShippingMethod
    shipping1 = ShippingMethod("Express", 15.00, 2.0)
    print("\n[OK] ShippingMethod stvoveno: {}".format(shipping1.get_description()))
    print("     Typ: {}, Dni dostavky: {}".format(shipping1.component_type, shipping1.get_delivery_days()))

    return item1, discount1, shipping1


def demonstrate_polymorphism():
    """Demonstruvannia polimorfizmu: vyukoristannia abstraktnoho interfeysu."""
    print("\n" + "="*70)
    print("3. POLIMORFIZM: VYUKORISTANNIA ABSTRAKTNOHO INTERFEYSU")
    print("="*70)

    components = [
        OrderItem("Mouse", 29.99, 2),
        Discount("Summer Sale", "percent", 10),
        ShippingMethod("Standard", 5.00, 1.0)
    ]

    print("Vyuklyk abstraktnykh metodiv proza polimorfizm:")
    for comp in components:
        print("\n  Komponent: {}".format(comp.name))
        print("    - component_type: '{}'".format(comp.component_type))
        print("    - get_description(): '{}'".format(comp.get_description()))
        print("    - calculate(): {:.2f}".format(comp.calculate()))
        # validate() - konkretnyy metod, dostupnyy vsim
        comp.validate()
        print("    - validate(): OK")


def demonstrate_composition_and_delegation():
    """Demonstruvannia kompozycyy i deleguvannia vidpovidalno​sti."""
    print("\n" + "="*70)
    print("4. KOMPOZYCYA I DELEGUVANNIA")
    print("="*70)

    order = Order("ORD-2024-001", "customer@example.com")

    # Odavannia pozyciy
    print("[OK] Stvorennia Order z HAS-A komponentamy:")
    item1 = OrderItem("Gaming PC", 1500.00, 1)
    item2 = OrderItem("Monitor", 299.99, 2)
    order.add_item(item1)
    order.add_item(item2)
    print("     - dod. OrderItem 1: {}".format(item1.get_description()))
    print("     - dod. OrderItem 2: {}".format(item2.get_description()))

    # Odavannia znyzok
    discount1 = Discount("Loyality", "percent", 5)
    discount2 = Discount("Coupon", "fixed", 50)
    order.add_discount(discount1)
    order.add_discount(discount2)
    print("     - dod. Discount 1: {}".format(discount1.get_description()))
    print("     - dod. Discount 2: {}".format(discount2.get_description()))

    # Vstanovlennia dostavky
    shipping = ShippingMethod("Overnight", 30.00, 3.0)
    order.set_shipping(shipping)
    print("     - vstanovleno ShippingMethod: {}".format(shipping.get_description()))

    # Deleguvannia: Order vyukoristovuye metody komponentiv
    print("\n[OK] Deleguvannia rozrahubuv komponentam:")
    print("     - item1.calculate() -> {:.2f}".format(item1.calculate()))
    print("     - item2.calculate() -> {:.2f}".format(item2.calculate()))
    print("     - discount1.apply_to_amount(3099.98) -> {:.2f}".format(
        discount1.apply_to_amount(3099.98)))
    print("     - discount2.apply_to_amount(2944.98) -> {:.2f}".format(
        discount2.apply_to_amount(2944.98)))
    print("     - shipping.calculate() -> {:.2f}".format(shipping.calculate()))

    print("\n[OK] Order.calculate_total() (deleguvannia vsim):")
    print("     Zagalna vartist: {:.2f}".format(order.calculate_total()))

    print("\n" + order.get_order_summary())

    return order


def demonstrate_validation_errors():
    """Demonstruvannia validacyy komponentiv."""
    print("\n" + "="*70)
    print("5. VALIDACYA I OBROBKA POMYLOK")
    print("="*70)

    # Test 1: Nevalidne znachennia
    print("Test 1: Negativna cina")
    try:
        bad_item = OrderItem("Bad Item", -100, 1)
        bad_item.calculate()
    except ValueError as e:
        print("[OK] ValueError perekhopleno: {}".format(e))

    # Test 2: Neverifiable discount type
    print("\nTest 2: Nepravylnyy typ znyzky")
    try:
        bad_discount = Discount("Bad", "invalid_type", 10)
        bad_discount.calculate()
    except ValueError as e:
        print("[OK] ValueError perekhopleno: {}".format(e))

    # Test 3: Zbirka bez nazvy
    print("\nTest 3: Pusta nazva komponenty")
    try:
        empty_name = OrderItem("", 100, 1)
        empty_name.validate()
    except ValueError as e:
        print("[OK] ValueError perekhopleno: {}".format(e))


def demonstrate_architecture_explanation():
    """Poyasnennya arkhitektury: IS-A i HAS-A."""
    print("\n" + "="*70)
    print("6. ARKHITEKTURNA SKHEMA: IS-A TA HAS-A")
    print("="*70)

    print("""
IZHARKHIYA KLASIS:

    AbstractOrderComponent (ABC)
        |
        +--- OrderItem (IS-A)
        |    - ye komponentom zamovlennia
        |    - realizuye abstraktni metody
        |
        +--- Discount (IS-A)
        |    - ye komponentom zamovlennia
        |    - realizuye abstraktni metody
        |
        +--- ShippingMethod (IS-A)
             - ye komponentom zamovlennia
             - realizuye abstraktni metody


KOMPOZYCYA (HAS-A):

    Order (MISTYT komponenty yak atrybuty)
        |
        +--- items: List[OrderItem] (HAS-A)
        |    - Order ne ye OrderItem
        |    - Order MISTYT OrderItems i DLEHUYUЄ rosrahubuv yim
        |
        +--- discounts: List[Discount] (HAS-A)
        |    - Order ne ye Discount
        |    - Order orhanizuye znyzky i DLEHUYUЄ yim
        |
        +--- shipping: ShippingMethod (HAS-A)
             - Order ne ye ShippingMethod
             - Order vyukoristovuye dostavku i DLEHUYUЄ rozrahunkam


OBHRUNTUVANNIA:

1. CHOMU IS-A (naslidu​vannia)?
   - OrderItem, Discount, ShippingMethod - rizni typy komponentiv
   - Usi vyukonuyut spilnyy kontrakт (AbstractOrderComponent)
   - Vyukoristuvannia polimorfizmu: mozhlivo obroblyyaty yih proza spilnyy interfeys
   - Kozhnyy ma vlasnu realizacyu abstraktnykh metodiv

2. CHOMU HAS-A (kompozycya)?
   - Order NISHCHO ne ye OrderItem, Discount abo ShippingMethod  
   - Order ORHANIZUYE yikh, ne POSHYRYUYE
   - Zabezpechuye Gybku strukturu:
     * Order mozhe maty BILY-YAKU kilkist items
     * Order mozhe maty BILY-YAKU kilkist discounts
     * Order mozhe zminyyuty dostavku bez perevyznachennia klasu
   - Zabezpechuye Slabu zale​zhysti (Loose Coupling):
     * Zmina v OrderItem ne vplyn na Order
     * Mozhlivo stvoryty novi typy komponentiv bez zminy Order

3. DELEHUVANNIA:
   - Order NE rozrahovuye vartist sam
   - Order DLEHUYUЄ metodam komponentiv (calculate(), apply_to_amount())
   - Order ORHANIZUYE rezultaty, ale ne vykonuye logiku
""")


def main():
    """Osnovna demonstruvalna funkciya."""
    print("="*70)
    print("SISTEMA ZAMOVLEN Z ABSTRAKTNYM KLASOM TA KOMPOZYCYEYU")
    print("="*70)

    demonstrate_abstract_instantiation()
    demonstrate_concrete_subclasses()
    demonstrate_polymorphism()
    demonstrate_composition_and_delegation()
    demonstrate_validation_errors()
    demonstrate_architecture_explanation()

    print("\n" + "="*70)
    print("DEMONSTRUVANNIA ZAVERSHENA")
    print("="*70)


if __name__ == "__main__":
    main()
