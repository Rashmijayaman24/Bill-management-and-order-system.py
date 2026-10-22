from abc import ABC, abstractmethod


class ShipmentOrder(ABC):

    def __init__(self, client_name, goods, reduction_rate=0.0):
        self.client_name = client_name
        self._goods = goods                          # protected: dict of item -> price
        self.__reduction_rate = reduction_rate       # encapsulation
        self.__settled_amount = 0.0                  # encapsulation

    @abstractmethod                                  # abstract
    def compute_amount(self):
        """Return the full amount payable for this order."""

    @abstractmethod                                  # abstract
    def order_kind(self):
        """Return the type of order."""

    def _items_cost(self):
        return sum(self._goods.values())

    def _apply_reduction(self, amount):
        return amount * (1 - self.__reduction_rate)

    @property                                        # encapsulation (read-only)
    def amount_settled(self):
        return self.__settled_amount

    def submit_payment(self, amount):
        pending = self.pending_amount()
        if amount <= 0:
            print("  Payment declined: amount must be greater than zero.")
        elif round(amount, 2) > pending:
            print(f"  Payment declined: only Rs. {pending:.2f} is pending.")
        else:
            self.__settled_amount += amount
            print(f"  Rs. {amount:.2f} payment accepted.")

    def pending_amount(self):
        return round(self.compute_amount() - self.__settled_amount, 2)

    def show_order_details(self):
        print(f"##### {self.order_kind()} #####")
        print(f"  Client     : {self.client_name}")
        print(f"  Goods      : {', '.join(self._goods)}")
        print(f"  Amount Due : Rs. {self.compute_amount():.2f}")
        print(f"  Settled    : Rs. {self.amount_settled:.2f}")
        print(f"  Pending    : Rs. {self.pending_amount():.2f}")


# inheritance + method overriding
class CafeOrder(ShipmentOrder):
    HANDLING_RATE = 0.12
    SHIPPING_PER_KM = 65.0
    PRIORITY_FEE = 300.0

    def __init__(self, client_name, goods, trip_km, priority=False, reduction_rate=0.0):
        super().__init__(client_name, goods, reduction_rate)
        self.__trip_km = trip_km
        self.__priority = priority

    def compute_amount(self):                        # overriding
        base = self._items_cost()
        handling = base * self.HANDLING_RATE
        shipping = self.__trip_km * self.SHIPPING_PER_KM
        rush = self.PRIORITY_FEE if self.__priority else 0.0
        return self._apply_reduction(base + handling) + shipping + rush

    def order_kind(self):                            # overriding
        return "Cafe Order"


class SupermarketOrder(ShipmentOrder):
    WRAP_PER_ITEM = 25.0
    SHIPPING_PER_KM = 45.0

    def __init__(self, client_name, goods, trip_km, reduction_rate=0.0):
        super().__init__(client_name, goods, reduction_rate)
        self.__trip_km = trip_km

    def compute_amount(self):                        # overriding
        base = self._items_cost()
        wrapping = len(self._goods) * self.WRAP_PER_ITEM
        shipping = self.__trip_km * self.SHIPPING_PER_KM
        return self._apply_reduction(base) + wrapping + shipping

    def order_kind(self):                            # overriding
        return "Supermarket Order"


class PastryOrder(ShipmentOrder):
    BOX_FEE = 200.0
    SHIPPING_PER_KM = 55.0

    def __init__(self, client_name, goods, trip_km, reduction_rate=0.0):
        super().__init__(client_name, goods, reduction_rate)
        self.__trip_km = trip_km

    def compute_amount(self):                        # overriding
        base = self._items_cost()
        shipping = self.__trip_km * self.SHIPPING_PER_KM
        return self._apply_reduction(base) + self.BOX_FEE + shipping

    def order_kind(self):                            # overriding
        return "Pastry Order"


if __name__ == "__main__":
    order_list = [
        CafeOrder("Nadeesha", {"Kottu": 1400, "Devilled Chicken": 1250, "Iced Tea": 350},
                  trip_km=6, priority=True, reduction_rate=0.05),
        SupermarketOrder("Tharindu", {"Flour 2kg": 620, "Sugar 1kg": 280,
                                      "Tea 400g": 950, "Coconut Oil": 780},
                         trip_km=2, reduction_rate=0.08),
        PastryOrder("Sithara", {"Chocolate Cake": 4200, "Butter Buns": 650},
                    trip_km=7, reduction_rate=0.15),
    ]

    # Polymorphism
    print(">>> Order Details <<<")
    for entry in order_list:
        entry.show_order_details()
        print()

    # Payments through a controlled method
    print(">>> Payment Processing <<<")
    order_list[0].submit_payment(1500)
    order_list[0].submit_payment(-75)        # declined: negative
    order_list[1].submit_payment(50000)      # declined: too much
    order_list[2].submit_payment(3000)

    print("\n>>> Updated Order Details <<<")
    for entry in order_list:
        entry.show_order_details()
        print()

    # Encapsulation check
    print(">>> Encapsulation check <<<")
    try:
        order_list[0].amount_settled = 0
    except AttributeError as e:
        print("Cannot modify amount_settled ->", e)

    # Abstraction check
    try:
        ShipmentOrder("Test", {})
    except TypeError as e:
        print("Cannot create abstract class object ->", e)