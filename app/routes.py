from flask import render_template, request, jsonify
from app import app
from app.model import lr_model, preprocessor, imputer
import pandas as pd

categorical_features = ["job", "marital", "education", "default", "housing", "loan", 
                        "contact", "month", "day_of_week", "poutcome"]
numerical_features = ["age", "duration", "campaign", "pdays", "previous", "emp.var.rate", 
                      "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        form_data = pd.DataFrame([{
            'age': request.form.get('age'),
            'job': request.form.get('job'),
            'marital': request.form.get('marital'),
            'education': request.form.get('education'),
            'default': request.form.get('default'),
            'housing': request.form.get('housing'),
            'loan': request.form.get('loan'),
            'contact': request.form.get('contact', 'cellular'),
            'month': request.form.get('month', 'may'),
            'day_of_week': request.form.get('day_of_week', 'mon'),
            'duration': request.form.get('duration', '450'), 
            'campaign': request.form.get('campaign', '3'), 
            'pdays': request.form.get('pdays', '200'), 
            'previous': request.form.get('previous', '1'),
            'poutcome': request.form.get('poutcome', 'success'),
            'emp.var.rate': request.form.get('emp.var.rate', '0.5'), 
            'cons.price.idx': request.form.get('cons.price.idx', '94.0'),
            'cons.conf.idx': request.form.get('cons.conf.idx', '-20.0'), 
            'euribor3m': request.form.get('euribor3m', '4.9'),  
            'nr.employed': request.form.get('nr.employed', '5200')
        }])

        # Print raw input data for debugging
        print("\nReceived Form Data:", form_data)

        # Handle missing values
        form_data[categorical_features] = imputer.transform(form_data[categorical_features])

        # Apply preprocessing
        form_data_processed = preprocessor.transform(form_data)

        # Predict using Logistic Regression
        prediction_lr = lr_model.predict(form_data_processed)
        probability = lr_model.predict_proba(form_data_processed)[0][1]
        print("\nPrediction using Logistic Regression:", prediction_lr)
        print("\nPrediction using Logistic Regression probability:", probability)

        # Prediction result
        result = {
            "prediction": "YES" if prediction_lr == "yes" else "NO",
            "probability": f"{probability:.2f}"
        }

        # Debugging output
        print("\nPrediction Result:", result)  

        return render_template('result.html', result=result)

    except Exception as e:
        print("Error:", e)  
        return render_template('result.html', result={"error": str(e)})
