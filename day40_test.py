import joblib

# Load the saved model and vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Get a new complaint
complaint = input("Describe your complaint: ")

# Convert the complaint into numerical features
complaint_vector = vectorizer.transform([complaint])

#predict the department
department = model.predict(complaint_vector)[0]

# Get probablities for every department
probabilities = model.predict_proba(complaint_vector)[0]

# Find the highest probability
best_index = probabilities.argmax()
best_department = model.classes_[best_index]
best_probability = probabilities[best_index]


print("\n===== AI prediction =====")
print("Complaint:", complaint)
print("Predicted department:", department)
print("Highest estimated probability:",
      round(best_probability * 100, 2), "%")

if best_probability < 0.60:
    print("Warning: Low prediction score.")
    print("Please confirm the department manually.")

else:
    print("Suggested department: ", best_department)
     

print("\n===== DEPARTMENT PROBABILITIES =====")
for name, probability in zip(model.classes_, probabilities):
    print(f"{name}: {probability * 100:.2f}%")

