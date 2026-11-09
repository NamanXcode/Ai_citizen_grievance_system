from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib


from day46  import predict_priority

app = FastAPI(
    title="AI Citizen Grievance System",
    description="AI-powered complaint prediction API",
    version="1.0.0"
)

# Load your saved model and TF-IDF vectorizer
model = joblib.load("complaint_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

class ComplaintRequest(BaseModel):
    complaint: str = Field(
        min_length=10,
        max_length=500
    )


@app.get("/")
def home():
    return {
        "message": "AI Citizen Grievance API is running"
    }

@app.post("/predict")
def predict_complaint(request: ComplaintRequest):
    complaint = request.complaint.strip()

    if len(complaint) < 10:
        return {
            "error": "Please describe your complaint in more detail."
        }

    # Convert complaint text into TF-IDF features
    complaint_vector = vectorizer.transform([complaint])

    # Predict department and probabilities
    probabilities = model.predict_proba(complaint_vector)[0]
    best_index = probabilities.argmax()

    department = str(model.classes_[best_index])
    probability = float(probabilities[best_index])

    # Predict priority using your existing function
    priority = predict_priority(complaint)

    return {
        "complaint": complaint,
        "predicted_department":department,
        "probability_percent": round(probability * 100, 2),
        "suggested_priority": priority,
        "warning":  (
            "Prediction may be uncertain; review manually."
            if probability < 0.60 else None
        )
    }