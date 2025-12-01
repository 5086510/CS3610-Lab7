from abc import ABC, abstractmethod
from typing import Dict, Type, Optional


# ---------- Implementation interface & concrete implementors ----------

class IPaymentProcessor(ABC):
    """Implementation interface in the Bridge pattern."""

    @abstractmethod
    def process_payment(self, employee_name: str, amount: float) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class BankTransferProcessor(IPaymentProcessor):
    def process_payment(self, employee_name: str, amount: float) -> str:
        return f"[BankTransfer] Sent ${amount:.2f} to {employee_name} via bank transfer."


class ChequeProcessor(IPaymentProcessor):
    def process_payment(self, employee_name: str, amount: float) -> str:
        return f"[Cheque] Printed a cheque of ${amount:.2f} for {employee_name}."


class DigitalWalletProcessor(IPaymentProcessor):
    def process_payment(self, employee_name: str, amount: float) -> str:
        return f"[DigitalWallet] Transferred ${amount:.2f} to {employee_name}'s digital wallet."


# ---------- Factory Method for Payment Processors ----------

_processors_map: Dict[str, Type[IPaymentProcessor]] = {
    "Bank": BankTransferProcessor,
    "Cheque": ChequeProcessor,
    "Wallet": DigitalWalletProcessor
}


class PaymentProcessorFactory:
    """Factory Method creator for payment processors."""

    @staticmethod
    def create_processor(method_name: str) -> Optional[IPaymentProcessor]:
        if method_name in _processors_map:
            return _processors_map[method_name]()
        print(f"[Factory] Unknown payment method: {method_name}")
        return None


# ---------- Abstraction hierarchy (Employee types) ----------

class Employee(ABC):

    def __init__(self, name: str, payment_processor: IPaymentProcessor) -> None:
        self._name = name
        self._payment_processor = payment_processor

    @abstractmethod
    def calculate_salary(self) -> float:
        raise NotImplementedError

    def process_payment(self) -> str:
        amount = self.calculate_salary()
        return self._payment_processor.process_payment(self._name, amount)

    @property
    def name(self) -> str:
        return self._name


class HourlyEmployee(Employee):
    def __init__(self, name: str, hourly_rate: float, hours_worked: float,
                 payment_processor: IPaymentProcessor) -> None:
        super().__init__(name, payment_processor)
        self.__hourly_rate = hourly_rate
        self.__hours_worked = hours_worked

    def calculate_salary(self) -> float:
        return self.__hourly_rate * self.__hours_worked


class SalariedEmployee(Employee):
    def __init__(self, name: str, monthly_salary: float,
                 payment_processor: IPaymentProcessor) -> None:
        super().__init__(name, payment_processor)
        self.__monthly_salary = monthly_salary

    def calculate_salary(self) -> float:
        return self.__monthly_salary


class ContractorEmployee(Employee):
    def __init__(self, name: str, project_fee: float,
                 payment_processor: IPaymentProcessor) -> None:
        super().__init__(name, payment_processor)
        self.__project_fee = project_fee

    def calculate_salary(self) -> float:
        return self.__project_fee


# ---------- App that combines Bridge + Factory Method ----------

class PayrollApp:
    def __init__(self) -> None:
        self.available_payment_methods: Dict[str, IPaymentProcessor] = {}

    def configure_payment_methods(self) -> None:
        """Create required payment methods via the Factory Method."""
        for name in ("Bank", "Cheque", "Wallet"):
            processor = PaymentProcessorFactory.create_processor(name)
            if processor:
                self.available_payment_methods[name] = processor

    def run_demo(self) -> None:
        """Create employees and link them with concrete payment methods."""
        # Make sure factory ran
        self.configure_payment_methods()

        bank_proc = self.available_payment_methods["Bank"]
        cheque_proc = self.available_payment_methods["Cheque"]
        wallet_proc = self.available_payment_methods["Wallet"]

        # Bridge links (employee type -> payment method)
        salaried = SalariedEmployee("Alice (Salaried)", 5000.0, bank_proc)
        hourly = HourlyEmployee("Bob (Hourly)", hourly_rate=25.0, hours_worked=160, payment_processor=cheque_proc)
        contractor = ContractorEmployee("Charlie (Contractor)", project_fee=8000.0, payment_processor=wallet_proc)

        employees = [salaried, hourly, contractor]

        print("=== Payroll Run ===")
        for emp in employees:
            result = emp.process_payment()
            print(result)


if __name__ == "__main__":
    app = PayrollApp()
    app.run_demo()
