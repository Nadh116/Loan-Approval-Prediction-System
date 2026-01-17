from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Global variables to store model and preprocessors
model = None
scaler = None
label_encoders = None
feature_columns = None

def load_model():
    """Load the trained model and preprocessors"""
    global model, scaler, label_encoders, feature_columns
    
    try:
        model = joblib.load('model/loan_model.pkl')
        scaler = joblib.load('model/scaler.pkl')
        label_encoders = joblib.load('model/label_encoders.pkl')
        feature_columns = joblib.load('model/feature_columns.pkl')
        print("✅ Model and preprocessors loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def preprocess_input(data):
    """Preprocess input data for prediction"""
    try:
        # Create DataFrame from input
        df = pd.DataFrame([data])
        
        # Encode categorical variables
        categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 
                              'Self_Employed', 'Property_Area']
        
        for col in categorical_columns:
            if col in df.columns and col in label_encoders:
                # Handle unknown categories
                try:
                    df[col] = label_encoders[col].transform(df[col])
                except ValueError:
                    # If unknown category, use the most frequent class
                    df[col] = 0
        
        # Ensure all required columns are present
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data
        df = df[feature_columns]
        
        # Scale features
        df_scaled = scaler.transform(df)
        
        return df_scaled
    
    except Exception as e:
        print(f"❌ Error in preprocessing: {e}")
        return None

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "🏦 Loan Approval Prediction API - BALANCED & FAIR",
        "status": "running",
        "model_loaded": model is not None,
        "version": "1.0.0"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict loan approval with balanced approach"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate required fields
        required_fields = [
            'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 
            'Loan_Amount_Term', 'Credit_History', 'Property_Area'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {missing_fields}"
            }), 400
        
        # Preprocess input
        processed_data = preprocess_input(data)
        if processed_data is None:
            return jsonify({"error": "Error processing input data"}), 400
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        prediction_proba = model.predict_proba(processed_data)[0]
        
        # Convert prediction to readable format
        loan_status = "Approved" if prediction == 1 else "Rejected"
        confidence = float(max(prediction_proba))
        
        # Get feature importance if available
        feature_importance = None
        if hasattr(model, 'feature_importances_'):
            importance_dict = dict(zip(feature_columns, model.feature_importances_))
            # Sort by importance
            feature_importance = dict(sorted(importance_dict.items(), 
                                           key=lambda x: x[1], reverse=True))
        
        # Add helpful message
        message = ""
        if loan_status == "Approved":
            message = "🎉 Congratulations! Your loan application shows strong indicators for approval."
        else:
            message = "📋 Your application needs some improvements. Consider enhancing your credit history or income."
        
        response = {
            "prediction": loan_status,
            "confidence": round(confidence, 4),
            "message": message,
            "input_data": data,
            "feature_importance": feature_importance
        }
        
        print(f"🔍 Prediction made: {loan_status} (Confidence: {confidence:.2%})")
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500

@app.route('/model-info')
def model_info():
    """Get model information"""
    try:
        info = {
            "model_type": type(model).__name__,
            "features": feature_columns,
            "model_loaded": model is not None,
            "description": "Balanced loan approval model designed for fair predictions"
        }
        
        # Add feature importance if available
        if hasattr(model, 'feature_importances_'):
            importance_dict = dict(zip(feature_columns, model.feature_importances_))
            info["feature_importance"] = dict(sorted(importance_dict.items(), 
                                                   key=lambda x: x[1], reverse=True))
        
        return jsonify(info)
    
    except Exception as e:
        return jsonify({"error": f"Error getting model info: {str(e)}"}), 500

@app.route('/health')
def health():
    """Detailed health check"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "components": {
            "model": "✅" if model is not None else "❌",
            "scaler": "✅" if scaler is not None else "❌",
            "encoders": "✅" if label_encoders is not None else "❌",
            "features": "✅" if feature_columns is not None else "❌"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Balanced Loan Approval Prediction API...")
    
    # Load model on startup
    if not load_model():
        print("⚠️ Warning: Model not loaded. Please run train_model.py first.")
        print("📝 Steps to setup:")
        print("   1. pip install -r requirements.txt")
        print("   2. python train_model.py")
        print("   3. python app.py")
    else:
        print("🎯 Model loaded successfully - Ready for fair predictions!")
    
    print("🌐 Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)