import joblib
from day15 import connect_database

# Load the saved model and vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def predict_department(complaint):
    complaint_vector = vectorizer.transform([complaint])
    probabilities = model.predict_proba(complaint_vector)[0]

    best_index = probabilities.argmax()
    department = model.classes_[best_index]
    probability = probabilities[best_index]

    return department, probability

def submit_ai_complaint(citizen_id):
    complaint = input("Describe your complaint: ").strip()

    if not complaint:
        print("Complaint cannot be empty.")
        return

    # Ask the AI to predict the department
    department, probability = predict_department(complaint)

    print("\n===== AI DEPARTMENT SUGGESTION =====")
    print("Suggested department:", department)
    print("Estimated probability:", round(probability * 100, 2), "%")

    if probability < 0.60:
        print("Waring: This prediction may be uncertain.")

    confirmation = input(
        "Use this department? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        department = input(
            "Enter the correct department "
            "(water/electricity/gas/municipal/transport):"
        ).strip().lower()

    valid_departments = {
        "water",
        "electricity",
        "gas",
        "municipal",
        "transport"
    }

    if department not in valid_departments:
        print("Invalid department. Complaint not  submitted.")
        return

    priority = input("Enter priority (Low/Medium/High): ").strip().title()

    if  priority not in {"Low", "Medium", "High"}:
        print("Invalid priority. Complaint not submitted.")
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
        print("Status: Pending")

    except Exception:
        connection.rollback()
        print("Could not submit the complaint. Please try again.")
        raise

    finally:
        connection.close()

# Test with an existing citizen ID from your database

if __name__ == "__main__":
    citizen_id = int(input("Enter your citizen ID:"))
    submit_ai_complaint(citizen_id)

