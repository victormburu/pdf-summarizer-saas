import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
#from matplotlib.pyplot import plt 
#import seaborn as sns
diabetes_data = pd.read_csv(r"../sckit-learn_project/Multiclass_Diabetes_Dataset.csv")

# Splitting data into training and testing sets
X = diabetes_data.drop("Level", axis=1)
y = diabetes_data["Level"]

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Creating and training the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Predictions:", y_pred[:10])

# Visualizing feature importances
