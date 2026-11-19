
import inspect
import unittest

import file_handler
import main
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")


class ProductFactoryTests(unittest.TestCase):

    def test_creates_a_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10,
                                        SUPPLIER, weight=1.2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        assert isinstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 1.2)

    def test_creates_a_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100,
                                        SUPPLIER, download_size=850)
        self.assertIsInstance(product, DigitalProduct)
        assert isinstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 850)

    def test_product_type_ignores_case_and_spaces(self) -> None:
        product = ProductFactory.create(" Physical ", "P002", "Office Chair", 89.00, 3, SUPPLIER)
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_a_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, SUPPLIER)
        self.assertEqual(str(context.exception), "Unknown product type: service")

    def test_weight_can_be_left_out(self) -> None:
        product = ProductFactory.create("physical", "P003", "Monitor Stand", 39.50, 7, SUPPLIER)
        assert isinstance(product, PhysicalProduct)
        self.assertIsNone(product.get_weight())
        with self.assertRaises(ValueError):
            product.calculate_shipping_cost()

    def test_factory_products_still_pass_through_validation(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P004", "Free Lamp", 0, 1, SUPPLIER)

    def test_program_creates_products_only_through_the_factory(self) -> None:
        for module in (main, file_handler):
            source = inspect.getsource(module)
            with self.subTest(module=module.__name__):
                self.assertNotIn("PhysicalProduct(", source)
                self.assertNotIn("DigitalProduct(", source)
                self.assertIn("ProductFactory.create(", source)


if __name__ == "__main__":
    unittest.main()
