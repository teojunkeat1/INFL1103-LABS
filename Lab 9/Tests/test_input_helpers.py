
import io
import unittest
from collections.abc import Callable
from contextlib import redirect_stdout
from unittest.mock import patch

from input_helpers import (get_positive_float, read_non_empty, read_quantity, read_stock,
                           read_yes_no)


def run_with_answers(helper: Callable[[str], object], answers: list[str]) -> tuple[object, list[str]]:
    """Call the helper, 'typing' each answer in turn. Returns (result, lines printed)."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=answers), redirect_stdout(output):
        result = helper("Prompt: ")
    return result, output.getvalue().splitlines()


class InputHelperTests(unittest.TestCase):

    def test_predict_first_abc_then_minus_5_then_12_50(self) -> None:
        result, printed = run_with_answers(get_positive_float, ["abc", "-5", "12.50"])
        self.assertEqual(result, 12.5)
        self.assertEqual(printed, ["Please enter a valid number, e.g. 12.50",
                                   "Please enter a number greater than zero."])

    def test_zero_is_not_a_positive_number(self) -> None:
        result, printed = run_with_answers(get_positive_float, ["0", "3"])
        self.assertEqual(result, 3.0)
        self.assertEqual(printed, ["Please enter a number greater than zero."])

    def test_stock_rejects_text_and_negative_numbers(self) -> None:
        result, printed = run_with_answers(read_stock, ["ten", "-1", "5"])
        self.assertEqual(result, 5)
        self.assertEqual(printed, ["Please enter a whole number.", "Stock cannot be negative."])

    def test_quantity_rejects_zero_and_decimals(self) -> None:
        result, printed = run_with_answers(read_quantity, ["0", "1.5", "2"])
        self.assertEqual(result, 2)
        self.assertEqual(printed, ["Quantity must be greater than zero.",
                                   "Please enter a whole number."])

    def test_empty_input_is_asked_again(self) -> None:
        result, printed = run_with_answers(read_non_empty, ["", "   ", "Desk Lamp"])
        self.assertEqual(result, "Desk Lamp")
        self.assertEqual(printed, ["Input cannot be empty.", "Input cannot be empty."])

    def test_yes_no_accepts_only_y_or_n(self) -> None:
        result, printed = run_with_answers(read_yes_no, ["maybe", "Y"])
        self.assertTrue(result)
        self.assertEqual(printed, ["Please enter y or n."])


if __name__ == "__main__":
    unittest.main()
