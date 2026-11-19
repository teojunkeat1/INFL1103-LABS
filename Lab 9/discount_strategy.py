from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: one interchangeable way of discounting an order total.

    Every strategy provides the same apply() method, so an Order can use any of
    them without knowing how it works. A new discount means a new class here,
    not a change to Order (Open/Closed Principle).
    """

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after this discount is applied."""
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged. An Order uses this when no discount is given."""

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        # Validation: the strategy protects its own rule
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and no more than 100.")
        self.__percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (100 - self.__percentage) / 100

    def __str__(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold, e.g. BulkDiscount(200, 20)."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)  # a discount never makes the total negative
        return total

    def __str__(self) -> str:
        return f"${self.__amount:.2f} off orders of ${self.__threshold:.2f} or more"


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a fourth strategy (5% off for students), added without changing Order."""

    def apply(self, total: float) -> float:
        return total * 0.95

    def __str__(self) -> str:
        return "Student discount (5% off)"
