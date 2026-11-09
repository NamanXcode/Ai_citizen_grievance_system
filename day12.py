import psycopg

def connect_database():
    connection = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="citizen_portal",
        user="postgres",
        password="Password"
    )

    return connection
def add_citizen(name, age, city):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO citizens (name, age, city)
    VALUES (%s, %s, %s)
    """
    values = (name, age, city)
    cursor.execute(query, values)
    connection.commit()

    print("Citizen added successfully!")
    cursor.close()
    connection.close()


def view_citizens():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM citizens")
    citizens = cursor.fetchall()
    print("\n=====CITIZENS=====")

    for citizen in citizens:
        print(citizen)

    cursor.close()
    connection.close()

def add_complaint(citizen_id, description, department, priority, status):
    connection = connect_database()
    cursor = connection.cursor()

    query= """
    INSERT INTO complaints
    (citizen_id, description, department, priority, status)
    VALUES(%s, %s, %s, %s, %s)
    """

    values = (
        citizen_id,
        description,
        department,
        priority,
        status
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()
    print("complaint added successfully")


def view_complaints():
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT 
    c.name,
    cp.description,
    cp.department,
    cp.priority,
    cp.status
    FROM citizens c
    JOIN complaints cp
    ON c.id = cp.citizen_id
    """

    cursor.execute(query)

    complaints = cursor.fetchall()

    print("\n=====COMPLAINTS=====")

    for complaint in complaints:
        print(complaints)

    cursor.close()
    connection.close()


def update_complaint(complaint_id, new_status):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE complaints
    SET status = %s
    WHERE id = %s
    """
    values = (new_status, complaint_id )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    print("complaints status updated successfully")


update_complaint(1, "Resolved")