import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

#importing & exploring data
train = pd.read_csv(r"../sckit-learn_project/train.csv")


#feature & target
Z = train.drop("price_range", axis=1)#features
y = train["price_range"]#target


#splitting data
Z_train, Z_test, y_train, y_test = train_test_split(
    Z, y, test_size=0.2, random_state=42
)

#data preprocessing
scaler = StandardScaler()
Z_train = scaler.fit_transform(Z_train)
Z_test = scaler.transform(Z_test)

#create & train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(Z_train, y_train)

#predicting
y_pred = model.predict(Z_test)

#evaluating model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

#predicting on test set
test = pd.read_csv(r"../sckit-learn_project/test.csv")
test_feature = test.drop("id", axis=1)
test_scaled = scaler.transform(test_feature)
predictions = model.predict(test_scaled)

#save file
submission = pd.DataFrame({"id": test["id"], "price_range": predictions})
submission.to_csv(r"../sckit-learn_project/submission.csv", index=False)
print("Submission file created successfully.")
