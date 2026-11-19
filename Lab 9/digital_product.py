from supplier import Supplier
from product import Product


class DigitalProduct(Product):
    """A product delivered as a download, so it has a download size instead of a weight.

    A DigitalProduct is-a Product. It does NOT implement CanBeShipped,
    because digital products are never physically shipped. Its stock is the
    number of licences available, so it keeps Product's update_stock() as it is.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # Product stores the supplier
        if download_size <= 0:
            raise ValueError("Download size must be greater than 0.")
        self.__download_size: float = float(download_size)  # size in megabytes

    def get_download_size(self) -> float:
        return self.__download_size

    # Overrides Product.display_information()
    def display_information(self) -> None:
        super().display_information()  # parent prints the common product details
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    # Implements the abstract method from Product
    def get_fulfilment_info(self) -> str:
        return "Delivered digitally through a download link."
