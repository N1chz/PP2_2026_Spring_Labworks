class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return float(self.base_salary)

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100.0)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500

class Intern(Employee):
    pass

def main():
    tokens = input().split()
    role = tokens[0]

    if role == "Manager":
        _, name, base, bonus = tokens
        emp = Manager(name, int(base), int(bonus))
    elif role == "Developer":
        _, name, base, projects = tokens
        emp = Developer(name, int(base), int(projects))
    elif role == "Intern":
        _, name, base = tokens
        emp = Intern(name, int(base))
    else:
        return

    total = emp.total_salary()
    print(f"Name: {emp.name}, Total: {total:.2f}")

if __name__ == "__main__":
    main()