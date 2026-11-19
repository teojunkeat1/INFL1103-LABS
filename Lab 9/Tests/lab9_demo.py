
import os
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from unittest.mock import patch

from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from file_handler import load_products
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier

PROJECT_FOLDER = Path(__file__).resolve().parent
os.chdir(PROJECT_FOLDER)  # so products.csv is found wherever the demo is started from


def heading(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
chair = ProductFactory.create("physical", "P010", "Office Chair", 150.00, 5, supplier, weight=12)
lamp = ProductFactory.create("physical", "P011", "Desk Lamp", 25.00, 20, supplier, weight=1.2)

# ----------------------------------------------------------------------
heading("Predict first (2.3): an order whose lines add up to 250")
order = Order("O100", BulkDiscount(200, 20))
order.add_order_line(chair, 1)  # 150.00
order.add_order_line(lamp, 4)   # 100.00
order.display_order()
print(f"calculate_total() with BulkDiscount(200, 20): {order.calculate_total():.2f}")
order.set_discount(PercentageDiscount(10))
print(f"After set_discount(PercentageDiscount(10)):   {order.calculate_total():.2f}")

# ----------------------------------------------------------------------
heading("Section 2.4: a fourth strategy, with no change to Order")
order.set_discount(StudentDiscount())
print(f"Same order with StudentDiscount(): {order.calculate_total():.2f}")
shared_discount = PercentageDiscount(10)
order_a = Order("O101", shared_discount)
order_b = Order("O102", shared_discount)
print(f"Two orders share one PercentageDiscount object: "
      f"{order_a.get_discount() is order_b.get_discount()}")

# ----------------------------------------------------------------------
heading('Predict first (3.2): ProductFactory.create("service", ...)')
try:
    ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)
except ValueError as error:
    raising_line = traceback.extract_tb(error.__traceback__)[-1]
    print(f"Caught ValueError: {error}")
    print(f"Raised by line {raising_line.lineno} of {Path(raising_line.filename).name}:")
    print(f"    {raising_line.line}")

print("\nIf nothing catches it (run as a separate program):")
uncaught = (
    "from product_factory import ProductFactory\n"
    "from supplier import Supplier\n"
    "supplier = Supplier('S001', 'TechSource Pte Ltd', 'sales@techsource.example')\n"
    "ProductFactory.create('service', 'S001', 'Installation', 30.00, 5, supplier)\n"
    "print('This line never runs')\n"
)
result = subprocess.run([sys.executable, "-c", uncaught], capture_output=True, text=True)
for line in result.stderr.strip().splitlines()[-3:]:
    print(f"    {line}")
print(f"Exit code: {result.returncode} (the program stopped)")
print(f"'This line never runs' printed? {'yes' if 'never runs' in result.stdout else 'no'}")

# ----------------------------------------------------------------------
heading("Predict first (Section 4): can DigitalProduct skip the stock rule?")
photo_editor = ProductFactory.create("digital", "D010", "Photo Editor", 49.90, 100, supplier)
for product in (lamp, photo_editor):
    try:
        product.update_stock(-5)
    except ValueError as error:
        print(f"{type(product).__name__}.update_stock(-5) -> ValueError: {error}")

# ----------------------------------------------------------------------
heading("Predict first (5.1): the user types abc, then -5, then 12.50")
answers = iter(["abc", "-5", "12.50"])


def typed_input(prompt: str) -> str:
    """Pretend to be the user: show the prompt and the answer typed."""
    answer = next(answers)
    print(f"{prompt}{answer}")
    return answer


with patch("builtins.input", typed_input):
    price = get_positive_float("Price: ")
print(f"Returned value: {price!r}")

# ----------------------------------------------------------------------
heading("Predict first (5.2): loading products.csv into an empty inventory")
load_products("products.csv", Inventory(), supplier)
print("(else and finally ran; except did not)")

heading("Predict first (5.2): the same load after products.csv has been renamed")
with tempfile.TemporaryDirectory() as empty_folder:
    os.chdir(empty_folder)  # a folder with no products.csv in it - same as renaming the file
    try:
        load_products("products.csv", Inventory(), supplier)
    finally:
        os.chdir(PROJECT_FOLDER)
print("(except and finally ran; else did not)")
