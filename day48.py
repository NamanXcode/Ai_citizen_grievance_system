import joblib
from day15 import connect_database
from day46 import predict_priority

# Load saved model and vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer =  joblib.load("tfidf_vectorizer.pkl")

VALID_DEPARTMENTS = {
    "water",
    "electricity",
    "gas",
    "municipal",
    "transport"
}

def predict_department(complaint):
    complaint_vector = vectorizer.transform([complaint])
    probabilities = model.predict_proba(complaint_vector)[0]

    best_index = probabilities.argmax()
    department = model.classes_[best_index]
    probability = probabilities[best_index]

    return department, probability

def validate_complaint(complaint):
    complaint = complaint.strip()

    if len(complaint) < 10:
        return False, "Please describe your complaint in more detail."

    if len(complaint) > 500:
        return False, "Complaint must be 500 characters or fewer."

    return True, "Complaint is valid."


def submit_ai_complaint(citizen_id):
    complaint = input("Describe your complaint:").strip()

    is_valid, message = validate_complaint(complaint)

    if not is_valid:
        print(message)
        return

    department, probability = predict_department(complaint)
    priority = predict_priority(complaint)

    print("\n===== COMPLAINT REVIEW =====")
    print("Complaint:",  complaint)
    print("Suggested department:", department)
    print("Estimated probability:",  round(probability * 100, 2), "%")
    print("Suggested priority:", priority)

    if probability < 0.60:
        print("Warning: Department prediction may be  uncertain.")

    confirm = input(
        "Confirm these suggestions? (y/n):"
    ).strip().lower()

    if confirm != "y":
        print("Complaint not submitted. Please review it manually.")
        return

    if  department not  in VALID_DEPARTMENTS:
        print("Unsupported department. Complaint not submitted.")
        return

    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO complaints
            (citizen_id, description, department, priority, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """
            cursor.execute(
                query,
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
        citizen_id = int(input("Enter your citizen ID:"))
        submit_ai_complaint(citizen_id)
    except  ValueError:
        print("Please enter a valid numeric citizen ID.")


