
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt, JWTError
from day15 import connect_database
import os
import hashlib


app = FastAPI(title="Officer Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["GET", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"]
)

SECRET_KEY = os.getenv("SECRET_KEY", "citizen_portal_super_secret_jwt_key_2026")

if not SECRET_KEY:
    raise RuntimeError("Set the same SECRET_KEY used by day58.py.")

print(
    "DAY57 KEY FINGERPRINT:",
    hashlib.sha256(SECRET_KEY.encode()).hexdigest()[:12]
)

ALGORITHM = "HS256"

VALID_DEPARTMENTS = {
    "water", "electricity", "gas", "municipal", "transport"
}

VALID_STATUSES = {
    "Pending", "In Progress", "Resolved"
}

bearer_scheme = HTTPBearer()


def get_current_officer(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        officer_id = payload.get("sub")
        username = payload.get("username")
        department = str(payload.get("department", "")).strip().lower()

        if (
            not officer_id
            or not username
            or department not in VALID_DEPARTMENTS
        ):
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


class StatusUpdates(BaseModel):
    status: str


@app.get("/officer/complaints")
def get_department_complaints(
    officer: dict = Depends(get_current_officer)
):
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

            print("API STATUS COUNTS:", {
                status: sum(
                    1 for complaint in complaint_list
                    if complaint["status"].lower() == status.lower()
                )
                for status in VALID_STATUSES
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


@app.patch("/officer/complaints/{complaint_id}/status")
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
            detail="Invalid status."
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
                    detail="Complaint not found in this department."
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
