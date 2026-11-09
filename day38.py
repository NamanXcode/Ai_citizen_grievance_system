from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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


# Split raw text and labels first
X_train_text, X_test_text, y_train, y_test = train_test_split(
    complaints,
    departments,
    test_size=0.4,
    random_state=42,
    stratify=departments
)

#Learn Tf-Idf vocabulary from training text only
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

#Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

#Predict labels for unseen test data
predictions = model.predict(X_test)

#Evaluate
accuracy = accuracy_score(y_test, predictions)

print("Testing complaints:", len(y_test))
print("Correct predictions:", sum(
    actual == predicted
    for actual, predicted in zip(y_test, predictions)
))
print("Model accuracy:", round(accuracy * 100, 2), "%")

