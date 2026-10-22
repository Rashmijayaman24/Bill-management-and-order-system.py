from abc import ABC, abstractmethod


class MedicalService(ABC):
    def __init__(self, patient_full_name, insurance_share=0.0, discount_share=0.0):
        if not (0 <= insurance_share <= 1 and 0 <= discount_share <= 1):
            raise ValueError("Shares must be between 0 and 1.")
        self.patient_full_name = patient_full_name
        self.__money_paid = 0.0                          # encapsulation
        self.__insurance_share = insurance_share         # encapsulation
        self.__discount_share = discount_share           # encapsulation

    @abstractmethod                                      # abstract
    def compute_total_charge(self):
        """Return the total charge for this service."""

    @abstractmethod                                      # abstract
    def service_label(self):
        """Return the name of the service."""

    def _apply_reductions(self, starting_charge):
        discounted = starting_charge * (1 - self.__discount_share)
        return discounted * (1 - self.__insurance_share)

    @property                                            # encapsulation (read-only)
    def paid_amount(self):
        return self.__money_paid

    def make_payment(self, amount):
        pending = self.remaining_balance()
        if amount <= 0:
            print("  Payment declined: amount must be positive.")
        elif round(amount, 2) > pending:
            print(f"  Payment declined: exceeds remaining balance (Rs. {pending:.2f}).")
        else:
            self.__money_paid += amount
            print(f"  Payment of Rs. {amount:.2f} received.")

    def remaining_balance(self):
        return round(self.compute_total_charge() - self.__money_paid, 2)

    def display_summary(self):
        print(f"===== {self.service_label()} =====")
        print(f"  Patient       : {self.patient_full_name}")
        print(f"  Total charge  : Rs. {self.compute_total_charge():.2f}")
        print(f"  Amount paid   : Rs. {self.paid_amount:.2f}")
        print(f"  Balance left  : Rs. {self.remaining_balance():.2f}")


# inheritance + method overriding
class GeneralCheckup(MedicalService):
    CHECKUP_FEE = 1500.0

    def compute_total_charge(self):                      # overriding
        return self._apply_reductions(self.CHECKUP_FEE)

    def service_label(self):                             # overriding
        return "General Checkup"


class SpecialistVisit(MedicalService):
    RESERVATION_FEE = 500.0

    def __init__(self, patient_full_name, doctor_fee, **options):
        super().__init__(patient_full_name, **options)
        self.__doctor_fee = doctor_fee                   # private

    def compute_total_charge(self):                      # overriding
        return self._apply_reductions(self.__doctor_fee + self.RESERVATION_FEE)

    def service_label(self):                             # overriding
        return "Specialist Visit"


class LabExamination(MedicalService):
    def __init__(self, patient_full_name, exam_fees, **options):
        super().__init__(patient_full_name, **options)
        self.__exam_fees = list(exam_fees)               # private list of fees

    def compute_total_charge(self):                      # overriding
        return self._apply_reductions(sum(self.__exam_fees))

    def service_label(self):                             # overriding
        return "Laboratory Examination"


class EmergencyCare(MedicalService):
    ER_SURCHARGE = 5000.0

    def __init__(self, patient_full_name, care_cost, **options):
        super().__init__(patient_full_name, **options)
        self.__care_cost = care_cost                     # private

    def compute_total_charge(self):                      # overriding
        return self._apply_reductions(self.__care_cost + self.ER_SURCHARGE)

    def service_label(self):                             # overriding
        return "Emergency Care"


if __name__ == "__main__":
    service_list = [
        GeneralCheckup("rashmi"),
        SpecialistVisit("nethmi", doctor_fee=4000, insurance_share=0.5),
        LabExamination("Saman", exam_fees=[1200, 800, 2500], discount_share=0.1),
        EmergencyCare("kasun", care_cost=15000, insurance_share=0.6),
    ]

    # Polymorphism
    print("=== Bills ===")
    for item in service_list:
        item.display_summary()

    # Payments through a controlled method
    print("\n=== Payments ===")
    service_list[0].make_payment(1000)
    service_list[0].make_payment(-50)      # declined: negative amount
    service_list[3].make_payment(4000)

    print("\n=== After payment ===")
    for item in service_list:
        item.display_summary()

    # Encapsulation check
    print("\n=== Encapsulation check ===")
    try:
        service_list[0].paid_amount = 0
    except AttributeError as e:
        print("Cannot modify paid_amount ->", e)

    # Abstraction check
    try:
        MedicalService("Test")
    except TypeError as e:
        print("Cannot create abstract class object ->", e)