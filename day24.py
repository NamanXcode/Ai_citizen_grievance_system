import bcrypt
from day15 import connect_database

def register_officer(username, password, department):
    connection = connect_database()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    query = """
    INSERT INTO officers
    (username, password, department)
    VALUES(%s, %s, %s)
    """

    values  = (username, hashed_password.decode("utf-8"), department)

    cursor.execute(query, values)

    connection.commit()

    print("Officer registered successfully")

    cursor.close()
    connection.close()

def officer_login(username, password):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT id, username, password, department
    FROM officers
    WHERE username = %s
    """

    values = (username,)

    cursor.execute(query, values)

    officer = cursor.fetchone()

    if officer:

        stored_password = officer[2]

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):

            print("Officer login successful")
            print("Welcome", officer[1])

            officer_id = officer[0]
            department = officer[3]

            cursor.close()
            connection.close()

            return officer_id, department

    print("Invalid username or password")

    cursor.close()
    connection.close()

    return None

