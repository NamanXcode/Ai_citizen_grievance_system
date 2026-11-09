import bcrypt
import psycopg
from day15 import connect_database
from day21 import citizen_menu

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

            citizen_id = user[3]

            print("Login successful")
            print("Welcome", user[1])

            cursor.close()
            connection.close()

            return citizen_id

        else:
            print("Invalid username or password")

    else:
        print("Invalid username or password")

    cursor.close()
    connection.close()

    return None


def login_system():

    attempts = 3

    while attempts > 0:

        print("\n=====LOGIN=====")

        username = input("Enter username: ")
        password = input("Enter password: ")

        citizen_id = login_user(username, password)

        if citizen_id:
            return citizen_id

        attempts -= 1

        print("Attempts remaining:", attempts)

    print("Too many failed attempts.")
    return None


citizen_id = login_system()

if citizen_id:
    citizen_menu(citizen_id)
else:
    print("Access denied")
    