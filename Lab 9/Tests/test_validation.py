
import unittest

from order import Order
from order_line import OrderLine
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")


def make_product(product_type: str = "physical", price: float = 10.0, stock: int = 5) -> Product:
    return ProductFactory.create(product_type, "X001", "Test Item", price, stock, SUPPLIER)


class ProductValidationTests(unittest.TestCase):

    def test_price_must_be_greater_than_zero(self) -> None:
        for product_type in ("physical", "digital"):
            for price in (0, -12.5):
                with self.subTest(product_type=product_type, price=price):
                    with self.assertRaises(ValueError) as context:
                        make_product(product_type, price=price)
                    self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_stock_quantity_cannot_be_negative(self) -> None:
        for product_type in ("physical", "digital"):
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError) as context:
                    make_product(product_type, stock=-1)
                self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_every_subclass_keeps_the_stock_rule(self) -> None:
        """Predict first (Section 4): DigitalProduct may not skip Product's stock rule (LSP)."""
        for product_type in ("physical", "digital"):
            product = make_product(product_type)
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError):
                    product.update_stock(-3)
                product.update_stock(0)
                self.assertEqual(product.get_stock(), 0)

    def test_valid_values_are_accepted(self) -> None:
        product = make_product(price=0.01, stock=0)
        self.assertEqual(product.get_price(), 0.01)
        self.assertEqual(product.get_stock(), 0)

    def test_weight_and_download_size_must_be_positive_when_given(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "X002", "Item", 5.0, 1, SUPPLIER, weight=0)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "X003", "App", 5.0, 1, SUPPLIER, download_size=-1)

    def test_supplier_email_must_contain_an_at_sign(self) -> None:
        with self.assertRaises(ValueError):
            Supplier("S009", "Bad Email Ltd", "no-at-sign")


class OrderLineValidationTests(unittest.TestCase):

    def test_quantity_must_be_greater_than_zero(self) -> None:
        product = make_product()
        for quantity in (0, -2):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError) as context:
                    OrderLine(product, quantity)
                self.assertEqual(str(context.exception), "Quantity must be greater than zero.")

    def test_order_does_not_keep_an_invalid_line(self) -> None:
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(make_product(), 0)
        self.assertEqual(order.get_order_lines(), [])

    def test_quantity_must_be_a_whole_number(self) -> None:
        with self.assertRaises(TypeError):
            OrderLine(make_product(), 2.5)


if __name__ == "__main__":
    unittest.main()
