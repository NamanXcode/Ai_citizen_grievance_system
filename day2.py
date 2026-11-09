citizen = {
    "name" : "Naman Sharma",
    "age" : 20,
    "mobile" : 1234567890,
    "address" : "Delhi, india",
    "services" : ["electricity", "water", "gas"],
    "documents" : ["water_connection.pdf", "electricity_bill.pdf"]
}

complaints = [
    {
        "description" : "water supply stopped",
        "department" : "water",
        "priority" : "high",
        "status" : "pending"
    },
    {
        "description": "Street light not wokring",
        "department": "municipal",
        "priority": "medium",
        "status": "pending"
    }
]

for complaint in complaints:
    print("problem: ", complaint["description"])
    print("department: ", complaint["department"])
    print("status: ", complaint["status"])
    print()