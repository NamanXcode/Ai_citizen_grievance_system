from day15 import connect_database

def search_department_complaints(department, status):

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
    AND status = %s
    """

    values = (department, status)

    cursor.execute(query, values)

    complaints = cursor.fetchall()

    if complaints:

        print("\n=====COMPLAINTS FOUND=====")

        for complaint in complaints:

            print("---------------------")
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
