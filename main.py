import os
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import joblib
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from jose import jwt, JWTError
from pydantic import BaseModel, Field

from day15 import connect_database
from day46 import predict_priority

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------- CONFIGURATION & CONSTANTS -----------------
SECRET_KEY = os.getenv("SECRET_KEY", "citizen_portal_super_secret_jwt_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 60

VALID_DEPARTMENTS = {"water", "electricity", "gas", "municipal", "transport"}
VALID_STATUSES = {"Pending", "In Progress", "Resolved"}
CONFIDENCE_THRESHOLD = 0.50
SENSITIVE_FIELD_HINTS = ("password", "hash", "token", "secret")

# Load ML model & vectorizer
model_path = os.path.join(BASE_DIR, "complaint_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# ----------------- FASTAPI APP SETUP -----------------
app = FastAPI(
    title="AI Smart Citizen Grievance System",
    description="Unified API for Citizen Complaints and Officer Grievance Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_sql_path = os.path.join(BASE_DIR, "init.sql")
    if os.path.exists(init_sql_path):
        try:
            conn = connect_database()
            with open(init_sql_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            with conn.cursor() as cur:
                cur.execute(sql_content)
            conn.commit()
            conn.close()
            print("Auto-initialization: Database verified and ready.")
        except Exception as exc:
            print("Auto-initialization notice:", exc)

bearer_scheme = HTTPBearer(auto_error=False)


# ----------------- PYDANTIC SCHEMAS -----------------
class ComplaintRequest(BaseModel):
    citizen_id: int = Field(gt=0)
    complaint: str = Field(min_length=10, max_length=500)
    confirm: bool


class OfficerLogin(BaseModel):
    username: str
    password: str


class StatusUpdates(BaseModel):
    status: str


# ----------------- HELPER FUNCTIONS -----------------
def predict_department(complaint: str):
    complaint_lower = complaint.lower()

    if any(word in complaint_lower for word in [
        "gas leak", "gas leaking", "gas pipeline", "lpg", "gas cylinder"
    ]):
        return "gas", 1.0, True

    elif any(word in complaint_lower for word in [
        "street light", "streetlight", "street lamp", "pothole",
        "road damage", "garbage", "municipal", "drainage"
    ]):
        return "municipal", 1.0, True

    elif any(word in complaint_lower for word in [
        "water supply", "water leakage", "water", "tap water"
    ]):
        return "water", 1.0, True

    elif any(word in complaint_lower for word in [
        "electricity", "power outage", "electric wire",
        "electric shock", "transformer"
    ]):
        return "electricity", 1.0, True

    elif any(word in complaint_lower for word in [
        "bus service", "public transport", "metro service", "train service"
    ]):
        return "transport", 1.0, True

    complaint_vector = vectorizer.transform([complaint_lower])
    probabilities = model.predict_proba(complaint_vector)[0]
    best_index = probabilities.argmax()

    department = str(model.classes_[best_index])
    probability = float(probabilities[best_index])

    return department, probability, False


def get_citizen_profile(cursor, citizen_id: int):
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


def find_missing_fields(profile: dict):
    return [
        name for name, value in profile.items()
        if value is None or str(value).strip() == ""
    ]


def get_current_officer(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)
):
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authorization token required."
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        officer_id = payload.get("sub")
        username = payload.get("username")
        department = str(payload.get("department", "")).strip().lower()

        if not officer_id or not username or department not in VALID_DEPARTMENTS:
            raise HTTPException(
                status_code=401,
                detail="Invalid officer token."
            )

        return {
            "id": officer_id,
            "username": username,
            "department": department
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )


# ----------------- SYSTEM & HEALTH ENDPOINTS -----------------
@app.get("/health", tags=["System"])
def health_check():
    db_ok = False
    try:
        conn = connect_database()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            db_ok = cur.fetchone()[0] == 1
        conn.close()
    except Exception as exc:
        db_error = str(exc)
        return {
            "status": "degraded",
            "database": "unreachable",
            "error": db_error,
            "model_ready": True
        }

    return {
        "status": "healthy",
        "database": "connected" if db_ok else "error",
        "model_ready": True,
        "departments": list(VALID_DEPARTMENTS)
    }


# ----------------- CITIZEN ENDPOINTS -----------------
@app.post("/complaints", tags=["Citizens"])
def submit_complaint(request: ComplaintRequest):
    complaint = request.complaint.strip()

    if len(complaint) < 10:
        raise HTTPException(
            status_code=400,
            detail="Please describe your complaint in more detail (min 10 characters)."
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
            profile = get_citizen_profile(cursor, request.citizen_id)
            if profile is None:
                raise HTTPException(
                    status_code=404,
                    detail="Citizen ID not found. Please register or enter a valid ID."
                )

            missing_information = find_missing_fields(profile)

            # Preview Mode
            if not request.confirm:
                message = (
                    "The system is not confident about the department. Please describe in more detail."
                    if low_confidence
                    else "Complaint analyzed. Please review and confirm to submit."
                )
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

            # Confirm Mode
            if low_confidence:
                raise HTTPException(
                    status_code=422,
                    detail="The system could not identify the department with enough confidence."
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


# ----------------- OFFICER AUTH ENDPOINTS -----------------
@app.post("/officer/login", tags=["Officers"])
def officer_login(request: OfficerLogin):
    username = request.username.strip()

    if not username or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Username and password are required."
        )

    conn = connect_database()
    if not conn:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed."
        )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, username, password, department
                FROM officers
                WHERE username = %s
                """,
                (username,)
            )
            officer = cur.fetchone()

        if officer is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        officer_id, stored_username, stored_hash, department = officer

        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        try:
            password_valid = bcrypt.checkpw(
                request.password.encode("utf-8"),
                stored_hash
            )
        except (ValueError, TypeError):
            password_valid = False

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        department = str(department).strip().lower()
        if department not in VALID_DEPARTMENTS:
            raise HTTPException(
                status_code=403,
                detail="Officer department is not configured correctly."
            )

        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_MINUTES
        )

        token = jwt.encode(
            {
                "sub": str(officer_id),
                "username": stored_username,
                "department": department,
                "exp": expires_at
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "message": "Officer login successful.",
            "access_token": token,
            "token_type": "bearer",
            "expires_in_minutes": ACCESS_TOKEN_MINUTES,
            "officer": {
                "id": officer_id,
                "username": stored_username,
                "department": department
            }
        }
    finally:
        conn.close()


# ----------------- OFFICER DASHBOARD ENDPOINTS -----------------
@app.get("/officer/complaints", tags=["Officers"])
def get_department_complaints(officer: dict = Depends(get_current_officer)):
    department = officer["department"]

    conn = connect_database()
    if not conn:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed."
        )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, citizen_id, description,
                       department, priority, status
                FROM complaints
                WHERE LOWER(TRIM(department)) = %s
                ORDER BY id DESC
                """,
                (department,)
            )
            rows = cur.fetchall()

            complaint_list = []
            for row in rows:
                complaint_list.append({
                    "id": row[0],
                    "citizen_id": row[1],
                    "description": row[2],
                    "department": str(row[3]).strip().lower(),
                    "priority": str(row[4]).strip(),
                    "status": str(row[5]).strip()
                })

            return {
                "department": department,
                "total": len(complaint_list),
                "complaints": complaint_list
            }
    except Exception as error:
        print("DATABASE ERROR:", repr(error))
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve complaints."
        )
    finally:
        conn.close()


@app.patch("/officer/complaints/{complaint_id}/status", tags=["Officers"])
def update_status(
    complaint_id: int,
    request: StatusUpdates,
    officer: dict = Depends(get_current_officer)
):
    department = officer["department"]
    status = request.status.strip()

    if status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"
        )

    conn = connect_database()
    if not conn:
        raise HTTPException(
            status_code=500,
            detail="Database connection failed."
        )

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE complaints
                SET status = %s
                WHERE id = %s
                AND LOWER(TRIM(department)) = %s
                RETURNING id, status
                """,
                (status, complaint_id, department)
            )
            updated = cur.fetchone()

            if updated is None:
                conn.rollback()
                raise HTTPException(
                    status_code=404,
                    detail="Complaint not found in your department."
                )

            conn.commit()
            return {
                "message": "Complaint status updated successfully.",
                "complaint_id": updated[0],
                "status": updated[1]
            }
    except HTTPException:
        raise
    except Exception as error:
        conn.rollback()
        print("DATABASE ERROR:", repr(error))
        raise HTTPException(
            status_code=500,
            detail="Unable to update complaint status."
        )
    finally:
        conn.close()


# ----------------- STATIC FILES & FRONTEND MOUNTING -----------------
frontend_dir = os.path.join(BASE_DIR, "frontend")
officer_frontend_dir = os.path.join(BASE_DIR, "officer frontend")

if os.path.exists(frontend_dir):
    app.mount("/citizen", StaticFiles(directory=frontend_dir, html=True), name="citizen")

if os.path.exists(officer_frontend_dir):
    app.mount("/officer", StaticFiles(directory=officer_frontend_dir, html=True), name="officer")


@app.get("/", response_class=HTMLResponse, tags=["Navigation"])
def home_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Citizen Grievance System</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: #fff;
                min-height: 100vh;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .card {
                background: rgba(255, 255, 255, 0.96);
                color: #222;
                border-radius: 12px;
                padding: 36px 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
                text-align: center;
            }
            h1 { margin-top: 0; color: #1e3c72; }
            p { color: #555; line-height: 1.6; }
            .links { display: grid; gap: 14px; margin-top: 26px; }
            .btn {
                display: block;
                padding: 14px 20px;
                background: #1e3c72;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: background 0.2s, transform 0.1s;
            }
            .btn:hover { background: #2a5298; transform: translateY(-2px); }
            .btn-secondary { background: #00897b; }
            .btn-secondary:hover { background: #00796b; }
            .btn-tertiary { background: #546e7a; }
            .btn-tertiary:hover { background: #455a64; }
            .badge {
                display: inline-block;
                background: #e8f5e9;
                color: #2e7d32;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 600;
                margin-bottom: 12px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">&#9679; Docker System Online</span>
            <h1>AI Smart Citizen Grievance System</h1>
            <p>Welcome! The automated AI grievance classification system and officer management dashboard are actively running in Docker.</p>
            <div class="links">
                <a href="/citizen/" class="btn">Citizen Grievance Portal</a>
                <a href="/officer/officer.html" class="btn btn-secondary">Officer Dashboard Portal</a>
                <a href="/docs" class="btn btn-tertiary">Interactive API Documentation (Swagger)</a>
                <a href="/health" class="btn btn-tertiary">Health Check & Status Endpoint</a>
            </div>
        </div>
    </body>
    </html>
    """
