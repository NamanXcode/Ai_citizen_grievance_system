from day15 import connect_database

def login_user(username,  password):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT id, username, citizen_id
    FROM users
    WHERE username = %s
    AND password = %s
    """

    values = (username, password)

    cursor.execute(query, values)

    user = cursor.fetchone()

    if user:
        print("Login successful")
        print("Welcome", user[1])
        print("Citizen ID:", user[2])
    else:
        print("Invalid username or password")

    cursor.close()
    connection.close()

def get_citizen_by_user(username):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT 
    c.id,
    c.name,
    c.age,
    c.city
    FROM users u
    JOIN citizens c
    ON u.citizen_id = c.id
    WHERE u.username = %s
    """

    values = (username,)

    cursor.execute(query, values)

    citizen = cursor.fetchone()

    if citizen:
        print("User exist")
        print("Citizen ID :", citizen[0])
        print("Name :", citizen[1])
        print("Age :", citizen[2])
        print("City :", citizen[3])
    else:
        ("User doesn't exist")

    cursor.close()
    connection.close()


get_citizen_by_user("naman123")


