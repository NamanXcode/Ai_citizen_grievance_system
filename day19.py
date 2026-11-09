from day15 import connect_database

def view_my_complaints(citizen_id):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
    id,
    description,
    department,
    priority,
    status
    FROM complaints
    WHERE citizen_id = %s
    """

    values = (citizen_id,)

    cursor.execute(query, values)

    complaints = cursor.fetchall()

    if complaints:
        print("=====MY COMPLAINTS=====")

        for complaint in complaints:
            print("------------------")
            print("Complaint ID:", complaint[0])
            print("DESCRIPTION:", complaint[1])
            print("DEPARTMENT:", complaint[2])
            print("PRIORITY:", complaint[3])
            print("STATUS:", complaint[4])
    else:
        print("No complaints found")

    cursor.close()
    connection.close()

def view_my_profile(citizen_id):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT id, name, age, city
    FROM citizens
    WHERE id = %s
    """
    values = (citizen_id,)

    cursor.execute(query, values)

    citizen = cursor.fetchone()

    if citizen:
        print("=====My Profile=====")
        print("Citizen ID:", citizen[0])
        print("Name:", citizen[1])
        print("Age:", citizen[2])
        print("City:", citizen[3])
    else:
        print("Citizen not  found")

    cursor.close()
    connection.close()


def search_my_complaint(citizen_id, complaint_id):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT 
    id,
    description,
    department,
    priority,
    status
    FROM complaints
    WHERE id = %s
    AND citizen_id = %s
    """

    values = (complaint_id, citizen_id)

    cursor.execute(query, values)

    complaint = cursor.fetchone()

    if complaint:
        print("Complaint Found")
    else:
        print("Complaint Not found")

    cursor.close()
    connection.close()



