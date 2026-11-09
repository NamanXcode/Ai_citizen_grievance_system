import joblib
from day15 import connect_database
from day46 import predict_priority

# Load your saved AI model and TF-IDF vectorizer

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

    # Predict department
    department, probability = predict_department(complaint)

    # Predicting priority using Day 46
    priority = predict_priority(complaint)

    print("\n===== AI COMPLAINT ANALYSIS =====")
    print("Complaint:", complaint)
    print("Suggested department:", department)
    print("Department probability:", round(probability * 100, 2), "%")
    print("Suggested priority:", priority)

    if probability < 0.60:
        print("Waring : Department prediction may be uncertain.")

    confirm = input(
        "Do you confirm the suggested department and priority? (y/n):"
    ).strip().lower()

    if confirm != "y":
        print("Complaint not submitted.")
        print("Please run again after reviewing the suggestions.")
        return

    valid_departments = {
        "water", "electricity", "gas", "municipal", "transport"
    }

    if department not in valid_departments:
        print("Invalid department. Complaint not submitted.")
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
                (citizen_id, complaint, department, priority, "Pending")
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
        print("Could not  submit complaint:", error)

    finally:
        connection.close()

if __name__ == "__main__":
    try:
        citizen_id = int(input("Enter your citizen ID:"))
        submit_ai_complaint(citizen_id)
    except ValueError:
        print("Citizen ID must be a number.") 
