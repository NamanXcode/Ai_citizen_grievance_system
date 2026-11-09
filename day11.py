import psycopg

connection = psycopg.connect(
    host='localhost',
    port=5432,
    dbname = 'citizen_portal',
    user = 'postgres',
    password = 'Password'
)

cursor = connection.cursor()

cursor.execute("""
SELECT
c.name,
cp.description,
cp.department,
cp.priority,
cp.status
FROM citizens c
JOIN complaints cp
ON c.id=cp.citizen_id
""")

complaints = cursor.fetchall()

print("\n=====COMPLAINTS=====")

for complaint in complaints:
    print(complaint)


cursor.close()
connection.close()