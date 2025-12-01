from abc import ABC, abstractmethod
from typing import Dict, Any


# ---------- Target Interface ----------

class IFinanceDataSource(ABC):

    @abstractmethod
    def get_data(self) -> Dict[str, Any]:
        raise NotImplementedError


# ---------- Adaptees (External Modules we can't modify) ----------

class TaxCalculatorCSV:

    def get_tax_data_csv(self) -> str:
        # Example CSV: "year,tax_owed\n2024,12000\n"
        return "year,tax_owed\n2024,12000\n"


class AccountingXMLModule:

    def get_accounting_xml(self) -> str:
        # Example XML (simplified, we won't do real XML parsing here)
        return "<accounting><revenue>100000</revenue><expenses>60000</expenses></accounting>"


class CreditAuthorizationJSONService:

    def get_credit_json(self) -> Dict[str, Any]:
        return {
            "credit_score": 720,
            "limit": 15000,
            "status": "approved"
        }


# ---------- Adapters (Object Adapter: composition) ----------

class TaxCSVAdapter(IFinanceDataSource):

    def __init__(self, adaptee: TaxCalculatorCSV) -> None:
        self.__adaptee = adaptee

    def get_data(self) -> Dict[str, Any]:
        raw_csv = self.__adaptee.get_tax_data_csv()
        # Very simple parsing just to show the idea:
        lines = [line for line in raw_csv.strip().split("\n") if line]
        header = lines[0].split(",")
        rows = []
        for line in lines[1:]:
            values = line.split(",")
            row = dict(zip(header, values))
            rows.append(row)

        return {
            "source": "TaxCalculatorCSV",
            "tax_records": rows
        }


class AccountingXMLAdapter(IFinanceDataSource):

    def __init__(self, adaptee: AccountingXMLModule) -> None:
        self.__adaptee = adaptee

    def get_data(self) -> Dict[str, Any]:
        raw_xml = self.__adaptee.get_accounting_xml()
        revenue = "100000"
        expenses = "60000"

        if "<revenue>" in raw_xml and "</revenue>" in raw_xml:
            revenue = raw_xml.split("<revenue>")[1].split("</revenue>")[0]
        if "<expenses>" in raw_xml and "</expenses>" in raw_xml:
            expenses = raw_xml.split("<expenses>")[1].split("</expenses>")[0]

        return {
            "source": "AccountingXMLModule",
            "revenue": float(revenue),
            "expenses": float(expenses)
        }


class CreditJSONAdapter(IFinanceDataSource):

    def __init__(self, adaptee: CreditAuthorizationJSONService) -> None:
        self.__adaptee = adaptee

    def get_data(self) -> Dict[str, Any]:
        credit_data = self.__adaptee.get_credit_json()
        # We could also rename keys or add metadata here.
        return {
            "source": "CreditAuthorizationJSONService",
            "credit": credit_data
        }


# ---------- Forecasting & Finance Modeling Module (Target Client) ----------

class ForecastingAndModelingModule:

    def process(self, data: Dict[str, Any]) -> None:
        print(f"[Forecasting] Processing data from: {data.get('source')}")
        # dumb "forecast": if revenue & expenses exist, calculate profit; if tax_records exist, sum tax.
        if "revenue" in data and "expenses" in data:
            profit = data["revenue"] - data["expenses"]
            print(f"[Forecasting] Estimated profit: {profit}")
        if "tax_records" in data:
            total_tax = sum(float(row["tax_owed"]) for row in data["tax_records"])
            print(f"[Forecasting] Total tax owed: {total_tax}")
        if "credit" in data:
            status = data["credit"].get("status")
            limit_ = data["credit"].get("limit")
            print(f"[Forecasting] Credit status={status}, limit={limit_}")


# ---------- Client / App ----------

class FinanceApp:
    def __init__(self) -> None:
        self.forecasting_module = ForecastingAndModelingModule()

    def run(self) -> None:
        # Create adaptees (external modules)
        tax_calc = TaxCalculatorCSV()
        acc_module = AccountingXMLModule()
        credit_service = CreditAuthorizationJSONService()

        # Wrap them in adapters so we always get JSON-like dicts
        tax_adapter = TaxCSVAdapter(tax_calc)
        accounting_adapter = AccountingXMLAdapter(acc_module)
        credit_adapter = CreditJSONAdapter(credit_service)

        # Use them through the common Target interface
        for adapter in (tax_adapter, accounting_adapter, credit_adapter):
            data = adapter.get_data()
            self.forecasting_module.process(data)
            print("-" * 40)


if __name__ == "__main__":
    app = FinanceApp()
    app.run()
