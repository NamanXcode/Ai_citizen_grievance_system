import os
import psycopg


def connect_database():
    db_password = os.getenv("DB_PASSWORD", "Password")

    connection = psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER", "postgres"),
        dbname=os.getenv("DB_NAME", "citizen_portal"),
        password=db_password
    )

    return connection


def view_complaints_with_citizen():
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            query = """
            SELECT
                c.name,
                c.city,
                cp.description,
                cp.department,
                cp.priority,
                cp.status
            FROM citizens c
            JOIN complaints cp
            ON c.id = cp.citizen_id
            """

            cursor.execute(query)

            for complaint in cursor.fetchall():
                print(complaint)

    finally:
        connection.close()
