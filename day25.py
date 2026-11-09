from day15 import connect_database

def view_department_complaints(department):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT 
    id,
    citizen_id,
    description,
    department,
    priority,
    status
    FROM complaints
    WHERE department = %s
    """

    values = (department,)

    cursor.execute(query, values)

    complaints = cursor.fetchall()

    if complaints:

        print("\n=====DEPARTMENT COMPLAINTS=====")

        for complaint in complaints:
            print("Complaint Id:", complaint[0])
            print("Citizen Id:", complaint[1])
            print("Description:", complaint[2])
            print("Department:", complaint[3])
            print("Priority:", complaint[4])
            print("Status:", complaint[5])

    else:
        print("No complaints found")

    cursor.close()
    connection.close()
