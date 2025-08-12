from sklearn.compose import ColumnTransformer #applying different preprocessing
from sklearn.pipeline import Pipeline #chaining step together
from sklearn.impute import SimpleImputer #handle missing value
from sklearn.preprocessing import OneHotEncoder, StandardScaler #categories & scaling feature 
from sklearn.ensemble import RandomForestRegressor#ML model
from sklearn.model_selection import train_test_split #splitting into train/test set
from sklearn.metrics import  mean_squared_error, r2_score, mean_absolute_error
import pandas as pd


df = pd.read_csv('../sckit-learn_project/sample_employee_data.csv')
# Create salary categories
X = df.drop(columns=['salary'])
y = df['salary']

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
    ("imputer", SimpleImputer(strategy='most_frequent', fill_value='__missing__')),
    ('OneHot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

#combine both pipelines into single preprocessor
preprocessor = ColumnTransformer([
    ("num", numeric_pipeline, numeric_features),
    ("cat", categorical_pipeline, categorical_feature)
    
    ])

#create a full modeling pipeline
model_pipeline = Pipeline([
    ('preprocessor', preprocessor), # preprocess data
    ('reg', RandomForestRegressor(random_state=42))
])

#split dataset into 80% train 20% testing 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#fit the pipeline on training data
model_pipeline.fit(X_train, y_train)

#make predictions
y_pred =model_pipeline.predict(X_test)

#Evaluate the model
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
#rint("Root Mean Squared Error:", mean_squared_error(y_test, y_pred, squared=False))
print("R2 Score:", r2_score(y_test, y_pred))
print("Mean Absolute Error:", mean_absolute_error(y_test, y_pred))
print("Predictions:", y_pred[:5])# Display first 5 predictions