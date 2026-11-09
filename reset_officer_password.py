import bcrypt
from getpass import getpass
from day15 import connect_database

username = "water_admin"

password = getpass("Enter your new  officer password: ")

if len(password) < 8:
    print("Password must be at least 8 characters.")
    raise SystemExit

hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
).decode("utf-8")

conn = connect_database()

try:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE officers SET password = %s WHERE username = %s",
            (hashed_password, username)
        )

        print("Rows updated:", cur.rowcount)

    conn.commit()

finally:
    conn.close()

print("Officer password reset successfully!")