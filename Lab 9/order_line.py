from product import Product


class OrderLine:


    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("product must be a Product object.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")
        # Validation: the OrderLine protects its own quantity instead of trusting every caller
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product  # a reference to an existing Product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        """Price of the product multiplied by the quantity ordered."""
        return round(self.__product.get_price() * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} ({self.__product.get_product_id()}) "
              f"x {self.__quantity} @ ${self.__product.get_price():.2f} "
              f"= ${self.calculate_subtotal():.2f}")
