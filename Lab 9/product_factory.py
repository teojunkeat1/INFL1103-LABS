from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float | None = None, download_size: float | None = None) -> Product:
 
        kind = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight)
        if kind == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size)
        raise ValueError(f"Unknown product type: {product_type}")
