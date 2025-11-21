def get_initial_conditions():
    d1 = float(input("Enter the length of the first diagonal of the rhombus (d1): "))
    d2 = float(input("Enter the length of the second diagonal of the rhombus (d2): "))
    return d1, d2

def calculate_rhombus_area():
    d1, d2 = get_initial_conditions()
    area = 0.5 * d1 * d2
    print("Rhombus area:", area)

calculate_rhombus_area()
