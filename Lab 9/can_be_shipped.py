from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style abstract base class: a contract for anything that can be shipped.

    It has no attributes and no implementation details. Any class that
    implements ("signs") this interface must provide calculate_shipping_cost().
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the cost of shipping this item, in dollars."""
        pass
