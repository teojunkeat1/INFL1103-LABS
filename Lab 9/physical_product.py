from supplier import Supplier
from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that physically exists, so it has a weight and can be shipped.

    Inheritance (is-a):         a PhysicalProduct is-a Product (its one parent class).
    Interface (can-be-shipped): it implements the CanBeShipped interface.
    CanBeShipped is a contract, not a second parent class, so this is still
    single class inheritance plus one interface.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # Product stores the supplier
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        self.__weight: float = float(weight)  # weight in kilograms

    def get_weight(self) -> float:
        return self.__weight

    # Overrides Product.display_information()
    def display_information(self) -> None:
        super().display_information()  # parent prints the common product details
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    # Implements the abstract method from Product
    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping to the customer."

    # Implements the CanBeShipped interface
    def calculate_shipping_cost(self) -> float:
        """Shipping rule: $5.00 flat fee plus $2.00 for every kg."""
        base_fee = 5.00
        rate_per_kg = 2.00
        return round(base_fee + self.__weight * rate_per_kg, 2)
