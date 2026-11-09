print("=====Citizen Service Portal=====")

def register_citizen(name, age, mobile, city):
    citizen =  {
        "name" : name,
        "age" : age,
        "mobile" : mobile,
        "city" : city,
        "services" : [],
        "complaints" : []
    }
    return citizen

def add_service(citizen, service):
    citizen["services"].append(service)
    return citizen

def submit_complaint(citizen, complaint):
    citizen["complaints"].append(complaint)
    return citizen

def view_complaints(citizen):
    if len(citizen["complaints"]) > 0:
        return citizen["complaints"]
    else:
        return "No complaints submitted."

def main():
    citizen = register_citizen("Naman", 25, "1234567890", "new delhi")
    print("citizen registered successfully.")

    citizen = add_service(citizen, "electricity")
    citizen = add_service(citizen, "water")

    citizen = submit_complaint(citizen, "water supply is not working.")
    print("\ncitizen details:")
    print(citizen)

    citizen = submit_complaint(citizen, "street light is not working.")

    print("\ncomplaints:")
    print(view_complaints(citizen))
main()
