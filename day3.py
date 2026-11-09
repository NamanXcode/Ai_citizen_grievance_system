departments = {"water department", "municipal department", "electricity department", "gas department", "transport department" }
for department in departments:
    print("Department: ", department)

citizen = {
    "name" : "naman sharma",
    "age" : 20,
    "mobile" : 1234567890,
    "city" : "delhi",
    "services" : ["electricity", "gas"]
}
citizen["services"].append("water")
citizen["email"] = "xyz123@gmail.com"
print("Citizen details: ", citizen)

complaints = [
    {
        "description" : "water supply stopped",
        "department" : "water",
        "priority" : "high",
        "status" : "pending"
    },
    {
        "description" : "street light not working",
        "department" : "municipal",
        "priority" : "medium",
        "status" : "pending"
    },
    {
        "description" : "potholes on road",
        "department" : "municipal",
        "priority" : "medium",
        "status" : "pending"
    }
]

for complaint in complaints:
    print("problem: ", complaint["description"])
    print("department: ", complaint["department"])
    print("status: ", complaint["status"])
    print()
