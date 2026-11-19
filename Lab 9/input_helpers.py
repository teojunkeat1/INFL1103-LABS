def read_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_positive_float(prompt: str) -> float:
    """Section 5.1: ask for a number greater than zero (price, weight, download size)."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def read_stock(prompt: str) -> int:
    """Ask for a stock quantity: a whole number of 0 or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Stock cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def read_quantity(prompt: str) -> int:
    """Ask for an order quantity: a whole number greater than 0."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Quantity must be greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number.")


def read_email(prompt: str) -> str:
    while True:
        value = read_non_empty(prompt)
        if "@" in value:
            return value
        print("Please enter a valid email address (it must contain @).")


def read_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


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
