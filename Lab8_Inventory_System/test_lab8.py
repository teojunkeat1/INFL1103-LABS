"""Lab 8 checks: association, aggregation, composition, type hints, LSP and polymorphism.

Run with:  python test_lab8.py

The "Predict first" sections print what actually happens, so you can compare
the output with the prediction you wrote down BEFORE running this file.
"""
import gc
import inspect
import io
import os
import re
import tempfile
import weakref
from collections.abc import Callable
from contextlib import redirect_stdout

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order_line import OrderLine
from order import Order
from file_handler import load_inventory, save_inventory

results: list[bool] = []


# ---------- Helpers ----------

def check(description: str, passed: bool) -> None:
    """Record and print the result of one check."""
    results.append(passed)
    print(f"  [{'PASS' if passed else 'FAIL'}] {description}")


def heading(title: str) -> None:
    print(f"\n{title}")
    print("=" * len(title))


def captured_output(action: Callable[[], None]) -> str:
    """Run action() and return everything it printed, so the output can be checked."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        action()
    return buffer.getvalue()


def missing_type_hints(cls: type) -> list[str]:
    """List any method parameter or return value in cls that has no type hint."""
    missing: list[str] = []
    for name, member in vars(cls).items():
        if not inspect.isfunction(member):
            continue
        signature = inspect.signature(member)
        for parameter in list(signature.parameters.values())[1:]:  # skip self
            if parameter.annotation is inspect.Parameter.empty:
                missing.append(f"{name}(): parameter '{parameter.name}'")
        if signature.return_annotation is inspect.Signature.empty:
            missing.append(f"{name}(): return type")
    return missing


def show_product_details(product: Product) -> None:
    """Section 6.2: works with ANY Product, using only behaviour every Product promises."""
    product.display_information()
    print(product.get_fulfilment_info())


def show_all(inventory: Inventory) -> None:
    """Section 7.2: one loop over the Product collection - no isinstance(), no separate loops."""
    for product in inventory.get_products():
        product.display_information()
        print(f"    Fulfilment: {product.get_fulfilment_info()}")


class NoStockDigitalProduct(DigitalProduct):
    """Section 6.3 Diagnose: the teammate's proposal. It breaks a promise Product makes."""

    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


def restock_all(products: list[Product], quantity: int) -> None:
    """Code written for Product - it should work for every kind of Product."""
    for product in products:
        product.update_stock(quantity)


# ======================================================================
heading("2. Association: Supplier and Product")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
antivirus = DigitalProduct("D001", "Antivirus Software", 49.90, 100, supplier, 350)

print("Supplier information, reached through each product:")
laptop.get_supplier().display_information()
antivirus.get_supplier().display_information()
check("each Product stores a reference to its Supplier", laptop.get_supplier() is supplier)
check("both products share the SAME Supplier object (no copies)",
      laptop.get_supplier() is antivirus.get_supplier())
try:
    PhysicalProduct("P999", "Test", 1.00, 1, "TechSource Pte Ltd", 1.0)  # deliberately wrong type
    check("Product rejects a supplier name instead of a Supplier object", False)
except TypeError:
    check("Product rejects a supplier name instead of a Supplier object", True)

softhub = Supplier("S002", "SoftHub Digital", "licensing@softhub.example")
check("a Supplier can exist with no products", softhub.get_name() == "SoftHub Digital")
temporary = DigitalProduct("D900", "Temporary Item", 1.00, 1, softhub, 1)
del temporary
check("deleting a Product does not affect its Supplier", softhub.get_name() == "SoftHub Digital")

print("\nPredict first (2.2): after `del supplier`, can each product still show its supplier?")
del supplier
laptop.get_supplier().display_information()
antivirus.get_supplier().display_information()
check("both products still reach the supplier after `del supplier`",
      laptop.get_supplier().get_name() == "TechSource Pte Ltd"
      and antivirus.get_supplier().get_name() == "TechSource Pte Ltd")
print("  Why: `del` removes the variable name only. The Supplier object stays alive")
print("  because the products still hold references to it.")
techsource = laptop.get_supplier()

