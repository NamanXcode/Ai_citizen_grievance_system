import joblib
from day15 import connect_database
from day46 import predict_priority

model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

VALID_DEPARTMENTS = {
    "water",
    "electricity",
    "gas",
    "municipal",
    "transport"
}

def citizen_exists(citizen_id):
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM citizens WHERE id = %s",
                (citizen_id,)
            )
            return cursor.fetchone() is not None
    finally:
        connection.close()


def predict_department(complaint):
    complaint_vector = vectorizer.transform([complaint])
    probabilities = model.predict_proba(complaint_vector)[0]

    best_index = probabilities.argmax()

    return (
        model.classes_[best_index],
        probabilities[best_index]
    )

def submit_ai_complaint(citizen_id):
    # Verify citizen before proceeding
    try:
        if not citizen_exists(citizen_id):
            print("Citizen ID not found. Complaint not  submitted.")
            return
    except Exception as error:
        print("Could not verify citizen:", error)
        return

    complaint = input("Describe your complaint: ").strip()

    if  len(complaint) < 10:
        print("Please describe your complaint in at least 10 characters.")
        return

    if len(complaint) > 500:
        print("Complaint must be 500 characters or fewer.")
        return

    department, probability = predict_department(complaint)
    priority = predict_priority(complaint)

    print("\n===== COMPLAINT REVIEW =====")
    print("Complaint:", complaint)
    print("Suggested department:", department)
    print("Estimated probability:", round(probability * 100, 2), "%")
    print("Suggested priority:", priority)

    if probability < 0.60:
        print("Warning: Department prediction may be uncertain.")

    confirm = input(
        "Confirm the suggestions? (y/n):"
    ).strip().lower()

    if confirm != "y":
        print("Complaint  not  submitted.")
        return

    if department not in VALID_DEPARTMENTS:
        print("Unsupported department.Complaint not submitted.")
        return

    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO complaints
                (citizen_id, description, department, priority, status)
                VALUES  (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    citizen_id,
                    complaint,
                    department,
                    priority,
                    "Pending"
                )
            )

            complaint_id = cursor.fetchone()[0]
            connection.commit()

        print("\nComplaint submitted successfully!")
        print("Complaint ID:", complaint_id)
        print("Department:", department)
        print("Priority:", priority)
        print("Status: Pending")

    except Exception as error:
        connection.rollback()
        print("Database error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    try:
        citizen_id = int(input("Enter your citizen ID: "))

        if  citizen_id <= 0:
            print("Citizen ID must be a positive number.")
        else:
            submit_ai_complaint(citizen_id)

    except  ValueError:
        print("Please enter a valid numeric citizen ID.")