from day15 import connect_database

def view_department_complaint_details(department):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
    cp.id,
    c.id,
    c.name,
    c.city,
    cp.description,
    cp.department,
    cp.priority,
    cp.status
    FROM complaints cp
    JOIN citizens c
    ON cp.citizen_id = c.id
    WHERE cp.department = %s
    """

    values =  (department,)

    cursor.execute(query, values)

    complaints = cursor.fetchall()

    if complaints:

        print("\n=====COMPLAINT DETAILS=====")

        for complaint in complaints:

            print("Complaint ID:", complaint[0])
            print("Citizen ID:", complaint[1])
            print("Citizen Name:", complaint[2])
            print("City:", complaint[3])
            print("Description:", complaint[4])
            print("Department:", complaint[5])
            print("Priority:", complaint[6])
            print("Status:", complaint[7])

    else:

        print("No complaints found")

    cursor.close()
    connection.close()
