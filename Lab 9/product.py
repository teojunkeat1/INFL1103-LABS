from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
    
        if not isinstance(supplier, Supplier):
            raise TypeError("supplier must be a Supplier object, not a name or ID.")
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier  

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier


    def update_stock(self, quantity: int) -> None:
        """Set a new stock level. Every Product accepts any whole number of 0 or more."""
        if not isinstance(quantity, int):
            raise TypeError("Stock must be a whole number.")
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        """Print the details every product has. Subclasses add their own details using super()."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
              f"Supplier: {self.__supplier.get_name()}")


    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message explaining how this product is delivered to the customer."""
        pass
