from product import Product
from canbeshipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
  
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)  # reuse Product's constructor
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        self.__weight = float(weight)  # weight in kilograms

    def get_weight(self):
        return self.__weight

    # Overrides Product.display_information()
    def display_information(self):
        super().display_information()  # parent prints the common product details
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    # Implements the abstract method from Product
    def get_fulfilment_info(self):
        return "Requires physical shipping to the customer."

    # Implements the CanBeShipped interface
    def calculate_shipping_cost(self):
        """Shipping rule: $5.00 flat fee plus $2.00 for every kg."""
        base_fee = 5.00
        rate_per_kg = 2.00
        return round(base_fee + self.__weight * rate_per_kg, 2)
