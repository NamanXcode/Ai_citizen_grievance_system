import bcrypt
from getpass import getpass
from day15 import connect_database

username = "municipal_admin"
department = "municipal"

password = getpass("Enter officer password: ")

hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

connection = connect_database()

try:
    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO officers (username, password, department)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (username, hashed_password, department)
        )

        officer_id = cursor.fetchone()[0]
        connection.commit()

        print("Municipal officer created successfully!")
        print("Officer ID:", officer_id)
        print("Username:", username)
        print("Department:", department)

except Exception as error:
    connection.rollback()
    print("Error:", error)

finally:
    connection.close()