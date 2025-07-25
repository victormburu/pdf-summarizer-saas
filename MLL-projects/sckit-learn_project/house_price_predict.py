import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt

#stimulate a clean dataset
np.random.seed(42)
n_sample = 100

data = pd.DataFrame({
    "size": np.random.randint(50, 250, size=n_sample),
    "neighborhood_avg": np.random.randint(100000, 300000, size=n_sample),
    "latitude": np.random.uniform(-1.3, -1.2, size=n_sample),
    "longtitude": np.random.uniform(36.7, 36.9, size=n_sample),
    "has_basement": np.random.choice(["Yes", "No"], size=n_sample)
})
#print(data)

# Simulate price with some relation to inputs (target)
data["price"] = (
    data["size"] * 1500 + (data["has_basement"] == "Yes") * 20000 + 
    np.random.normal(0, 20000, size=n_sample)
)

# Step 2: Separate features and target
X = data.drop(columns="price")
y = data["price"]

# Step 3: Define preprocessing for numeric and categorical
numeric_feature = ["size", "neighborhood_avg", "latitude", "longtitude"]
categorical_feature = ["has_basement"]

numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder()
preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_feature),
    ("cat", categorical_transformer, categorical_feature)
])

# Step 4: Build pipeline (preprocessing + model)
pipe = Pipeline(steps=[
    ("Preprocessor", preprocessor),
    ("model", LinearRegression())
])

# Step 5: Cross-validation (5-fold)
scores = cross_val_score(
    pipe, X, y,
    cv=5,
    scoring="r2"
)

print("Cross-Valitaded R2 scores:", scores)
print("Avg scores R2:", scores.mean())

# Simulate linear model loss function: MSE vs weight
weight_range = np.linspace(1000, 2000, 100)
losses = []

for w in weight_range:
    y_pred = w * data["size"]
    mse = ((y - y_pred) ** 2).mean()
    losses.append(mse)

plt.figure(figsize=(8, 5))
plt.plot(weight_range, losses, color='orange')
plt.title("Simulated MSE vs Weight (for 'size' feature)")
plt.xlabel("Weight (Coefficient for size)")
plt.ylabel("Mean Squared Error (MSE)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Gradient descent simulation
import matplotlib.pyplot as plt

# Reuse your original data
size = data["size"].values
price = data["price"].values

# Define MSE loss for a single feature (size)
def mse_loss(w):
    y_pred = size * w
    return np.mean((price - y_pred) ** 2)

# Define gradient of the loss function
def mse_gradient(w):
    y_pred = size * w
    return -2 * np.mean(size * (price - y_pred))

# Simulate gradient descent
w = 1000             # Initial guess
learning_rate = 1e-3 # Small enough for stable steps
n_steps = 50         # More steps for clearer path

w_path = [w]         # Store weights
loss_path = [mse_loss(w)]

for _ in range(n_steps):
    grad = mse_gradient(w)
    w = w - learning_rate * grad
    w_path.append(w)
    loss_path.append(mse_loss(w))

# Plot the full loss curve
w_range = np.linspace(500, 2000, 200)
losses = [mse_loss(wi) for wi in w_range]

plt.figure(figsize=(10, 6))
plt.plot(w_range, losses, label="MSE Curve")
plt.plot(w_path, loss_path, "ro-", label="Gradient Descent Path", markersize=4)
plt.title("MSE Loss vs Weight (w) for 'size' feature")
plt.xlabel("Weight (w)")
plt.ylabel("Mean Squared Error")
plt.legend()
plt.grid(True)
plt.show()


#Plot R² scores from cross-validation
plt.figure(figsize=(8, 5))
plt.bar(range(1, 6), scores, color='skyblue')
plt.axhline(scores.mean(), color='red', linestyle='--', label=f'Avg R² = {scores.mean():.2f}')
plt.title("Cross-Validated R² Scores (Linear Regression)")
plt.xlabel("Fold")
plt.ylabel("R² Score")
plt.ylim(0, 1)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()