party_guests = []

print("Enter the names of three people you want to invite to the party:")

for i in range(3):
    name = input(f"Enter the person's name {i+1}: ")
    party_guests.append(name)

print("\nCurrent list of invitees:")
for i, name in enumerate(party_guests, 1):
    print(f"{i}. {name}")

add_more = input("\nWould you like to add another name? (yes/no): ").lower()

while add_more == "yes":
    name = input("Enter a name: ")
    party_guests.append(name)

    print("\nUpdated guest list:")
    for i, name in enumerate(party_guests, 1):
        print(f"{i}. {name}")

    add_more = input("\nWould you like to add another name? (yes/no): ").lower()

print(f"\nInvited to the party are {len(party_guests)} people.")
print("The list of all invitees:")
for i, name in enumerate(party_guests, 1):
    print(f"{i}. {name}")
