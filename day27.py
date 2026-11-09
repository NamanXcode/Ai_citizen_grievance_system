from day24 import officer_login
from day25 import view_department_complaints
from day26 import update_department_complaint_status
from day28 import search_department_complaints
from day29 import view_department_statistics
from day30 import view_department_complaint_details


def officer_menu(officer_id, department):

    while True:

        print("\n=====OFFICER DASHBOARD=====")
        print("Officer ID:", officer_id)
        print("Department:", department)

        print("\n1. View Department Complaints")
        print("2. Search Complaints by Status")
        print("3. Update Complaint Status")
        print("4. View Complaint Statistics")
        print("5. View Complaint Details")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            view_department_complaints(department)

        elif choice == "2":

            status = input(
                "Enter status (Pending/In Progress/Resolved):"
            )

            search_department_complaints(
                department,
                status
            )


        elif choice == "3":

            complaint_id = int(
                input("Enter complaint ID: ")
            )

            new_status = input(
                "Enter new status: "
            )

            update_department_complaint_status(
                complaint_id,
                department,
                new_status
            )
        elif choice == "4":

            view_department_statistics(department)

        elif choice == "5":

            view_department_complaint_details(department)


        elif choice == "6":

            print("Officer logged out successfully")
            break

        else:

            print("Invalid choice")


username = input("Enter officer username: ")
password = input("Enter officer password: ")

result = officer_login(
    username,
    password
)

if result:

    officer_id, department = result

    officer_menu(
        officer_id,
        department
    )

else:

    print("Officer login failed")


