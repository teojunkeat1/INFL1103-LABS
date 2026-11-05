import json

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def product_to_dict(product):
    """Convert a Product object into a dictionary, including its type identifier."""
    if isinstance(product, PhysicalProduct):
        product_type = "physical"
    elif isinstance(product, DigitalProduct):
        product_type = "digital"
    else:
        raise ValueError(f"Cannot save unknown product type: {type(product).__name__}")

    data = {
        "type": product_type,
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
    }

    # Add the extra attribute that only this product type has
    if product_type == "physical":
        data["weight"] = product.get_weight()
    else:
        data["download_size"] = product.get_download_size()
    return data


def dict_to_product(item):
    """Use the saved "type" identifier to rebuild the correct subclass."""
    product_type = item.get("type")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"],
                               item["stock"], item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"],
                              item["stock"], item["download_size"])
    raise ValueError(f"Unknown or missing product type: {product_type}")


def load_inventory(filename=INVENTORY_FILE):
    """Read the JSON file and rebuild an Inventory of PhysicalProduct / DigitalProduct objects."""
    inventory = Inventory()
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} is missing. Starting with an empty inventory.")
        return inventory
    except json.JSONDecodeError:
        print(f"{filename} is corrupted. Starting with an empty inventory.")
        return inventory

    if not isinstance(data, list):
        print(f"{filename} is corrupted. Starting with an empty inventory.")
        return inventory

    print(f"{filename} found.")
    skipped = 0
    for item in data:
        try:
            product = dict_to_product(item)
        except (KeyError, TypeError, ValueError, AttributeError):
            print(f"Skipped invalid product record: {item}")
            skipped += 1
            continue
        if not inventory.add_product(product):
            print(f"Skipped duplicate product ID: {product.get_product_id()}")
            skipped += 1

    print("Inventory loaded successfully.")
    if skipped:
        print(f"Warning: {skipped} record(s) were skipped and will not be kept when you save.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Convert each product to a dictionary and write the list to JSON."""
    data = [product_to_dict(product) for product in inventory.get_products()]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
