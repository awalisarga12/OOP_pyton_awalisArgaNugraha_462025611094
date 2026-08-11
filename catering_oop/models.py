from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


class Person(ABC):
    """Abstract base class: common contract for every person."""

    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Nama minimal 2 karakter.")
        self.__name = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Nomor telepon minimal 8 angka.")
        self.__phone = value

    @abstractmethod
    def role(self) -> str:
        pass


class Customer(Person, ABC):
    def __init__(self, name: str, phone: str, address: str):
        super().__init__(name, phone)
        self.address = address.strip()

    @abstractmethod
    def calculate_bill(self, subtotal: int) -> int:
        """Polymorphic billing contract."""
        pass

    def role(self):
        return "Pelanggan"


class RegularCustomer(Customer):
    customer_type = "regular"

    def calculate_bill(self, subtotal: int) -> int:
        return subtotal


class PromoCustomer(Customer):
    customer_type = "promo"
    discount_rate = 0.10

    def calculate_bill(self, subtotal: int) -> int:
        return round(subtotal * (1 - self.discount_rate))


class Chef(Person):
    def __init__(self, name: str, phone: str, specialty: str):
        super().__init__(name, phone)
        self.specialty = specialty

    def role(self):
        return "Koki"


@dataclass(frozen=True)
class MenuItem:
    id: int | None
    name: str
    category: str
    price: int
    stock: int

    def __post_init__(self):
        if self.price < 0 or self.stock < 0:
            raise ValueError("Harga dan stok tidak boleh negatif.")


@dataclass
class OrderItem:
    menu_id: int
    menu_name: str
    price: int
    quantity: int

    @property
    def subtotal(self):
        return self.price * self.quantity


class Order:
    def __init__(self, customer: Customer, items: list[OrderItem], delivery_date: str,
                 payment_method: str, notes: str = ""):
        if not items:
            raise ValueError("Pesanan minimal memiliki satu menu.")
        self.customer = customer
        self.items = items
        self.delivery_date = delivery_date
        self.payment_method = payment_method
        self.notes = notes
        self.created_at = datetime.now()

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)

    @property
    def total(self):
        return self.customer.calculate_bill(self.subtotal)

    @property
    def discount(self):
        return self.subtotal - self.total


def create_customer(customer_type: str, name: str, phone: str, address: str) -> Customer:
    classes = {"regular": RegularCustomer, "promo": PromoCustomer}
    if customer_type not in classes:
        raise ValueError("Jenis pelanggan tidak valid.")
    return classes[customer_type](name, phone, address)

