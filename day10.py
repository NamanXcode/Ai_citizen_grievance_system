import psycopg

connection = psycopg.connect(
    host='localhost',
    port=5432,
    dbname='citizen_portal',
    user='postgres',
    password='Password'
)

cursor = connection.cursor()

citizens = [
    ("Deepanshu", 25, "Peshawar"),
    ("Himani", 23, "Himachal"),
    ("piyush", 23, "Bulandshahar"),
    ("Chirag", 15, "Bangalore")
]

query = """
INSERT INTO citizens (name, age, city)
VALUES (%s, %s, %s)
"""
cursor.executemany(query, citizens)

connection.commit()

citizens = cursor.fetchall()

print("=====Citizens=====")
for citizen in citizens:
    print(citizen)
cursor.close()
connection.close()