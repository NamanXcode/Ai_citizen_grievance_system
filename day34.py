def predict_department(complaint):

    complaint = complaint.lower()

    if "water" in complaint or "supply" in complaint:
        return "water"

    elif "street light" in complaint or "streetlight" in complaint or "street lamp" in complaint:
        return "municipal"

    elif "electricity" in complaint or "power" in complaint:
        return "electricity"

    elif "gas" in complaint or "pipeline" in complaint:
        return "gas"

    elif "road" in complaint or "pothole" in complaint:
        return "municipal"

    else:
        return "unknown"

def predict_priority(complaint):

    complaint = complaint.lower()

    high_keywords = [
        "emergency",
        "danger",
        "fire",
        "accident",
        "injury",
        "critical",
        "urgent",
        "leakage",
        "leak",
        "leaking",
        "gas leak",
        "gas leaking",
        "gas pipeline",
        "electric shock",
        "high voltage",
        "fallen electric wire",
        "electric wire has fallen",
    ]

    medium_keywords = [
        "not working",
        "broken",
        "damaged",
        "problem",
        "stopped",
        "not coming",
        "not functioning",
        "big",
        "slow",
        "inconvenience",
    ]

    for keyword in high_keywords:
        if keyword in complaint:
            return "High"

    for keyword in medium_keywords:
        if keyword in complaint:
            return "Medium"

    return "Low"

print(predict_department("Gas pipeline is leaking"))
print(predict_priority("Gas pipeline is leaking"))

print(predict_department("Street light not working"))
print(predict_priority("Street light not working"))