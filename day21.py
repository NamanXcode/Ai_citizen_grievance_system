from day15 import connect_database
import bcrypt
from day19 import view_my_profile, view_my_complaints, search_my_complaint
from day20 import submit_my_complaint, delete_my_complaint
from day31 import add_citizen_service, view_citizen_services

def citizen_menu(citizen_id):

    while True:

        print("\n====CITIZEN PORTAL=====")
        print("1. View Profile")
        print("2. VIEW MY SERVICES")
        print("3. SUBMIT MY COMPLAINT")
        print("4. DELETE MY COMPLAINT")
        print("5. SEARCH MY COMPLAINT")
        print("6. VIEW MY COMPLAINTS")
        print("7. LOGOUT")

        choice = input("Enter your choice:")

        if choice == "1":
            view_my_profile(citizen_id)

        elif choice == "2":
            view_citizen_services(citizen_id)

        elif choice == "3":
            description = input("Enter complaint: ")
            department = input("Enter department: ")
            priority = input("Enter priority: ")


            submit_my_complaint(
                citizen_id,
                description,
                department,
                priority
            )

        elif choice == "4":
            complaint_id = int(
                input("Enter complaint ID to delete: ")
            )

            delete_my_complaint(
                citizen_id,
                complaint_id
            )

        elif choice == "5":
            complaint_id = int(
                input("Enter complaint ID to search: ")
            )
        
            search_my_complaint(
                citizen_id,
                complaint_id
                )

        elif choice == "6":
                    view_my_complaints(citizen_id)
        

        elif choice == "7":
            print("Logged out successfully")
            break

        else:
            print("Invalid choice")

def login_user(username, password):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT id, username, password, citizen_id
    FROM users
    WHERE username = %s
    """

    values = (username,)

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:

        stored_password = user[2]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):
            print("login successful")

            citizen_id = user[3]

            cursor.close()
            connection.close()

            return citizen_id

    print("Invalid username or password")

    cursor.close()
    connection.close()


def register_user(username, password, citizen_id):

    connection = connect_database()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    query = """
    INSERT INTO users
    (username, password, citizen_id)
    VALUES (%s, %s, %s)
    """

    values = (
        username,
        hashed_password.decode("utf-8"),
        citizen_id
    )

    cursor.execute(query, values)

    connection.commit()

    print("User registered successfully")

    cursor.close()
    connection.close()

