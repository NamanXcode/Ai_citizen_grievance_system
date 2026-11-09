import psycopg

def connect_database():
    connection = psycopg.connect(
        host = 'localhost',
        port=5432,
        user='postgres',
        dbname='citizen_portal',
        password='@Naman2005'
    )
    return connection

def view_complaints_with_citizen():
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
        cp.id,
        c.name,
        c.city,
        cp.description,
        cp.department,
        cp.priority,
        cp.status
    FROM citizens c
    JOIN complaints cp
    ON c.id=cp.citizen_id
    """

    cursor.execute(query)

    complaints =  cursor.fetchall()

    print("=====ALL COMPLAINTS=====")

    for complaint in complaints:
        print("--------------------")
        print("Complaint ID:", complaint[0])
        print("Citizen Name:", complaint[1])
        print("City:", complaint[2])
        print("Description:", complaint[3])
        print("Department:", complaint[4])
        print("Priority:", complaint[5])
        print("Status:", complaint[6])

    cursor.close()
    connection.close()

def update_complaint_department(complaint_id, new_department):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE complaints
    SET department = %s
    WHERE id = %s
    """
    values = (new_department, complaint_id)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Department updated successfully")
    else:
        print("Complaint not found")

    cursor.close()
    connection.close()


def update_complaint_priority(complaint_id, new_priority):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    UPDATE complaints
    SET priority = %s
    WHERE id = %s
    """

    values = (new_priority, complaint_id)

    cursor.execute(query, values)

    connection.commit()

    if cursor.rowcount > 0:
        print("Priority updated successfully")
    else:
        print("Complaint not found")

    cursor.close()
    connection.close()

def search_complaints_by_department(department) :

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT *
    FROM complaints
    WHERE department = %s
    """

    values = (department,)

    cursor.execute(query, values)

    complaints = cursor.fetchall()
    if complaints :
        print("=====COMPLAINTS FOUND=====")
        for complaint in complaints:
            print("Complaint ID:", complaint[0])
            print("Citizen ID:", complaint[1])
            print("Description:", complaint[2])
            print("Department:", complaint[3])
            print("Priority:", complaint[4])
            print("Status:", complaint[5])

        else:
            print("No complaints found")

    cursor.close()
    connection.close()




    