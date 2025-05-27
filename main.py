from transaction import *
from category import *
from analysis import *
from gui.main_gui import run_gui


if __name__ == "__main__":
    run_gui()

#data = load_data()

#income = total_income(data)
#expenses = total_expenses(data)
#balance = total_balace(data)

#income_by_cat = sum_income_by_categories(data)
#expenses_by_cat = sum_expenses_by_categories(data)
#total, optional = count_optional_expenses(data)
#income, expenses, balance = calculate_balance(data)
#result = sum_by_categories(data)

#print()
#print(f"Доходы: {income}")
#print(f"Расходы: {expenses}")
#print(f"Разница: {balance}")

#print("\nСумма доходов по категориям:")
#for category, amount in income_by_cat.items():
#    print(f"{category}: {amount}")

#print("\nСумма расходов по категориям:")
#for category, amount in expenses_by_cat.items():
#    print(f"{category}: {amount}")

#print(f"\nВсего расходов: {total}| Из них необязательных расходов: {optional}")
