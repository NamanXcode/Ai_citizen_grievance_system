import bcrypt

from day15 import connect_database

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
    values = (username, hashed_password.decode("utf-8"), citizen_id)

    cursor.execute(query, values)

    connection.commit()

    print("User registered successfully")

    cursor.close()
    connection.close()

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
            print("Login successful")

            citizen_id = user[3]

            print("Welcome", user[1])
            print("Citizen ID:", citizen_id)
        
    else:
        print("Invalid username or password")

    cursor.close()
    connection.close()

    return citizen_id

def change_password(username, new_password):

    connection = connect_database()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    query  = """
    UPDATE users
    SET password = %s
    WHERE username = %s
    """
    values = (hashed_password.decode("utf-8"), username)

    cursor.execute(query, values)

    users = connection.commit()

    if cursor.rowcount > 0:
        connection.commit()
        print("Password changed successfully")
    else:
        connection.rollback()
        print("No user found")

    cursor.close()
    connection.close()



