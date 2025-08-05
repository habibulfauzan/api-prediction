from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
# Enable CORS for all routes from all origins
CORS(app) 

# Load the model and scaler
# It's better to load them once when the app starts
try:
    with open('best_rf_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
except FileNotFoundError:
    print("Error: Model or scaler file not found. Make sure 'best_rf_model.pkl' and 'scaler.pkl' are in the same directory.")
    model = None
    scaler = None
except Exception as e:
    print(f"An error occurred while loading files: {e}")
    model = None
    scaler = None

@app.route('/')
def home():
    # A simple route to check if the API is running
    return "Diabetes Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    # Check if model and scaler were loaded successfully
    if model is None or scaler is None:
        return jsonify({
            'error': 'Model or scaler not loaded properly. Check server logs.'
        }), 500

    try:
        data = request.get_json(force=True)
        
        # Extract features in the correct order as per your training
        # Ensure the order matches the columns your model was trained on
        features_list = [
            data['gender'],
            data['age'],
            data['hypertension'],
            data['heart_disease'],
            data['smoking_history'],
            data['bmi'],
            data['HbA1c_level'],
            data['blood_glucose_level']
        ]
        
        # Convert to numpy array and reshape for a single prediction
        features = np.array(features_list).reshape(1, -1)
        
        # Scale the features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'message': 'Prediction successful'
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
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the app, accessible from any IP on the network
    app.run(host='0.0.0.0', port=port, debug=True)
