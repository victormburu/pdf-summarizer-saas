from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import precision_score, recall_score, confusion_matrix

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

clf_hinge = SGDClassifier(loss="hinge", max_iter=1000, random_state=42)
clf_hinge.fit(X_train, y_train)

y_test_pred = clf_hinge.predict(X_test)

print("Precision score:", precision_score(
    y_test, y_test_pred, average='weighted'))
print("Recall score:", recall_score(y_test, y_test_pred, average='weighted'))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))