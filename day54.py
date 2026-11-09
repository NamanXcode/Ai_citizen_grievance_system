from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
from fastapi.middleware.cors import CORSMiddleware

from day15 import connect_database
from day46 import predict_priority

app = FastAPI(title="AI Citizen Grievance System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "complaint_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"))

VALID_DEPARTMENTS = {
    "water", "electricity", "gas", "municipal", "transport"
}

# If the model is less sure than this, ask the citizen to describe the
# problem in more detail instead of guessing a department.
# Tune this using real predictions (set to 0.0 to disable the check).
CONFIDENCE_THRESHOLD = 0.50

# Profile columns that must never be sent back to the browser.
SENSITIVE_FIELD_HINTS = ("password", "hash", "token", "secret")


class ComplaintRequest(BaseModel):
    citizen_id: int = Field(gt=0)
    complaint: str = Field(min_length=10, max_length=500)
    confirm: bool


def predict_department(complaint):

    complaint = complaint.lower()

    # Rule-based department detection
    if any(word in complaint for word in [
        "gas leak", "gas leaking", "gas pipeline",
        "lpg", "gas cylinder"
    ]):
        return "gas", 1.0, True

    elif any(word in complaint for word in [
        "street light", "streetlight", "street lamp",
        "pothole", "road damage", "garbage",
        "municipal", "drainage"
    ]):
        return "municipal", 1.0, True

    elif any(word in complaint for word in [
        "water supply", "water leakage", "water",
        "tap water"
    ]):
        return "water", 1.0, True

    elif any(word in complaint for word in [
        "electricity", "power outage", "electric wire",
        "electric shock", "transformer"
    ]):
        return "electricity", 1.0, True

    elif any(word in complaint for word in [
        "bus service", "public transport",
        "metro service", "train service"
    ]):
        return "transport", 1.0, True

    # ML prediction for unmatched complaints
    complaint_vector = vectorizer.transform([complaint])

    probabilities = model.predict_proba(complaint_vector)[0]

    best_index = probabilities.argmax()

    department = str(model.classes_[best_index])
    probability = float(probabilities[best_index])

    return department, probability, False



def get_citizen_profile(cursor, citizen_id):
    """Return the citizen's stored profile as a dict, or None if not found.

    Reads whatever columns exist in the citizens table, so it works with
    your current schema without hard-coding column names.
    """
    cursor.execute("SELECT * FROM citizens WHERE id = %s", (citizen_id,))
    row = cursor.fetchone()

    if row is None:
        return None

    column_names = [column[0] for column in cursor.description]
    profile = {}

    for name, value in zip(column_names, row):
        lowered = name.lower()

        if lowered == "id":
            continue

        if any(hint in lowered for hint in SENSITIVE_FIELD_HINTS):
            continue

        if isinstance(value, (bytes, bytearray, memoryview)):
            value = "stored file" if value else None

        profile[name] = value

    return profile


def find_missing_fields(profile):
    return [
        name for name, value in profile.items()
        if value is None or str(value).strip() == ""
    ]


@app.post("/complaints")
def submit_complaint(request: ComplaintRequest):
    complaint = request.complaint.strip()

    if len(complaint) < 10:
        raise HTTPException(
            status_code=400,
            detail="Please describe your complaint in more detail."
        )

    department, probability, rule_matched = predict_department(complaint)
    priority = predict_priority(complaint)

    if department not in VALID_DEPARTMENTS:
        raise HTTPException(
            status_code=422,
            detail="The predicted department is unsupported."
        )

    low_confidence = (
        probability < CONFIDENCE_THRESHOLD
        and not rule_matched
    )

    connection = connect_database()

    if not connection:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed."
        )

    try:
        with connection.cursor() as cursor:
            # Check that the citizen exists and load their stored details
            profile = get_citizen_profile(cursor, request.citizen_id)

            if profile is None:
                raise HTTPException(
                    status_code=404,
                    detail="Citizen ID not found."
                )

            missing_information = find_missing_fields(profile)

            # ---------- PREVIEW MODE ----------
            if not request.confirm:
                if low_confidence:
                    message = (
                        "The system is not confident about the department. "
                        "Please describe the problem in more detail."
                    )
                else:
                    message = "Complaint was not submitted. Please review and confirm."

                return {
                    "submitted": False,
                    "message": message,
                    "predicted_department": department,
                    "probability_percent": round(probability * 100, 2),
                    "suggested_priority": priority,
                    "low_confidence": low_confidence,
                    "citizen_profile": profile,
                    "missing_information": missing_information
                }

            # ---------- CONFIRM MODE ----------
            if low_confidence:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "The system could not identify the department with "
                        "enough confidence. Please describe the problem in "
                        "more detail."
                    )
                )

            cursor.execute(
                """
                INSERT INTO complaints
                (citizen_id, description, department, priority, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    request.citizen_id,
                    complaint,
                    department,
                    priority,
                    "Pending"
                )
            )

            complaint_id = cursor.fetchone()[0]
            connection.commit()

            return {
                "submitted": True,
                "complaint_id": complaint_id,
                "department": department,
                "priority": priority,
                "status": "Pending",
                "probability_percent": round(probability * 100, 2),
                "missing_information": missing_information
            }

    except HTTPException:
        connection.rollback()
        raise

    except Exception as error:
        connection.rollback()
        print("DATABASE ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Unable to save complaint. Please try again."
        )

    finally:
        connection.close()