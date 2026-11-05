from product import Product


class DigitalProduct(Product):


    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)  # reuse Product's constructor
        if download_size <= 0:
            raise ValueError("Download size must be greater than 0.")
        self.__download_size = float(download_size)  # size in megabytes

    def get_download_size(self):
        return self.__download_size

    # Overrides Product.display_information()
    def display_information(self):
        super().display_information()  # parent prints the common product details
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")

    # Implements the abstract method from Product
    def get_fulfilment_info(self):
        return "Delivered digitally through a download link."
