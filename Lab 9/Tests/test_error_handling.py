
import ast
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from file_handler import load_inventory
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
SUPPLIER = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")


class SpecificExceptTests(unittest.TestCase):

    def test_every_except_names_a_specific_exception(self) -> None:
        for path in sorted(PROJECT_FOLDER.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    with self.subTest(file=path.name, line=node.lineno):
                        self.assertIsNotNone(node.type, "a bare 'except:' catches everything")
                        assert node.type is not None
                        self.assertNotIn(ast.unparse(node.type), ("Exception", "BaseException"))


class FileErrorTests(unittest.TestCase):

    def test_missing_inventory_file_starts_an_empty_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as folder, redirect_stdout(io.StringIO()) as output:
            inventory, suppliers = load_inventory(os.path.join(folder, "missing.json"))
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(suppliers, [])
        self.assertIn("is missing", output.getvalue())

    def test_corrupted_inventory_file_starts_an_empty_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w", encoding="utf-8") as file:
                file.write("{not valid json")
            with redirect_stdout(io.StringIO()) as output:
                inventory, _ = load_inventory(path)
        self.assertEqual(inventory.get_products(), [])
        self.assertIn("is corrupted", output.getvalue())

    def test_a_save_problem_is_reported_instead_of_crashing(self) -> None:
        with patch("main.save_inventory", side_effect=PermissionError(13, "Permission denied")), \
                redirect_stdout(io.StringIO()) as output:
            saved = main.try_save(Inventory(), [])
        self.assertFalse(saved)
        self.assertIn("Could not save to inventory.json: Permission denied.", output.getvalue())

    def test_exit_lets_the_user_stay_when_saving_fails(self) -> None:
        answers = ["13", "n", "13", "y"]  # exit, refuse to lose data, exit again, accept
        with patch("main.save_inventory", side_effect=PermissionError(13, "Permission denied")), \
                patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()) as output:
            main.run_menu(Inventory(), [])
        printed = output.getvalue()
        self.assertEqual(printed.count("Could not save"), 2)
        self.assertEqual(printed.count("Program exited."), 1)


class ShippingErrorTests(unittest.TestCase):

    def test_missing_weight_is_explained_in_search(self) -> None:
        inventory = Inventory()
        inventory.add_product(ProductFactory.create("physical", "P003", "Monitor Stand",
                                                    39.50, 7, SUPPLIER))
        with patch("builtins.input", side_effect=["P003"]), redirect_stdout(io.StringIO()) as output:
            main.search_product(inventory)
        self.assertIn("Shipping Cost: unavailable", output.getvalue())


if __name__ == "__main__":
    unittest.main()
