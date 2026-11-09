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
        "stopped",
        "blocked",
        "damaged",
        "broken",
        "leaking",
        "irregular",
        "low pressure",
        "garbage"
    ]

    for keyword in high_keywords:
        if keyword in complaint:
            return "High"

    for keyword in medium_keywords:
        if keyword in complaint:
            return "Medium"

    return "Low"


