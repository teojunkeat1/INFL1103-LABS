from abc import ABC, abstractmethod


class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    # ---------- Getters (read-only access from outside) ----------

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # ---------- Regular methods: implemented here, reused by every subclass ----------

    def update_stock(self, quantity):
        """Set a new stock level. The Product decides what values are allowed."""
        if not isinstance(quantity, int):
            raise TypeError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        """Print the details every product has. Subclasses add their own details using super()."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # ---------- Abstract method: no implementation, every subclass MUST provide one ----------

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a message explaining how this product is delivered to the customer."""
        pass
