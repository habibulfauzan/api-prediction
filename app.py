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
        
        # Only scale the numeric columns that were used during training
        # Based on your notebook: ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        # These correspond to indices [1, 5, 6, 7] in your features_list
        numeric_features = features[:, [1, 5, 6, 7]]  # age, bmi, HbA1c_level, blood_glucose_level
        numeric_features_scaled = scaler.transform(numeric_features)
        
        # Reconstruct the full feature array with scaled numeric values
        features_scaled = features.copy()
        features_scaled[:, [1, 5, 6, 7]] = numeric_features_scaled
        
        # Make prediction
        prediction = model.predict(features_scaled)[0] the order matches the columns your model was trained on
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
        
        # Only scale the numeric columns that were used during training
        # Based on your notebook: ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
        # These correspond to indices [1, 5, 6, 7] in your features_list
        numeric_features = features[:, [1, 5, 6, 7]]  # age, bmi, HbA1c_level, blood_glucose_level
        numeric_features_scaled = scaler.transform(numeric_features)
        
        # Reconstruct the full feature array with scaled numeric values
        features_scaled = features.copy()
        features_scaled[:, [1, 5, 6, 7]] = numeric_features_scaled
        
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
    # Jalankan server agar bisa diakses dari luar (host='0.0.0.0')
    # di port yang diharapkan oleh Hugging Face (port=7860)
    app.run(host='0.0.0.0', port=7860, debug=True)
