from sklearn.feature_extraction.text import TfidfVectorizer

complaints = [
    "water supply has stopped",
    "There is no water in my area",
    "Water connection is not working",
    "No electricity in my area",
    "Power supply has stopped",
    "Electricity connection is not working",
    "Gas pipeline has a problem",
    "Gas supply has stopped",
    "There is a gas connection issue",
    "There are potholes on the road",
    "Road is damaged",
    "Street road needs repair",
    "Bus service is not working",
    "Public transport is unavailable",
    "Bus is not arriving"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(complaints)

new_complaint = [
    "Power is not available in my locality"
]

new_X = vectorizer.transform(new_complaint)

print("\nNew complaint converted successfully")
print(new_X.toarray())
