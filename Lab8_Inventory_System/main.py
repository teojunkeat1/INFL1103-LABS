from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order
from file_handler import load_inventory, save_inventory, INVENTORY_FILE

LINE = "-" * 48


# ---------- Input helpers (main program is responsible for user input) ----------

def read_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def read_price(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Price cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")


def read_positive_number(prompt: str) -> float:
    """Keep asking until the user types a number greater than 0 (weight, download size)."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Value must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")


def read_stock(prompt: str) -> int:
    """Keep asking until the user types a non-negative whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Stock cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")


def read_quantity(prompt: str) -> int:
    """Keep asking until the user types a whole number greater than 0."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Quantity must be greater than 0.")
        except ValueError:
            print("Please enter a whole number.")


def read_email(prompt: str) -> str:
    while True:
        value = read_non_empty(prompt)
        if "@" in value:
            return value
        print("Please enter a valid email address (it must contain @).")


def read_product_type() -> str:
    """Ask whether the new product is physical or digital."""
    print("Product Type:")
    print("1. Physical Product (shipped, has a weight)")
    print("2. Digital Product (downloaded, has a download size)")
    while True:
        choice = input("Choose type (1-2): ").strip()
        if choice == "1":
            return "physical"
        if choice == "2":
            return "digital"
        print("Please enter 1 or 2.")


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
    price = read_price("Price: ")
    stock = read_stock("Stock Quantity: ")
    supplier = choose_supplier(suppliers)  # association: pass in an existing Supplier object

    product: Product  # either subclass can be used wherever a Product is expected
    if product_type == "physical":
        weight = read_positive_number("Weight (kg): ")
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = read_positive_number("Download Size (MB): ")
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

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
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("Supplied by:")
    product.get_supplier().display_information()  # reached through the association
    print(LINE)


# ---------- Order actions ----------

def find_order(orders: list[Order], order_id: str) -> Order | None:
    for order in orders:
        if order.get_order_id().upper() == order_id.upper():
            return order
    return None


def create_order(inventory: Inventory, orders: list[Order]) -> None:
    print("Create Order")
    order_id = read_non_empty("Order ID: ")
    if find_order(orders, order_id) is not None:
        print("An order with this ID already exists.")
        return
    order = Order(order_id)
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


def view_orders(orders: list[Order]) -> None:
    if not orders:
        print("No orders yet.")
        return
    for order in orders:
        order.display_order()


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
    print("10. Save Inventory")
    print("11. Exit")
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
            print("Saving inventory...")
            save_inventory(inventory, suppliers)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "11":
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Inventory saved successfully.")
            print("Program exited.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 11.")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory, suppliers = load_inventory()
    run_menu(inventory, suppliers)


if __name__ == "__main__":
    main()
