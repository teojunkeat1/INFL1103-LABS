from product import Product
from order_line import OrderLine

LINE = "-" * 48


class Order:
    """A customer order made up of OrderLine objects.

    Composition: the Order creates its own OrderLine objects inside
    add_order_line() and is the only thing that manages them. The lines
    belong to this Order alone - when the Order goes away, its lines go too.
    """

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and add it to the order."""
        order_line = OrderLine(product, quantity)  # the Order creates its own part
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns False if the order has no such line."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        """Return a copy of the list, so lines can only be added or removed through the Order."""
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        """Add up the subtotal that each OrderLine calculates for itself."""
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return round(total, 2)

    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print(LINE)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(LINE)
        print(f"Total: ${self.calculate_total():.2f}")
