from sklearn.compose import ColumnTransformer #applying different preprocessing
from sklearn.pipeline import Pipeline #chaining step together
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression #handle missing value
from sklearn.preprocessing import OneHotEncoder, StandardScaler #categories & scaling feature
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor#modeling
from sklearn.model_selection import train_test_split, cross_val_score #splitting into train/test set
from sklearn.metrics import  mean_squared_error, r2_score, mean_absolute_error
import pandas as pd
from datetime import datetime
import math

df = pd.read_csv('../sckit-learn_project/clean_dataset.csv')
# Create salary categories
X = df.drop(columns=['monthly_salary'], axis=1)
y = df['monthly_salary']
#identify numeric & categorical columns
numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_feature = X.select_dtypes(include=['object', 'category']).columns.tolist()

#pipeline for numeric features
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy='median')), #fill missing values with median
    ("scaler", StandardScaler()) #mean 0, std 1
])

#pipeline for categorical features
categorical_pipeline =Pipeline([
    ("imputer", SimpleImputer(strategy='constant', fill_value='__missing__')),
    ('OneHot', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
])

#combine both pipelines into single preprocessor
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_feature)
    
    ])

model = [
    RandomForestRegressor(random_state=42, n_estimators=200, n_jobs=-1), #modeling
    GradientBoostingRegressor(random_state=42, n_estimators=200),
    LinearRegression()
]
#create a full modeling pipeline
for reg in model:
    model_pipeline = Pipeline([ #add polynomial features
    ('preprocessor', preprocessor),# preprocess data
    ('reg', reg)
])
    


#split dataset into 80% train 20% testing 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
cv_scores = cross_val_score(model_pipeline, X_train, y_train, cv=5, scoring='r2')
#fit the pipeline on training data
model_pipeline.fit(X_train, y_train)

#make predictions
y_pred =model_pipeline.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
#Evaluate the model
rmse = math.sqrt(mse) #calculate RMSE
print(f'\nMean Squared Error: {mse}')
print(f'\nR2 Score: {r2}')
print(f'\nMean Absolute Error: {mae}')
print(f'\nCross-Validation Scores: {cv_scores}')
print(f'\nPredictions: {y_pred[:5]}')
print(f'\nRoot Mean Squared Error: {rmse}')