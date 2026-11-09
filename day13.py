import psycopg

def connect_database():
    connection = psycopg.connect(
        host='localhost',
        port=5432,
        user='postgres',
        dbname="citizen_portal",
        password='Password'
    )

    return connection

def add_citizen(name, age, city):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO citizens(name, age, city)
    VALUES(%s, %s, %s)
    """
    values = (name, age, city)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Citizen added successfully")


def view_citizen():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""SELECT id, name, age, city 
                   FROM citizens
                   ORDER BY id
                   """)

    citizens = cursor.fetchall()
    print("=====ALL CITIZEN DATA=====")
    for citizen in citizens:
        print(
            f"ID:{citizen[0]} |"
            f"Name:{citizen[1]} |"
            f"Age:{citizen[2]} |"
            f"City: {citizen[3]}"
        )

    cursor.close()
    connection.close()

def search_citizen(citizen_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT id, name, age, city
    FROM citizens
    WHERE id = %s
    """
    cursor.execute(query, (citizen_id,))

    citizen = cursor.fetchone()

    if citizen:
        print("\n=====CITIZEN FOUND=====")
        print(f"ID: {citizen[0]}")
        print(f"Name: {citizen[1]}")
        print(f"Age: {citizen[2]}")
        print(f"City: {citizen[3]}")
    else:
        print("Citizen not found.")

    cursor.close()
    connection.close()


def add_complaint(citizen_id, description, department, priority, status):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO complaints
    (citizen_id, description, department, priority, status)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (citizen_id, description, department, priority, status)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("Complaint Submitted successfully")

def update_citizen_city(citizen_id, new_city):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE citizens
    SET city = %s
    WHERE id = %s
    """
    values = (new_city, citizen_id)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Citizen city updated successfully.")
    else:
        print("Citizen not found.")

    cursor.close()
    connection.close()

def delete_citizen(citizen_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM citizens
    WHERE id = %s
    """

    values = (citizen_id,)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Citizen deleted successfully")
    else:
        print("Citizen not found")
    cursor.close()
    connection.close()

delete_citizen(10)