# ======================================================================
heading("3. Aggregation: Inventory and Product")
guitar = PhysicalProduct("P002", "Acoustic Guitar", 350.00, 8, techsource, 4.2)  # before any inventory
inventory_a = Inventory()
inventory_b = Inventory()
check("the product exists before it is added to an inventory", guitar.get_name() == "Acoustic Guitar")
check("add the product to Inventory A", inventory_a.add_product(guitar))

print("\nPredict first (3.2): does the product still work after it is removed from Inventory A?")
removed = inventory_a.remove_product("P002")
print("Removed from Inventory A, then used directly:")
guitar.display_information()
guitar.update_stock(10)
check("remove_product() hands back the same Product object", removed is guitar)
check("Inventory A no longer holds it", inventory_a.find_product("P002") is None)
check("the removed product still works (stock updated to 10)", guitar.get_stock() == 10)
check("the same Product object can be added to Inventory B", inventory_b.add_product(guitar))
check("Inventory B now holds that same object", inventory_b.find_product("P002") is guitar)
del inventory_b
gc.collect()
check("removing Inventory B (the whole) does not destroy the product (the part)",
      guitar.get_name() == "Acoustic Guitar")
print("  Why: an Inventory only stores references. Removing a product, or the whole")
print("  inventory, drops a reference - the Product lives on while anything still uses it.")

# ======================================================================
heading("4. Composition: Order and OrderLine")
order_1 = Order("O001")
order_1.add_order_line(laptop, 2)  # the Order creates each OrderLine itself
order_1.add_order_line(antivirus, 3)
order_1.display_order()
lines = order_1.get_order_lines()
check("the Order created its own OrderLine objects",
      len(lines) == 2 and all(isinstance(line, OrderLine) for line in lines))
check("an OrderLine refers to the existing Product (no copy is made)", lines[0].get_product() is laptop)
check("the total comes from the line subtotals (2 x 1200.00 + 3 x 49.90 = 2549.70)",
      order_1.calculate_total() == 2549.70)
lines.clear()  # only clears the copy we were given
check("get_order_lines() returns a copy, so only the Order can change its lines",
      len(order_1.get_order_lines()) == 2)

print("\nPredict first (4.3): the same Product added to two different Orders")
order_2 = Order("O002")
order_2.add_order_line(laptop, 1)
line_in_o001 = order_1.get_order_lines()[0]
line_in_o002 = order_2.get_order_lines()[0]
print(f"  OrderLine in O001: id {id(line_in_o001)}")
print(f"  OrderLine in O002: id {id(line_in_o002)}")
print(f"  Product in each line: id {id(line_in_o001.get_product())} and id {id(line_in_o002.get_product())}")
check("2 OrderLine objects - each Order created its own", line_in_o001 is not line_in_o002)
check("1 Product object - both lines refer to the same laptop",
      line_in_o001.get_product() is line_in_o002.get_product())

print("\nRemoving a line through the Order:")
check("remove_order_line('D001') removes the antivirus line", order_1.remove_order_line("D001"))
order_1.display_order()
check("O001 now has 1 line and a total of 2400.00",
      len(order_1.get_order_lines()) == 1 and order_1.calculate_total() == 2400.00)
check("the Product from the removed line still exists", antivirus.get_name() == "Antivirus Software")

print("\nWhat happens to the parts when the whole goes away?")
order_3 = Order("O003")
order_3.add_order_line(guitar, 1)
line_watcher = weakref.ref(order_3.get_order_lines()[0])  # watches the line without keeping it alive
del order_3
gc.collect()
check("when Order O003 is removed, its OrderLine is gone too", line_watcher() is None)
check("...but the Product it referred to still exists", guitar.get_name() == "Acoustic Guitar")

# ======================================================================
heading("5. Type hints")
for cls in (Supplier, Product, PhysicalProduct, DigitalProduct, CanBeShipped,
            Inventory, OrderLine, Order):
    missing = missing_type_hints(cls)
    check(f"{cls.__name__}: every parameter and return value has a type hint", not missing)
    for item in missing:
        print(f"      missing: {item}")

