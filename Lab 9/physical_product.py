from supplier import Supplier
from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # Product validates and stores these
        if weight is not None and weight <= 0:
            raise ValueError("Weight must be greater than zero.")
        self.__weight: float | None = None if weight is None else float(weight)  # kilograms


    def get_weight(self) -> float | None:
        return self.__weight

    # Overrides Product.display_information()
    def display_information(self) -> None:
        super().display_information()  # parent prints the common product details
        weight_text = "not recorded" if self.__weight is None else f"{self.__weight:.2f} kg"
        print(f"    Type: Physical | Weight: {weight_text}")


    # Implements the abstract method from Product
    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping to the customer."

    # Implements the CanBeShipped interface
    def calculate_shipping_cost(self) -> float:
        """Shipping rule: $5.00 flat fee plus $2.00 for every kg."""
        if self.__weight is None:
            raise ValueError("weight not recorded, so the shipping cost can't be calculated.")
        base_fee = 5.00
        rate_per_kg = 2.00
        return round(base_fee + self.__weight * rate_per_kg, 2)
