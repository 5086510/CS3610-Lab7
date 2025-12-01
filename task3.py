from abc import ABC, abstractmethod
from typing import List


# ---------- Component interface ----------

class IOrgComponent(ABC):
    """Component interface for both Departments (composites) and Employees (leaves)."""

    @abstractmethod
    def get_total_salary(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def do_operation(self, task: str) -> str:
        raise NotImplementedError


# ---------- Leaf: Employee ----------

class EmployeeLeaf(IOrgComponent):
    """Leaf node – individual employee."""

    def __init__(self, name: str, position: str, salary: float) -> None:
        self.__name = name
        self.__position = position
        self.__salary = salary

    @property
    def name(self) -> str:
        return self.__name

    @property
    def position(self) -> str:
        return self.__position

    def get_total_salary(self) -> float:
        return self.__salary

    def do_operation(self, task: str) -> str:
        return f"Employee {self.__name} ({self.__position}) is working on: {task}"


# ---------- Composite: Department ----------

class Department(IOrgComponent):
    """Composite – can contain sub-departments and employees."""

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__children: List[IOrgComponent] = []

    @property
    def name(self) -> str:
        return self.__name

    def add(self, component: IOrgComponent) -> None:
        self.__children.append(component)

    def remove(self, component: IOrgComponent) -> None:
        if component in self.__children:
            self.__children.remove(component)

    def get_total_salary(self) -> float:
        total = 0.0
        for child in self.__children:
            total += child.get_total_salary()
        return total

    def do_operation(self, task: str) -> str:
        lines = [f"Department {self.__name} received task: {task}"]
        for child in self.__children:
            lines.append(child.do_operation(task))
        return "\n".join(lines)


# ---------- Example client code ----------

def build_company_structure() -> Department:
    # Root department (the whole company)
    company = Department("Nemanja.")

    # Sub-departments
    it_dept = Department("IT Department")
    hr_dept = Department("HR Department")

    # Employees in IT
    dev_1 = EmployeeLeaf("Hanna", "Senior Developer", 100000.0)
    dev_2 = EmployeeLeaf("Kels", "Junior Developer", 80000.0)
    admin_1 = EmployeeLeaf("Brian", "System Administrator", 70000.0)

    it_dept.add(dev_1)
    it_dept.add(dev_2)
    it_dept.add(admin_1)

    # Employees in HR
    hr_manager = EmployeeLeaf("Abishek", "HR Manager", 80000.0)
    recruiter = EmployeeLeaf("Daksh", "Recruiter", 55000.0)

    hr_dept.add(hr_manager)
    hr_dept.add(recruiter)

    # Attach departments to company
    company.add(it_dept)
    company.add(hr_dept)

    return company


if __name__ == "__main__":
    root = build_company_structure()

    print("=== Total Salary for Company ===")
    print(root.get_total_salary())

    print("\n=== Assign Task to Entire Company ===")
    task_description = "Prepare quarterly performance report"
    print(root.do_operation(task_description))
