
import json
 
from product import Product
from inventory import Inventory
 
INVENTORY_FILE = "inventory.json"
 
 
def load_inventory(filename=INVENTORY_FILE):
    """Read the JSON file and rebuild an Inventory of Product objects."""
    inventory = Inventory()
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"{filename} found.")
        for item in data:
            product = Product(item["id"], item["name"], item["price"], item["stock"])
            inventory.add_product(product)
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print(f"{filename} is missing. Starting with an empty inventory.")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(f"{filename} is corrupted. Starting with an empty inventory.")
        inventory = Inventory()
    return inventory
 
 
def save_inventory(inventory, filename=INVENTORY_FILE):
    """Convert each Product back to a dictionary and write the list to JSON."""
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)