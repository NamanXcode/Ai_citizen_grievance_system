from datetime import datetime, timedelta, timezone
import os
import hashlib
import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from day15 import connect_database

app = FastAPI(title="Officer Authentication API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"]
)

SECRET_KEY = os.getenv("SECRET_KEY", "citizen_portal_super_secret_jwt_key_2026")
if not SECRET_KEY:
    raise RuntimeError("Set the SECRET_KEY environment variable.")

import hashlib

print( 
    "DAY58 KEY FINGERPRINT:",
    hashlib.sha256(SECRET_KEY.encode()).hexdigest()[:12]
)

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/officer/login")

class OfficerLogin(BaseModel):
    username: str
    password: str

@app.post("/officer/login")
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

        if department not in {
            "water", "electricity", "gas", "municipal", "transport"
        }:
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
                "username":  stored_username,
                "department": department
            }
        }

    finally:
        conn.close()
