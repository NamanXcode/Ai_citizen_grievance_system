"""
Automated Integration and Deployment Test Suite for AI Smart Citizen Grievance System
Tests backend endpoints, database persistence, ML classification, auth, and frontend serving.
"""

import urllib.request
import json
import time
import sys

BASE_URL = "http://localhost:8000"
OFFICER_API = "http://localhost:8001"
AUTH_API = "http://localhost:8002"
FRONTEND_URL = "http://localhost:5500"

def log(msg, success=None):
    if success is True:
        print(f" [PASS] {msg}")
    elif success is False:
        print(f" [FAIL] {msg}")
    else:
        print(f" [*] {msg}")

def request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    req_body = None
    if data is not None:
        req_body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=req_body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_bytes = resp.read()
            resp_str = resp_bytes.decode("utf-8", errors="ignore")
            content_type = resp.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return resp.status, json.loads(resp_str)
            return resp.status, resp_str
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, err_body
    except Exception as e:
        return 0, str(e)

def wait_for_backend(max_retries=20, delay=2):
    log("Waiting for backend service to become ready...")
    for i in range(max_retries):
        status, body = request(f"{BASE_URL}/health")
        if status == 200 and isinstance(body, dict) and body.get("database") == "connected":
            log("Backend & Database are UP and HEALTHY!", True)
            return True
        log(f"Attempt {i+1}/{max_retries}: status={status}, waiting {delay}s...")
        time.sleep(delay)
    return False

def test_all():
    print("=" * 60)
    print("AI CITIZEN GRIEVANCE SYSTEM - DOCKER INTEGRATION TEST SUITE")
    print("=" * 60)

    if not wait_for_backend():
        log("Backend did not become healthy in time.", False)
        return False

    # 1. Health check
    status, health = request(f"{BASE_URL}/health")
    assert status == 200 and health.get("status") == "healthy", f"Health check failed: {health}"
    log(f"Health Check: status={health['status']}, database={health['database']}, model_ready={health['model_ready']}", True)

    # 2. Citizen Complaint Preview (AI analysis)
    test_complaint = "Major water pipeline broken on main road, drinking water leaking everywhere"
    status, preview = request(
        f"{BASE_URL}/complaints",
        method="POST",
        data={"citizen_id": 1, "complaint": test_complaint, "confirm": False}
    )
    assert status == 200, f"Complaint preview failed: {preview}"
    assert preview.get("predicted_department") == "water", f"Expected water, got {preview.get('predicted_department')}"
    assert preview.get("suggested_priority") == "High", f"Expected High, got {preview.get('suggested_priority')}"
    log(f"AI Prediction Preview: Dept={preview['predicted_department']}, Priority={preview['suggested_priority']}, Conf={preview['probability_percent']}%", True)

    # 3. Citizen Complaint Submission (Confirm & Persist)
    status, submission = request(
        f"{BASE_URL}/complaints",
        method="POST",
        data={"citizen_id": 1, "complaint": test_complaint, "confirm": True}
    )
    assert status == 200 and submission.get("submitted") is True, f"Submission failed: {submission}"
    complaint_id = submission["complaint_id"]
    log(f"Complaint Persisted into DB: ID={complaint_id}, Department={submission['department']}, Status={submission['status']}", True)

    # 4. Officer Authentication (Login via Auth API port 8002 / 8000)
    status, auth = request(
        f"{AUTH_API}/officer/login",
        method="POST",
        data={"username": "water_admin", "password": "admin123"}
    )
    assert status == 200 and "access_token" in auth, f"Officer login failed: {auth}"
    token = auth["access_token"]
    officer_info = auth["officer"]
    log(f"Officer Authenticated: Username={officer_info['username']}, Dept={officer_info['department']}, JWT token acquired", True)

    # 5. Officer Dashboard Complaints Retrieval (Port 8001 / 8000)
    status, dept_data = request(
        f"{OFFICER_API}/officer/complaints",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert status == 200 and "complaints" in dept_data, f"Failed retrieving complaints: {dept_data}"
    complaint_ids = [c["id"] for c in dept_data["complaints"]]
    assert complaint_id in complaint_ids, f"Submitted complaint {complaint_id} not found in department complaints list"
    log(f"Officer Complaints Retrieved: Found {dept_data['total']} grievances in department '{dept_data['department']}'", True)

    # 6. Officer Status Update (PATCH)
    status, update = request(
        f"{OFFICER_API}/officer/complaints/{complaint_id}/status",
        method="PATCH",
        data={"status": "In Progress"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert status == 200 and update.get("status") == "In Progress", f"Status update failed: {update}"
    log(f"Complaint Status Updated to 'In Progress' for ID={complaint_id}", True)

    # 7. Frontend Serving Verification
    status, citizen_html = request(f"{FRONTEND_URL}/")
    assert status == 200 and "<!DOCTYPE html>" in citizen_html and "Citizen Grievance Portal" in citizen_html, "Citizen frontend failed to serve"
    log("Frontend Citizen Portal is serving on http://localhost:5500/", True)

    status, officer_html = request(f"{FRONTEND_URL}/officer/")
    assert status == 200 and "<!DOCTYPE html>" in officer_html and "Officer Portal" in officer_html, "Officer frontend failed to serve"
    log("Frontend Officer Dashboard is serving on http://localhost:5500/officer/", True)

    print("=" * 60)
    print(" ALL 7 DEPLOYMENT AND FUNCTIONALITY TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1)
