print("=====Citizen Service Portal=====")


def save_citizen(citizen):

    import json

    with open("citizen.json", "w") as file:
        json.dump(citizen, file, indent=4)

def load_citizen():
    import json

    with open("citizen.json", "r") as file:
        citizen = json.load(file)
    return citizen

citizen = {
    "name": "naman sharma",
    "age": 22,
    "city": "delhi",
    "services": ["electricity"],
    "complaints": ["no electricity"]
}

citizen["services"].append("water")
citizen["complaints"].append("no water")

save_citizen(citizen)
loaded_citizen = load_citizen()
print(loaded_citizen)