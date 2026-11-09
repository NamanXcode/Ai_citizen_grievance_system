from day15 import connect_database

def view_department_statistics(department):

    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE status = 'Pending') AS pending,
    COUNT(*) FILTER (WHERE status = 'In progress') AS in_progress,
    COUNT(*) FILTER (WHERE status = 'Resolved') AS resolved
    FROM complaints
    WHERE department = %s
    """

    values = (department,)

    cursor.execute(query, values)

    statistics = cursor.fetchone()

    print("\n=====COMPLAINT STATISTICS=====")
    print("Department:", department)
    print("Total Complaints:", statistics[0])
    print("Pending:", statistics[1])
    print("In Progress:", statistics[2])
    print("Resolved:", statistics[3])

    cursor.close()
    connection.close()
