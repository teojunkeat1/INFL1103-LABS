from supplier import Supplier
from product import Product


class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float | None = None) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # Product validates and stores these
        if download_size is not None and download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.__download_size: float | None = None if download_size is None else float(download_size)  # MB


    def get_download_size(self) -> float | None:
        return self.__download_size

    # Overrides Product.display_information()
    def display_information(self) -> None:
        super().display_information()  # parent prints the common product details
        size_text = "not recorded" if self.__download_size is None else f"{self.__download_size:.2f} MB"
        print(f"    Type: Digital | Download Size: {size_text}")


    # Implements the abstract method from Product
    def get_fulfilment_info(self) -> str:
        return "Delivered digitally through a download link."
