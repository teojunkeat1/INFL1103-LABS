from product import Product

LINE = "-" * 48


class Inventory:
    """Manages a collection of Product objects (SRP).

    Aggregation: an Inventory is a whole made up of Products, but it does not
    create or own them. Products exist before they are added, and removing a
    product only removes the reference - the Product object itself carries on
    and can be added to another Inventory.
    """

    def __init__(self) -> None:
        # Typed with the base class Product, so it can hold ANY kind of product (LSP)
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if a product with the same ID is already here."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the product's reference from this inventory and hand the Product back.

        The Product is not destroyed: the caller can keep using it or add it to
        another inventory. Returns None if no product has this ID.
        """
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with this ID (case-insensitive), or None."""
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def display_all_products(self) -> None:
        print("Current Inventory")
        print(LINE)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()  # each product runs its own version (polymorphism)
        print(LINE)

    def get_products(self) -> list[Product]:
        """Return a copy of the list so outside code can't change the internal list."""
        return list(self.__products)
