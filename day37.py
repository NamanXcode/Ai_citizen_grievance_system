from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

complaints = [
    "Water supply has stopped",
    "There is not water in my area",
    "Water connection is not working",

    "No electricity in my area",
    "Power supply has stopped",
    "Electricity connection is not working",

    "Gas pipeline has a problem",
    "Gas supply has stopped",
    "There is a gas connection issue",

    "There are potholes on the road",
    "Road  is damaged",
    "Street road needs repair",

    "Bus service is not working",
    "Public transport is unavailable",
    "Bus is not arriving"
]

departments = [
    "water",
    "water",
    "water",

    "electricity",
    "electricity",
    "electricity",

    "gas",
    "gas",
    "gas",

    "municipal",
    "municipal",
    "municipal",

    "transport",
    "transport",
    "transport",
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(complaints)

model = LogisticRegression()
model.fit(X, departments)

new_complaint = [
    "There are several potholes on my street."
]
new_X = vectorizer.transform(new_complaint)
prediction = model.predict(new_X)
print("Predicted Department:", prediction[0])


