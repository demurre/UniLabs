countries = ["Ukraine", "Japan", "Canada", "USA", "Germany"]

print("List of countries:")
for i, country in enumerate(countries, 1):
    print(f"{i}. {country}")

try:
    position = int(input("\nEnter the country number (from 1 to 5): "))

    if 1 <= position <= len(countries):
        selected_country = countries[position - 1]
        print(f"You have selected a country: {selected_country}")
    else:
        print(f"Error: enter a number between 1 and {len(countries)}")
except ValueError:
    print("Error: enter an integer")
