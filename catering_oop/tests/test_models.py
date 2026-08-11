import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from models import Order, OrderItem, PromoCustomer, RegularCustomer


class OOPModelTests(unittest.TestCase):
    def test_polymorphic_bill(self):
        regular = RegularCustomer("Budi", "08123456789", "Ponorogo")
        promo = PromoCustomer("Aisyah", "08129876543", "Madiun")
        self.assertEqual(regular.calculate_bill(100_000), 100_000)
        self.assertEqual(promo.calculate_bill(100_000), 90_000)

    def test_order_total(self):
        customer = PromoCustomer("Aisyah", "08129876543", "Madiun")
        order = Order(customer, [OrderItem(1, "Nasi", 25_000, 4)], "2026-08-10", "QRIS")
        self.assertEqual(order.subtotal, 100_000)
        self.assertEqual(order.discount, 10_000)
        self.assertEqual(order.total, 90_000)

    def test_encapsulation_validation(self):
        with self.assertRaises(ValueError):
            RegularCustomer("A", "123", "-")


if __name__ == "__main__":
    unittest.main()

