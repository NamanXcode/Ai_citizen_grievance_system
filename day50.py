from day15 import connect_database


def view_department_complaints(department):
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, citizen_id, description, department, priority, status
                FROM complaints
                WHERE department = %s
                ORDER BY id DESC
                """,
                (department.lower(),)
            )

            complaints = cursor.fetchall()

            if not complaints:
                print("No complaints found.")
                return

            print("\n===== DEPARTMENT COMPLAINTS =====")

            for complaint in complaints:
                print("--------------------------")
                print("Complaint ID:", complaint[0])
                print("Citizen ID:", complaint[1])
                print("Description:", complaint[2])
                print("Department:", complaint[3])
                print("Priority:", complaint[4])
                print("status:", complaint[5])

    finally:
        connection.close()


def search_department_complaints(department, status):
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                id,
                citizen_id, 
                description, 
                priority, 
                status
                FROM complaints
                WHERE department = %s
                  AND LOWER(status) = LOWER(%s)
                ORDER BY id DESC
                """,
                (department.lower(), status.strip())
            )

            complaints = cursor.fetchall()

            if not complaints:
                print("No matching complaints found.")
                return

            print("\n===== SEARCH RESULTS =====")

            for complaint in complaints:
                print("--------------------------------")
                print("Complaint ID:", complaint[0])
                print("Citizen ID:", complaint[1])
                print("Description:", complaint[2])
                print("Priority:", complaint[3])
                print("Status:", complaint[4])

    finally:
        connection.close()


def officer_menu(officer_id, department):
    while True:
        print("\n===== OFFICER DASHBOARD =====")
        print("Officer ID:", officer_id)
        print("Department:", department)
        print("1. View Department Complaints")
        print("2. Search Complaints by status")
        print("3. Logout")

        choice = input("Enter your choice:").strip()

        if choice == "1":
            view_department_complaints(department)

        elif choice == "2":
            status = input(
                "Enter status (Pending/In progress/Resolved): "
            ).strip()

            if status.lower() not in {
                "pending", "in progress", "resolved"
            }:
                print("Invalid status.")
                continue

            search_department_complaints(department, status)

        elif choice == "3":
            print("Officer logged out successfully.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        officer_id = int(input("Enter officer ID: "))
        department = input("Enter officer department: ").strip().lower()

        officer_menu(officer_id, department)

    except ValueError:
        print("Officer ID must be numeric.")