
import ast
import inspect
import unittest

import order as order_module
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")


def order_totalling(amount: float, discount: DiscountStrategy | None = None) -> Order:
    """Build an order with one line whose subtotal is exactly `amount`."""
    product = ProductFactory.create("digital", "T001", "Test Item", amount, 10, SUPPLIER)
    order = Order("T-ORDER", discount)
    order.add_order_line(product, 1)
    return order


class HalfPrice(DiscountStrategy):
    """A brand-new strategy that exists only in this test. Order was not changed for it."""

    def apply(self, total: float) -> float:
        return total / 2


class DiscountStrategyTests(unittest.TestCase):

    def test_discount_strategy_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_no_discount_leaves_the_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount_takes_the_percentage_off(self) -> None:
        self.assertEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_applies_from_the_threshold(self) -> None:
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230)
        self.assertEqual(bulk.apply(200), 180)  # exactly the threshold counts
        self.assertEqual(bulk.apply(199.99), 199.99)

    def test_bulk_discount_never_goes_below_zero(self) -> None:
        self.assertEqual(BulkDiscount(0, 50).apply(30), 0)

    def test_student_discount_takes_5_percent_off(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(100), 95)

    def test_invalid_discount_settings_are_rejected(self) -> None:
        for bad_percentage in (0, -5, 101):
            with self.subTest(percentage=bad_percentage), self.assertRaises(ValueError):
                PercentageDiscount(bad_percentage)
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 0)


class OrderDiscountTests(unittest.TestCase):

    def test_order_uses_no_discount_by_default(self) -> None:
        order = order_totalling(250)
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_predict_first_bulk_then_percentage_on_the_same_order(self) -> None:
        order = order_totalling(250, BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_subtotal_is_calculated_before_the_discount(self) -> None:
        order = order_totalling(250, PercentageDiscount(10))
        self.assertEqual(order.calculate_subtotal(), 250)

    def test_new_strategy_works_without_changing_order(self) -> None:
        self.assertEqual(order_totalling(250, HalfPrice()).calculate_total(), 125)

    def test_two_orders_can_share_one_strategy_object(self) -> None:
        shared = PercentageDiscount(10)
        first = order_totalling(250, shared)
        second = order_totalling(100, shared)
        self.assertIs(first.get_discount(), second.get_discount())
        self.assertEqual(first.calculate_total(), 225)
        self.assertEqual(second.calculate_total(), 90)

    def test_order_contains_no_discount_type_logic(self) -> None:
        # Check the code itself (not comments or docstrings) by parsing order.py
        tree = ast.parse(inspect.getsource(order_module))
        names_used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        names_used |= {alias.name for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
                       for alias in node.names}
        for strategy_name in ("PercentageDiscount", "BulkDiscount", "StudentDiscount"):
            with self.subTest(strategy=strategy_name):
                self.assertNotIn(strategy_name, names_used)
        elif_blocks = [node for node in ast.walk(tree) if isinstance(node, ast.If)
                       and len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)]
        self.assertEqual(elif_blocks, [], "Order should not choose between discounts with if/elif")


if __name__ == "__main__":
    unittest.main()
