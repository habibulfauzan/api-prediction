from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Load the trained pipeline model (includes preprocessing/scaling)
try:
    with open('rf_inference.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    
    print("Model pipeline loaded successfully!")
except Exception as e:
    print(f"Error loading model pipeline: {e}")
    model = None

@app.route('/')
def home():
    return jsonify({
        'message': 'Diabetes Prediction API is running!',
        'status': 'success'
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Create DataFrame with proper column names (same as training data)
        # Column order must match the training data
        features_df = pd.DataFrame({
            'gender': [data['gender']],
            'age': [data['age']],
            'hypertension': [data['hypertension']],
            'heart_disease': [data['heart_disease']],
            'smoking_history': [data['smoking_history']],
            'bmi': [data['bmi']],
            'HbA1c_level': [data['HbA1c_level']],
            'blood_glucose_level': [data['blood_glucose_level']]
        })
        
        # Debug: print data before prediction
        print("\n=== DATA SEBELUM PREDIKSI ===")
        print("Input dari frontend:")
        print(data)
        print("\nDataFrame yang akan diprediksi:")
        print(features_df)
        print("=" * 50)
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        
        # Get prediction probabilities
        prediction_proba = model.predict_proba(features_df)[0]
        
        # prediction_proba[0] = probability of class 0 (No Diabetes)
        # prediction_proba[1] = probability of class 1 (Diabetes)
        no_diabetes_prob = float(prediction_proba[0]) * 100
        diabetes_prob = float(prediction_proba[1]) * 100
        
        return jsonify({
            'prediction': int(prediction),
            'message': 'Prediction successful',
            'probability': {
                'no_diabetes': round(no_diabetes_prob, 2),
                'diabetes': round(diabetes_prob, 2)
            }
        })
        
    except KeyError as e:
        # Handle cases where a required key is missing in the JSON payload
        return jsonify({
            'error': f'Missing data for: {str(e)}',
            'message': 'Error processing request'
        }), 400
    except Exception as e:
        # Handle other potential errors during prediction
        return jsonify({
            'error': str(e),
            'message': 'Error processing request'
        }), 400

# This block is for local development.
# Render will use Gunicorn to run the app, so it won't execute this.
if __name__ == '__main__':
    # Jalankan server agar bisa diakses dari luar (host='0.0.0.0')
    app.run(host='0.0.0.0', port=7860, debug=True)