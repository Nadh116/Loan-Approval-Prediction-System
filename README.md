# 🏦 Loan Approval Prediction System

A complete Machine Learning web application that predicts loan approval status using a **balanced and fair** ML model. Built with Python (Flask) backend and React frontend.

## 🎯 Project Overview

This system provides instant loan approval predictions based on applicant financial information. The ML model is specifically designed to be **balanced and fair**, avoiding bias towards rejection.

### ✨ Key Features

- **Balanced ML Model**: Designed for fair predictions (~65% approval rate)
- **Real-time Predictions**: Instant loan approval/rejection with confidence scores
- **Feature Importance**: Shows which factors influenced the decision
- **Modern UI**: Clean, responsive React interface
- **REST API**: Well-documented Flask backend
- **Production Ready**: Complete project structure with error handling

## 🏗️ Project Structure

```
loan-approval-prediction/
│
├── backend/                    # Python Flask API
│   ├── app.py                 # Main Flask application
│   ├── train_model.py         # ML model training script
│   ├── requirements.txt       # Python dependencies
│   └── model/                 # Trained model files (generated)
│       ├── loan_model.pkl
│       ├── scaler.pkl
│       ├── label_encoders.pkl
│       └── feature_columns.pkl
│
├── frontend/                   # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoanForm.js
│   │   │   ├── LoanForm.css
│   │   │   ├── PredictionResult.js
│   │   │   └── PredictionResult.css
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── api.js
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### 1. Backend Setup

```bash
# Navigate to backend directory
cd loan-approval-prediction/backend

# Install Python dependencies
pip install -r requirements.txt

# Train the ML model (IMPORTANT: This creates a balanced model)
python train_model.py

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd loan-approval-prediction/frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will run on `http://localhost:3000`

## 🤖 Machine Learning Model

### Dataset Features

The model uses the following features for prediction:

| Feature | Type | Description |
|---------|------|-------------|
| Gender | Categorical | Male/Female |
| Married | Categorical | Yes/No |
| Dependents | Categorical | 0, 1, 2, 3+ |
| Education | Categorical | Graduate/Not Graduate |
| Self_Employed | Categorical | Yes/No |
| ApplicantIncome | Numerical | Monthly income in $ |
| CoapplicantIncome | Numerical | Coapplicant monthly income in $ |
| LoanAmount | Numerical | Loan amount in $ |
| Loan_Amount_Term | Numerical | Loan term in months |
| Credit_History | Categorical | 1 (Good) / 0 (Poor) |
| Property_Area | Categorical | Urban/Semiurban/Rural |

### Model Training

The system trains and compares three models:
- **Logistic Regression** (with balanced class weights)
- **Decision Tree** (with balanced class weights)
- **Random Forest** (with balanced class weights)

The best performing model is automatically selected and saved.

### Balanced Approach

🎯 **Key Feature**: The model is specifically designed to be **fair and balanced**:
- Target approval rate: ~65% (realistic and fair)
- Uses `class_weight='balanced'` to prevent bias
- Lower income thresholds for inclusivity
- Multiple factors considered for comprehensive evaluation

## 🌐 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "🏦 Loan Approval Prediction API - BALANCED & FAIR",
  "status": "running",
  "model_loaded": true,
  "version": "1.0.0"
}
```

#### 2. Predict Loan Approval
```http
POST /predict
```

**Request Body:**
```json
{
  "Gender": "Male",
  "Married": "Yes",
  "Dependents": "1",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5849,
  "CoapplicantIncome": 0,
  "LoanAmount": 146,
  "Loan_Amount_Term": 360,
  "Credit_History": 1,
  "Property_Area": "Urban"
}
```

**Response:**
```json
{
  "prediction": "Approved",
  "confidence": 0.8234,
  "message": "🎉 Congratulations! Your loan application shows strong indicators for approval.",
  "input_data": { ... },
  "feature_importance": {
    "Credit_History": 0.3456,
    "ApplicantIncome": 0.2341,
    "LoanAmount": 0.1876,
    ...
  }
}
```

#### 3. Model Information
```http
GET /model-info
```

**Response:**
```json
{
  "model_type": "RandomForestClassifier",
  "features": ["Gender", "Married", ...],
  "model_loaded": true,
  "description": "Balanced loan approval model designed for fair predictions",
  "feature_importance": { ... }
}
```

## 💻 Frontend Features

### Loan Application Form
- **Comprehensive Form**: All required fields with validation
- **User-Friendly**: Dropdowns and input validation
- **Responsive Design**: Works on desktop and mobile
- **Real-time Validation**: Immediate feedback on form errors

### Prediction Results
- **Clear Status**: Approved/Rejected with confidence score
- **Visual Indicators**: Color-coded results with icons
- **Feature Importance**: Shows which factors influenced the decision
- **Application Summary**: Review of submitted information
- **New Application**: Easy reset for another prediction

### Connection Status
- **Backend Health**: Real-time connection status
- **Error Handling**: Graceful error messages and retry options
- **Setup Instructions**: Helpful guidance when backend is offline

## 🔧 Development

### Running Tests
```bash
# Backend tests (if implemented)
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Frontend production build
cd frontend
npm run build
```

## 📊 Model Performance

The trained model achieves:
- **Accuracy**: ~85-90% on test data
- **Balanced Predictions**: ~65% approval rate
- **Fair Classification**: Considers multiple factors
- **Feature Importance**: Credit history and income are key factors

## 🚀 Deployment

### Backend Deployment
- Can be deployed on Heroku, AWS, or any Python hosting service
- Requires Python 3.8+ and pip
- Environment variables for configuration

### Frontend Deployment
- Can be deployed on Netlify, Vercel, or any static hosting
- Update API base URL in `src/api.js` for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with React, Flask, and scikit-learn
- Designed for educational and portfolio purposes
- Emphasizes fair and balanced ML practices

## 📞 Support

If you encounter any issues:
1. Check that both backend and frontend are running
2. Ensure the model is trained (`python train_model.py`)
3. Verify all dependencies are installed
4. Check the console for error messages

---

**Made with ❤️ for fair and balanced loan predictions**