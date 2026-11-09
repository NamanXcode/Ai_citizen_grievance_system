from day15 import connect_database

def update_department_complaint_status(
        complaint_id,
        department,
        new_status
):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE complaints
    SET status = %s
    WHERE id = %s
    AND department = %s
    """

    values = (new_status, complaint_id, department)

    cursor.execute(query, values)

    if cursor.rowcount > 0:
        connection.commit()
        print("Complaint status updated successfully")
    else:
        connection.rollback()
        print("Complaint status updates successfully")

    cursor.close()
    connection.close()
