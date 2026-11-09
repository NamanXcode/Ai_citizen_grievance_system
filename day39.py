complaints = [
    #Water
    "Water supply has stopped",
    "Water not coming in my area",
    "There is no water in my area",
    "No water is coming from the tap",
    "Water pressure is very low",
    "Water pipeline is leaking",
    "Water supply is irregular",
    "Dirty water is coming from the tap",
    "Our locality has a water shortage",
    "The water tank is not getting filled",
    "The water is too dirty and polluted",
    "Quality of water is so poor in my area",

    # Electricity
    "No electricity in my area",
    "Power supply has stopped",
    "Electricity connection is not working",
    "There is power cut in my locality",
    "There is a power shortage at home",
    "Electricity keeps going off",
    "The street light are not working",
    "An electric pole is damaged",
    "The power line has fallen",
    "Electricity supply is irregular",
    "Sparking in transformer",
    "Sparking in bus bar on pole",
    "Sparking in my meter box",
    "Meter cable is damaged",
    "My meter box is stolen",
    "Meter box is missing",

    # Gas
    "Gas pipeline has a problem",
    "Gas supply has stopped",
    "There is a gas connection issue",
    "Gas is not coming to my house",
    "The gas pipeline is leaking",
    "My gas connection is not working",
    "There is no gas supply in our area",
    "Gas pressure is very low",
    "I need a new gas connection",
    "The gas meter is damaged",
    "My gas pipeline is damaged",
    "Facing gas leaking problem in my house",

    # Municipal
    "There are potholes on the road",
    "Road is damaged",
    "Street road needs repair",
    "Garbage has not been collected",
    "The street is full of garbage",
    "The drain is blocked",
    "Sewage water is overflowing",
    "A manhole is damaged",
    "The public park is dirty",
    "There is a broken footpath",

    # Transport
    "Bus service is not working",
    "Public transport is unavailable",
    "Bus is not arriving",
    "The bus is always late",
    "There is no bus service in my area",
    "The bus stop is damaged",
    "My bus route has been cancelled",
    "Buses are overcrowded",
    "The bus does not stop at our stop",
    "Public transport is irregular"
]

departments = (
    ["water"] * 12
    + ["electricity"] * 16
    + ["gas"] * 12
    + ["municipal"] * 10
    + ["transport"] * 10
)



from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report



# Split raw text and labels first
X_train_text, X_test_text, y_train, y_test = train_test_split(
    complaints,
    departments,
    test_size=0.2,
    random_state=42,
    stratify=departments
)

#Learn Tf-Idf vocabulary from training text only
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

#Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

#Predict labels for unseen test data
predictions = model.predict(X_test)

#Evaluate
accuracy = accuracy_score(y_test, predictions)

print("\n===== DAY 39 RESULTS =====")
print("Training complaints:", len(y_train))
print("Testing complaints:", len(y_test))
print("Correct predictions:", sum(
    actual == predicted
    for actual, predicted in zip(y_test, predictions)
))
print("Model accuracy:", round(accuracy * 100, 2), "%")

# Show confusion matrix
print("\nConfusion matrix:")
print(confusion_matrix(
    y_test,
    predictions,
    labels=["water", "electricity", "gas", "municipal", "transport"]
))

# Classification report

print("\n===== CLASSIFICATION REPORT =====")

print(classification_report(
    y_test,
    predictions,
    labels=["water", "electrcity", "gas", "municipal", "transport"],
    zero_division=0
))