from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount 

LINE = "-" * 48


class Order:


    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Swap in a different discount strategy. Order itself does not change."""
        self.__discount = discount

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

    def calculate_subtotal(self) -> float:
        """Add up the subtotal that each OrderLine calculates for itself."""
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return round(total, 2)
    
    def calculate_total(self) -> float:
        """Pass the subtotal to the discount strategy - the Order doesn't know how it works."""
        return round(self.__discount.apply(self.calculate_subtotal()), 2)
    
    def display_order(self) -> None:
        print(f"Order {self.__order_id}")
        print(LINE)
        if not self.__order_lines:
            print("No items in this order.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(LINE)
        subtotal = self.calculate_subtotal()
        total = self.calculate_total()
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Discount: {self.__discount} (-${subtotal - total:.2f})")
        print(f"Total: ${total:.2f}")

