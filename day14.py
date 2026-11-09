import psycopg

def connect_database():
    connection = connect_database(
        host = 'localhost',
        port=5432,
        user='postgres',
        dbname='citizen_portal',
        password='Password'
    )
    return connection

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

def view_complaints():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM complaints")

    complaints = cursor.fetchall()

    print("=====COMPLAINTS=====")

    for complaint in complaints:
        print(complaints)

    cursor.close()
    connection.close()

def search_complaint(complaint_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM complaints
    WHERE id = %s
    """

    values = (complaint_id,)

    cursor.execute(query, values)

    complaint = cursor.fetchone()

    if complaint:
        print("COMPLAINT FOUND")
        print(complaint)
    else:
        print("COMPLAINT NOT FOUND")

    cursor.close()
    connection.close()

def update_complaint_status(complaint_id, new_status):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE complaints
    SET status = %s
    WHERE id = %s
    """
    values = (complaint_id, new_status)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Complaint status updated successfully")
    else :
        ("Complaint not found")

    cursor.close()
    connection.close()

def delete_complaint(complaint_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM complaints
    WHERE id = %s
    """

    values = (complaint_id)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Complaint deleted successfully")
    else:
        print("Complaint not found")

    cursor.close()
    connection.close()


def search_complaints_by_status(status):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT * 
    FROM complaints
    WHERE status = %s
    """

    values = (status,)

    cursor.execute(query, values)

    complaints = cursor.fetchall()

    if cursor.rowcount > 0:
        print("Complaints Found")
        print(complaints)
    else:
        print("No complaint found")

    cursor.close()
    connection.close()


