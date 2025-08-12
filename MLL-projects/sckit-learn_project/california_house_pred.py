from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LinearRegression
#from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

#load datasets
housing = fetch_california_housing()
X = housing.data
y = housing.target

#split into train & test
X_train, X_test, y_train, y_test =train_test_split(
    X,y, test_size=0.2, random_state=42
)

#CREATE & TRAIN THE MODEL
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

#make predictions
y_pred =model.predict(X_test)

#evaluate 
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", mae)
print("Mean Squared Error:", mse)
print("Root Mean Squared Error:", rmse)
print("R^2 Score:", r2)