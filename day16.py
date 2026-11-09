from day15 import connect_database

def register_user(username, password, citizen_id):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO users
    (username, password, citizen_id)
    VALUES (%s, %s, %s)
    """
    values = (username, password, citizen_id)

    cursor.execute(query, values)

    connection.commit()

    print("User registered successfully")


    cursor.close()
    connection.close()

def login_user(username, password):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM users
    WHERE username = %s
    AND password = %s
    """

    values = (username, password)

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:
        print("Login successful")
        print("WELCOME", username)
    else:
        print("Invalid username or password")

    cursor.close()
    connection.close()

def check_username(username):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT * 
    FROM users
    WHERE username = %s
    """

    values = (username,)

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:
        print("Username already exists")
    else:
        print("Username available")

    cursor.close()
    connection.close()
