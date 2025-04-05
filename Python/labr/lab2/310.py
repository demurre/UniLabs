def calculate_deposit(initial_amount, years, interest_rate=0.1):
    amount = initial_amount

    print(f"Initial amount: {amount:.2f} $")

    for year in range(1, years + 1):
        amount *= 1 + interest_rate
        print(f"After {year} year: {amount:.2f} $")

    return amount


initial_amount = 31700
years = 7
interest_rate = 0.1

final_amount = calculate_deposit(initial_amount, years, interest_rate)
print(f"\nTotal amount after {years} years: {final_amount:.2f} $")
print(f"Net profit: {final_amount - initial_amount:.2f} $")
