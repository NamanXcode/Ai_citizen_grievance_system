import joblib

# Load the saved model and vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

def predict_complaint(complaint):

    if not complaint.strip():
        raise ValueError("Complaint cannot be empty.")

    # Convert complaint into TF-IDF features
    complaint_vector = vectorizer.transform([complaint])

    # Get prediction probabilities
    probabilities = model.predict_proba(complaint_vector)[0]

    best_index = probabilities.argmax()

    best_department = model.classes_[best_index]
    best_probability = probabilities[best_index]

    print("\n===== AI COMPLAINT ANALYSIS =====")
    print("Complaint:", complaint)
    print("Suggested department:", best_department)

    print(
        "Highest estimated probability:",
        round(best_probability * 100, 2),
        "%"
    )

    if best_probability < 0.60:
        print("Warning: Prediction may be uncertain.")
        print("Please confirm the department manually.")
    else:
        print("Prediction confidence is sufficient.")

    return best_department


#Test the function
complaint = input("Describe your complaint: ")
predict_complaint(complaint)

