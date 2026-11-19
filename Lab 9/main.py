import csv

from supplier import Supplier
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)
from file_handler import load_inventory, save_inventory, load_products, INVENTORY_FILE
from input_helpers import (read_non_empty, get_positive_float, read_stock, read_quantity,
                           read_email, read_yes_no, read_product_type)

LINE = "-" * 48

DISCOUNT_OPTIONS: dict[str, DiscountStrategy] = {
    "1": NoDiscount(),
    "2": PercentageDiscount(10),
    "3": BulkDiscount(200, 20),
    "4": StudentDiscount(),
}

# ---------- Supplier actions ----------

def find_supplier(suppliers: list[Supplier], supplier_id: str) -> Supplier | None:
    for supplier in suppliers:
        if supplier.get_supplier_id().upper() == supplier_id.upper():
            return supplier
    return None


def add_supplier(suppliers: list[Supplier]) -> None:
    print("Add New Supplier")
    supplier_id = read_non_empty("Supplier ID: ")
    if find_supplier(suppliers, supplier_id) is not None:
        print("A supplier with this ID already exists.")
        return
    name = read_non_empty("Supplier Name: ")
    contact_email = read_email("Contact Email: ")
    suppliers.append(Supplier(supplier_id, name, contact_email))
    print("Supplier added successfully!")


def display_suppliers(suppliers: list[Supplier], inventory: Inventory) -> None:
    print("Suppliers")
    print(LINE)
    if not suppliers:
        print("No suppliers yet.")
    for supplier in suppliers:
        supplier.display_information()
        # A Supplier doesn't keep a product list (loose coupling), so ask each product instead
        names = [product.get_name() for product in inventory.get_products()
                 if product.get_supplier() is supplier]
        print(f"    Supplies: {', '.join(names) if names else 'no products yet'}")
    print(LINE)


def choose_supplier(suppliers: list[Supplier]) -> Supplier:
    """Show the suppliers and keep asking until the user picks one of them."""
    print("Suppliers:")
    for supplier in suppliers:
        supplier.display_information()
    while True:
        supplier = find_supplier(suppliers, read_non_empty("Supplier ID: "))
        if supplier is not None:
            return supplier
        print("Supplier not found. Please enter one of the IDs above.")


# ---------- Product actions (call Inventory / Product methods) ----------

def add_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("Add New Product")
    if not suppliers:
        print("No suppliers yet. Please add a supplier first (option 6).")
        return
    product_type = read_product_type()
    product_id = read_non_empty("Product ID: ")
    if inventory.find_product(product_id) is not None:
        print("A product with this ID already exists.")
        return
    name = read_non_empty("Product Name: ")
    price = get_positive_float("Price: ")
    stock = read_stock("Stock Quantity: ")
    supplier = choose_supplier(suppliers)  # association: pass in an existing Supplier object

    weight: float | None = None
    download_size: float | None = None
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download Size (MB): ")
    try:
        # Factory pattern: main.py never creates a PhysicalProduct or DigitalProduct itself
        product = ProductFactory.create(product_type, product_id, name, price, stock,
                                        supplier, weight=weight, download_size=download_size)
    except ValueError as error:
        print(f"Product not added: {error}")
        return
    
    inventory.add_product(product)
    print("Product added successfully!")


