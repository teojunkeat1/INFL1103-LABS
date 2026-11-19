import json

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory

INVENTORY_FILE = "inventory.json"


def supplier_to_dict(supplier: Supplier) -> dict[str, str]:
    """Convert a Supplier object into a dictionary that can be saved as JSON."""
    return {
        "id": supplier.get_supplier_id(),
        "name": supplier.get_name(),
        "contact_email": supplier.get_contact_email(),
    }


def dict_to_supplier(item: dict[str, str]) -> Supplier:
    """Rebuild a Supplier object from its saved dictionary."""
    return Supplier(str(item["id"]), str(item["name"]), str(item["contact_email"]))


def product_to_dict(product: Product) -> dict[str, str | float | int]:
    """Convert a Product into a dictionary. The supplier is saved by its ID, not copied."""
    if isinstance(product, PhysicalProduct):
        product_type, extra_key, extra_value = "physical", "weight", product.get_weight()
    elif isinstance(product, DigitalProduct):
        product_type, extra_key, extra_value = "digital", "download_size", product.get_download_size()
    else:
        raise ValueError(f"Cannot save unknown product type: {type(product).__name__}")

    return {
        "type": product_type,
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
        "supplier_id": product.get_supplier().get_supplier_id(),
        extra_key: extra_value,
    }


def dict_to_product(item: dict[str, str | float | int],
                    suppliers_by_id: dict[str, Supplier]) -> Product:
    """Use the saved "type" to rebuild the right subclass, linked to its existing Supplier."""
    supplier = suppliers_by_id.get(str(item.get("supplier_id", "")).upper())
    if supplier is None:
        raise ValueError(f"Unknown supplier: {item.get('supplier_id')}")

    product_type = item.get("type")
    if product_type == "physical":
        return PhysicalProduct(str(item["id"]), str(item["name"]), float(item["price"]),
                               int(item["stock"]), supplier, float(item["weight"]))
    if product_type == "digital":
        return DigitalProduct(str(item["id"]), str(item["name"]), float(item["price"]),
                              int(item["stock"]), supplier, float(item["download_size"]))
    raise ValueError(f"Unknown or missing product type: {product_type}")


def load_inventory(filename: str = INVENTORY_FILE) -> tuple[Inventory, list[Supplier]]:
    """Read the JSON file: rebuild the suppliers first, then the products that refer to them."""
    inventory = Inventory()
    suppliers: list[Supplier] = []
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} is missing. Starting with an empty inventory.")
        return inventory, suppliers
    except json.JSONDecodeError:
        print(f"{filename} is corrupted. Starting with an empty inventory.")
        return inventory, suppliers

    if isinstance(data, list):
        print(f"{filename} uses the old Lab 7 format (no suppliers). Starting with an empty inventory.")
        print("Warning: the old products will not be kept when you save.")
        return inventory, suppliers
    if (not isinstance(data, dict) or not isinstance(data.get("suppliers"), list)
            or not isinstance(data.get("products"), list)):
        print(f"{filename} is corrupted. Starting with an empty inventory.")
        return inventory, suppliers

    print(f"{filename} found.")
    skipped = 0

    # 1. Suppliers first, so that products can be linked to them
    suppliers_by_id: dict[str, Supplier] = {}
    for item in data["suppliers"]:
        try:
            supplier = dict_to_supplier(item)
        except (KeyError, TypeError, ValueError):
            print(f"Skipped invalid supplier record: {item}")
            skipped += 1
            continue
        key = supplier.get_supplier_id().upper()
        if key in suppliers_by_id:
            print(f"Skipped duplicate supplier ID: {supplier.get_supplier_id()}")
            skipped += 1
            continue
        suppliers_by_id[key] = supplier
        suppliers.append(supplier)

    # 2. Products - products with the same supplier ID share ONE Supplier object
    for item in data["products"]:
        try:
            product = dict_to_product(item, suppliers_by_id)
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
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: list[Supplier],
                   filename: str = INVENTORY_FILE) -> None:
    """Save the suppliers and the products (each product stores its supplier's ID)."""
    data = {
        "suppliers": [supplier_to_dict(supplier) for supplier in suppliers],
        "products": [product_to_dict(product) for product in inventory.get_products()],
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
