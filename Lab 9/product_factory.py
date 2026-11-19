from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    """Factory pattern: the one place that decides which Product class to create.

    The rest of the program asks the factory for a Product and never needs to
    know about PhysicalProduct or DigitalProduct. A new product type means
    changing this factory only. That still breaks OCP here, but it keeps the
    change in one place, which is an acceptable trade-off for a small application.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float | None = None, download_size: float | None = None) -> Product:
        """Create a product of the given type ("physical" or "digital").

        weight (kg) is used for physical products and download_size (MB) for
        digital ones. Either can be left out when it isn't known.
        """
        kind = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        if kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        raise ValueError(f"Unknown product type: {product_type}")
