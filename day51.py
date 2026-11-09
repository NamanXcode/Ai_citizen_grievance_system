from day15 import connect_database
from day26 import update_department_complaint_status
from day50 import (
    view_department_complaints,
    search_department_complaints
)


def officer_menu(officer_id, department):
    while True:
        print("\n===== OFICER DASHBOARD =====")
        print("Officer ID:", officer_id)
        print("Department:", department)
        print("1. View Department Complaints")
        print("2. Search Complaints by Status")
        print("3. Update Complaint Status")
        print("4. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_department_complaints(department)

        elif choice == "2":
            status = input(
                "Enter status (Pending/In progress/Resolved):"
            ).strip()

            if status.lower() not in {
                "Pending", "In progress", "Resolved"
            }:
                print("Invalid status.")
                continue

            search_department_complaints(department, status)

        elif choice == "3":
            try:
                complaint_id = int(
                    input("Enter complaint ID:")
                )

                new_status = input(
                    "Enter new status (Pending/In Progress/Resolved):"
                ).strip().title()

                valid_statuses = {
                    "Pending", "In Progress", "Resolved"
                }

                if new_status not in valid_statuses:
                    print("Invalid status.")
                    continue

                update_department_complaint_status(
                    complaint_id,
                    department,
                    new_status
                )

            except ValueError:
                print("Complaint ID must be a number.")

        elif choice == "4":
            print("Officer logged out successfully.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        officer_id = int(input("Enter officer ID: "))
        department = input(
            "Enter officer department: "
        ).strip().lower()

        officer_menu(officer_id, department)

    except ValueError:
        print("Officer ID must be numeric.")