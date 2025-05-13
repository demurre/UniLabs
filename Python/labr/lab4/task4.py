subjects = ["Mathematics", "Physics", "Biology", "History", "Literature", "CS"]

print("List of school subjects:")
for i, subject in enumerate(subjects, 1):
    print(f"{i}. {subject}")

disliked_subjects = input(
    "\nEnter the names of the items you don't like (separate them with a comma): "
)

disliked_list = [subject.strip() for subject in disliked_subjects.split(",")]

removed_subjects = []
for subject in disliked_list:
    if subject in subjects:
        subjects.remove(subject)
        removed_subjects.append(subject)

print("\nUpdated list of items:")
if subjects:
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")
else:
    print("The list is empty! You have deleted all items.")

if removed_subjects:
    print("\nThe following items were removed:")
    for subject in removed_subjects:
        print(f"- {subject}")
else:
    print("\nNo items have been deleted. You may have entered incorrect item names.")
