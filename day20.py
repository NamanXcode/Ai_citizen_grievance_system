from day15 import connect_database

def submit_my_complaint(citizen_id, description, department, priority):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO complaints
    (citizen_id, description, department, priority, status)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """

    values = (citizen_id, description, department, priority, "Pending")

    cursor.execute(query, values)

    complaint_id = cursor.fetchone()[0]

    connection.commit()

    print("Complaint Submitted Successfully")
    print("Complaint ID:", complaint_id)

    cursor.close()
    connection.close()

def delete_my_complaint(citizen_id, complaint_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    DELETE FROM complaints
    WHERE id = %s
    AND citizen_id = %s
    """

    values = (complaint_id, citizen_id)

    cursor.execute(query, values)

    if cursor.rowcount > 0:
        connection.commit()
        print("Complaint Deleted Successfully")
    else:
        connection.rollback()
        print("No complaint found")

    cursor.close()
    connection.close()
