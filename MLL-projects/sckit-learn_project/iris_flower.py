#import necessary libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.tree import DecisionTreeClassifier as DecisionClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay

# Load the iris dataset
iris = load_iris()
X = iris.data #features
y = iris.target #target 

#split into train & test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#create & train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

#evaluate model
print("Accuracy:", accuracy_score(y_test,y_pred))
print("\nClassification Report:", classification_report(y_test, y_pred))

#visualize confusion m
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)

