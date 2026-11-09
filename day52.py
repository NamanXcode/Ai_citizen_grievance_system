from fastapi import FastAPI

app = FastAPI(
    title="AI Citizen Grievance System",
    description = "API for citizen complaints and services",
    version = "1.0.0"
)


@app.get("/")
def home():
    return {
        "message":"Welcome to AI Citizen Grievance System",
        "status": "running"
    }

@app.get("/about")
def about():
    return {
        "project": "AI Citizen Grievance System",
        "departments": [
            "water",
            "electricity",
            "gas",
            "municipal",
            "transport"
        ]
    }