def remove_product(inventory: Inventory) -> None:
    print("Remove Product")
    product = inventory.remove_product(read_non_empty("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print(f"Removed {product.get_name()} ({product.get_product_id()}) from the inventory.")


def update_stock(inventory: Inventory) -> None:
    print("Update Stock")
    product = inventory.find_product(read_non_empty("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    product.update_stock(read_stock("New Stock Quantity: "))
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("Search Product")
    product = inventory.find_product(read_non_empty("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    # Shipping is an optional capability (the CanBeShipped interface), not part of Product
    if isinstance(product, CanBeShipped):
        try:
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        except ValueError as error:
            print(f"Shipping Cost: unavailable - {error}")
    print("Supplied by:")
    product.get_supplier().display_information()  # reached through the association
    print(LINE)

def import_products(inventory: Inventory, suppliers: list[Supplier]) -> None:
    print("Import Products from CSV")
    if not suppliers:
        print("No suppliers yet. Please add a supplier first (option 6).")
        return
    path = input("CSV file name (press Enter for products.csv): ").strip() or "products.csv"
    supplier = choose_supplier(suppliers)  # every imported product gets this supplier
    try:
        load_products(path, inventory, supplier)
    except (UnicodeDecodeError, csv.Error):
        print("That file could not be read as a CSV file, so nothing more was imported.")


# ---------- Order actions ----------

def find_order(orders: list[Order], order_id: str) -> Order | None:
    for order in orders:
        if order.get_order_id().upper() == order_id.upper():
            return order
    return None

def choose_discount() -> DiscountStrategy:
    """Show the discount options and return the chosen strategy object."""
    print("Discounts:")
    for key, discount in DISCOUNT_OPTIONS.items():
        print(f"{key}. {discount}")
    while True:
        choice = input("Choose discount: ").strip()
        if choice in DISCOUNT_OPTIONS:
            return DISCOUNT_OPTIONS[choice]
        print(f"Please enter a number from 1 to {len(DISCOUNT_OPTIONS)}.")

def create_order(inventory: Inventory, orders: list[Order]) -> None:
    print("Create Order")
    order_id = read_non_empty("Order ID: ")
    if find_order(orders, order_id) is not None:
        print("An order with this ID already exists.")
        return
    order = Order(order_id, choose_discount()) 
    print("Add products to the order. Leave the Product ID blank when you are done.")
    while True:
        product_id = input("Product ID: ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = read_quantity("Quantity: ")
        order.add_order_line(product, quantity)  # the Order creates the OrderLine itself
        print(f"Added {quantity} x {product.get_name()}.")

    if not order.get_order_lines():
        print("No products were added, so the order was not created.")
        return
    orders.append(order)
    print("Order created successfully!")
    order.display_order()

def change_order_discount(orders: list[Order]) -> None:
    print("Change Order Discount")
    order = find_order(orders, read_non_empty("Order ID: "))
    if order is None:
        print("Order not found.")
        return
    print(f"Current discount: {order.get_discount()}")
    order.set_discount(choose_discount())  # swap the strategy - Order itself doesn't change
    print("Discount updated.")
    order.display_order()

def view_orders(orders: list[Order]) -> None:
    if not orders:
        print("No orders yet.")
        return
    for order in orders:
        order.display_order()

def try_save(inventory: Inventory, suppliers: list[Supplier]) -> bool:
    """Save, reporting a problem instead of crashing. Returns True if the save worked."""
    try:
        save_inventory(inventory, suppliers)
    except OSError as error:
        print(f"Could not save to {INVENTORY_FILE}: {error.strerror or error}.")
        return False
    return True

def print_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Remove Product")
    print("4. Update Stock")
    print("5. Search Product")
    print("6. Add Supplier")
    print("7. Display Suppliers")
    print("8. Create Order")
    print("9. View Orders")
    print("10. Change Order Discount")
    print("11. Import Products from CSV")
    print("12. Save Inventory")
    print("13. Exit")
    print("----------------------------")


def run_menu(inventory: Inventory, suppliers: list[Supplier]) -> None:
    orders: list[Order] = []  # orders are kept while the program is running
    print_menu()
    while True:
        option = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product(inventory, suppliers)
        elif option == "3":
            remove_product(inventory)
        elif option == "4":
            update_stock(inventory)
        elif option == "5":
            search_product(inventory)
        elif option == "6":
            add_supplier(suppliers)
        elif option == "7":
            display_suppliers(suppliers, inventory)
        elif option == "8":
            create_order(inventory, orders)
        elif option == "9":
            view_orders(orders)
        elif option == "10":
            change_order_discount(orders)
        elif option == "11":
            import_products(inventory, suppliers)
        elif option == "12":
            print("Saving inventory...")
            if try_save(inventory, suppliers):
                print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "13":
            print("Saving inventory before exit...")
            if try_save(inventory, suppliers):
                print("Inventory saved successfully.")
            elif not read_yes_no("Exit without saving? (y/n): "):
                continue  # stay in the menu so the user can fix the problem and try again
            print("Program exited.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 13.")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory, suppliers = load_inventory()
    try:
        run_menu(inventory, suppliers)
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped. Changes since your last save were not saved.")


if __name__ == "__main__":
    main()
