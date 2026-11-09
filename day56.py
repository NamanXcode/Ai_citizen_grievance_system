from day15 import connect_database


def view_department_complaints(department):
    conn = connect_database()

    if not conn:
        print("Database connection failed.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, citizen_id, description, department, priority, status
                FROM complaints
                WHERE LOWER(department) = LOWER(%s)
                ORDER BY id DESC
                """,
                (department,)
            )

            complaints = cur.fetchall()


            if not complaints:
                print("No complaints found for this department.")
                return

            print(f"\n--- {department.upper()} COMPLAINTS ---")


            for complaint in complaints:
                print("-" * 50)
                print("Complaints ID:", complaint[0])
                print("Citizen ID:", complaint[1])
                print("Description:", complaint[2])
                print("Department:", complaint[3])
                print("Priority:", complaint[4])
                print("Status:", complaint[5])

    except Exception as error:
        print("Error:", error)

    finally:
        conn.close()


if __name__ == "__main__":
    department = input(
        "Enter department (water/electricity/gas/municipal/transport): "
    ).strip().lower()

    view_department_complaints(department)



def update_complaint_status(complaint_id, department, new_status):
    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if new_status not in allowed_statuses:
        print("Invalid status.")
        return

    conn = connect_database()


    if not conn:
        print("Database connection failed.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE complaints
                SET status = %s
                WHERE id = %s
                AND LOWER(department) = LOWER(%s)
                RETURNING id
                """,
                (new_status, complaint_id, department)
            )

            updated = cur.fetchone()

            if updated:
                conn.commit()
                print("Complaint status updated successfully.")
            else:
                conn.rollback()
                print("Complaint not found in this department.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()



complaint_id = int(input("Enter complaint ID to update: "))
new_status = input(
    "Enter new status (Pending/In Progress/Resolved): "
).strip().title()

update_complaint_status(complaint_id, department, new_status)
