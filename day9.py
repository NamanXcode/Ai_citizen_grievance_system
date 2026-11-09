import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname = "citizen_portal",
    user = "postgres",
    password = "Password"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM citizens WHERE id = %s",
               (2,))

citizens = cursor.fetchone()

print("Citizens:")
cursor.close()
connection.close()