print("  Examples (these match the UML diagram):")
for method in (Product.__init__, Inventory.add_product, Inventory.remove_product,
               Inventory.find_product, Order.add_order_line, OrderLine.calculate_subtotal):
    signature = re.sub(r"\b[a-z_]+\.(?=[A-Z])", "", str(inspect.signature(method)))  # drop module names
    print(f"    {method.__qualname__}{signature}")

# ======================================================================
heading("6. Liskov Substitution Principle")
print("show_product_details(product: Product) with a PhysicalProduct, then a DigitalProduct:")
physical_output = captured_output(lambda: show_product_details(laptop))
digital_output = captured_output(lambda: show_product_details(antivirus))
print(physical_output + digital_output, end="")
check("the function works with a PhysicalProduct", "Requires physical shipping" in physical_output)
check("the same function works with a DigitalProduct, unchanged", "Delivered digitally" in digital_output)

print("\nExpectation set by Product: update_stock() accepts any whole number >= 0 and rejects negatives")
for product in (laptop, antivirus):
    product.update_stock(0)
    accepts_zero = product.get_stock() == 0
    product.update_stock(25)
    accepts_25 = product.get_stock() == 25
    try:
        product.update_stock(-1)
        rejects_negative = False
    except ValueError:
        rejects_negative = True
    check(f"{type(product).__name__} keeps the same update_stock() behaviour",
          accepts_zero and accepts_25 and rejects_negative)
check("both subclasses return a str from get_fulfilment_info(), as Product promises",
      isinstance(laptop.get_fulfilment_info(), str) and isinstance(antivirus.get_fulfilment_info(), str))

print("\nBoth product types used through the normal Inventory operations:")
shop = Inventory()
check("both types can be added to one Inventory", shop.add_product(laptop) and shop.add_product(antivirus))
check("find_product() returns either type",
      shop.find_product("p001") is laptop and shop.find_product("d001") is antivirus)
removed_digital = shop.remove_product("D001")
check("remove_product() works for either type", removed_digital is antivirus)
shop.add_product(antivirus)  # put it back for Section 7

print("\nDiagnose (6.3): the teammate's DigitalProduct that refuses update_stock()")
ebook = NoStockDigitalProduct("D998", "E-book", 9.90, 10, techsource, 5)
try:
    restock_all([laptop, ebook], 50)
    check("the teammate's subclass breaks code written for Product (LSP violation)", False)
except NotImplementedError as error:
    print(f"  NotImplementedError: {error}")
    check("the teammate's subclass breaks code written for Product (LSP violation)", True)

# ======================================================================
heading("7. Polymorphism through the Product type")
print("Predict first (7.2): what will each product print for get_fulfilment_info()?")
output = captured_output(lambda: show_all(shop))
print(output, end="")
check("the PhysicalProduct ran its own display_information()", "Type: Physical | Weight: 2.50 kg" in output)
check("the DigitalProduct ran its own display_information()", "Type: Digital | Download Size: 350.00 MB" in output)
check("each product ran its own get_fulfilment_info()",
      "Fulfilment: Requires physical shipping to the customer." in output
      and "Fulfilment: Delivered digitally through a download link." in output)

# ======================================================================
heading("Persistence: saving and loading keeps suppliers, links and product types")
with tempfile.TemporaryDirectory() as folder:
    test_file = os.path.join(folder, "test_inventory.json")  # never touches inventory.json
    with redirect_stdout(io.StringIO()):  # hide the loader's messages
        save_inventory(shop, [techsource, softhub], test_file)
        loaded_inventory, loaded_suppliers = load_inventory(test_file)
loaded_laptop = loaded_inventory.find_product("P001")
loaded_antivirus = loaded_inventory.find_product("D001")
check("both suppliers are restored (including one with no products)", len(loaded_suppliers) == 2)
check("product types are restored",
      isinstance(loaded_laptop, PhysicalProduct) and isinstance(loaded_antivirus, DigitalProduct))
check("each product is linked back to its supplier",
      loaded_laptop is not None and loaded_laptop.get_supplier().get_supplier_id() == "S001")
check("products that shared a supplier share ONE Supplier object again",
      loaded_laptop is not None and loaded_antivirus is not None
      and loaded_laptop.get_supplier() is loaded_antivirus.get_supplier())

print(f"\n{sum(results)}/{len(results)} checks passed.")
