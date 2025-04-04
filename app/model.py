import joblib

lr_model = joblib.load("models/logistic_regression_model.joblib")
preprocessor = joblib.load("models/preprocessor.joblib")
imputer = joblib.load("models/imputer.joblib")