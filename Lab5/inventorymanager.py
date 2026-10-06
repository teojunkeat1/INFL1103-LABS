
import json
 
INVENTORY_FILE = "inventory.json"
LINE = "-" * 48
 
 

def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")
 
 
def read_price(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            print("Price cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")
 
 
def read_stock(prompt):
    """Keep asking until the user types a non-negative whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            print("Stock cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")
 
 
# ---------- Data persistence ----------
 
def load_inventory():
    """Load inventory.json if it exists, otherwise start with an empty list."""
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
        return []
    except json.JSONDecodeError:
        print("inventory.json is corrupted. Starting with an empty inventory.")
        return []
 
 
def save_inventory(inventory):
    """Overwrite inventory.json with the current inventory."""
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)
 

 
def find_product(inventory, product_id):
    """Return the product dictionary with this ID, or None."""
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None
 
 
def display_all(inventory):
    print("Current Inventory")
    print(LINE)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print(LINE)
 
 
def add_product(inventory):
    print("Add New Product")
    product_id = read_non_empty("Product ID: ")
    if find_product(inventory, product_id):
        print("A product with this ID already exists.")
        return
    name = read_non_empty("Product Name: ")
    price = read_price("Price: ")
    stock = read_stock("Stock Quantity: ")
 
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")
 
 
def update_stock(inventory):
    print("Update Stock")
    product = find_product(inventory, read_non_empty("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    product["stock"] = read_stock("New Stock Quantity: ")
    print("Stock updated successfully!")
 
 
def search_product(inventory):
    print("Search Product")
    product = find_product(inventory, read_non_empty("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print("Product Found")
    print(LINE)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print(LINE)
 
 
def print_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")
 
 
def run_menu(inventory):
    print_menu()
    while True:
        option = input("Enter option: ").strip()
        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {INVENTORY_FILE}.")
        elif option == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Program exited.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
 
 
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()
    run_menu(inventory)

main()