import bcrypt
from getpass import getpass
from day15 import connect_database

username = "water_admin"

password = getpass("Enter the password you are using in Swagger:")

conn = connect_database()

try:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT password FROM officers WHERE username  = %s",
            (username,)
        )
        result = cur.fetchone()

    if not result:
        print("Officer account not found.")
    else:
        stored_hash = result[0]

        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        try:
            valid = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash
            )
            print("Password verification:", valid)

        except (ValueError, TypeError):
            print("Stored password is not a valid bcrypt hash.")

finally:
    conn.close()
    