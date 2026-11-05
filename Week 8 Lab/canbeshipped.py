from abc import ABC, abstractmethod


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this item, in dollars."""
        pass
