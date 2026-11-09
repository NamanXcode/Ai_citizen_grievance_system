from day15 import connect_database

def add_citizen_service(
        citizen_id,
        service_name,
        connection_number
):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    INSERT INTO citizen_services
    (citizen_id, service_name, connection_number)
    VALUES (%s, %s, %s)
    """

    values = (citizen_id, service_name, connection_number)

    cursor.execute(query, values)

    connection.commit()

    print("Service added successfully.")

    cursor.close()
    connection.close()

def view_citizen_services(citizen_id):
    connection = connect_database()
    cursor = connection.cursor()

    query = """
    SELECT
    id,
    service_name,
    connection_number
    FROM citizen_services
    WHERE citizen_id = %s
    """

    values = (citizen_id,)

    cursor.execute(query, values)

    services = cursor.fetchall()

    if services:

        print("\n=====CITIZEN SERVICES=====")

        for service in services:
            
            print("\n---------------------------")
            print("SERVICE ID:", service[0])
            print("SERVICE:", service[1])
            print("CONNECTION NUMBER:", service[2])

    else:
        print("No service found")

    cursor.close()
    connection.close()
