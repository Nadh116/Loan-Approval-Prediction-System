import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, Classification_report, confusion_matrix
import joblib
import os

def create_sample_data():
    """Create sample loan dataset for training with BALANCED approvals"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'Married': np.random.choice(['Yes', 'No'], n_samples),
        'Dependents': np.random.choice(['0', '1', '2', '3+'], n_samples),
        'Education': np.random.choice(['Graduate', 'Not Graduate'], n_samples),
        'Self_Employed': np.random.choice(['Yes', 'No'], n_samples),
        'ApplicantIncome': np.random.randint(1000, 15000, n_samples),
        'CoapplicantIncome': np.random.randint(0, 8000, n_samples),
        'LoanAmount': np.random.randint(50, 700, n_samples),
        'Loan_Amount_Term': np.random.choice([120, 180, 240, 300, 360], n_samples),
        'Credit_History': np.random.choice([0, 1], n_samples, p=[0.2, 0.8]),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create BALANCED and FAIR loan approval logic (NOT biased towards rejection)
    approval_prob = (
        (df['ApplicantIncome'] > 3000) * 0.25 +  # Lower income threshold
        (df['Credit_History'] == 1) * 0.35 +     # Credit history important
        (df['Education'] == 'Graduate') * 0.15 +  # Education bonus
        (df['Married'] == 'Yes') * 0.1 +          # Married stability
        ((df['ApplicantIncome'] + df['CoapplicantIncome']) > 6000) * 0.2 +  # Combined income
        (df['LoanAmount'] < 400) * 0.15 +         # Reasonable loan amount
        np.random.random(n_samples) * 0.4         # Random factor for diversity
    )
    
    # Ensure balanced dataset - aim for ~65% approval rate (realistic and fair)
    df['Loan_Status'] = np.where(approval_prob > 0.45, 'Y', 'N')  # Lower threshold = more approvals
    
    # Force balance if needed
    approval_rate = (df['Loan_Status'] == 'Y').mean()
    print(f"Initial approval rate: {approval_rate:.2%}")
    
    # If approval rate is too low, adjust some rejections to approvals
    if approval_rate < 0.6:
        rejected_indices = df[df['Loan_Status'] == 'N'].index
        n_to_flip = int(len(rejected_indices) * 0.3)  # Flip 30% of rejections
        flip_indices = np.random.choice(rejected_indices, n_to_flip, replace=False)
        df.loc[flip_indices, 'Loan_Status'] = 'Y'
        
    final_approval_rate = (df['Loan_Status'] == 'Y').mean()
    print(f"Final approval rate: {final_approval_rate:.2%}")
    
    return df

def preprocess_data(df):
    """Preprocess the loan dataset"""
    # Handle missing values (if any)
    df = df.fillna(df.mode().iloc[0])
    
    # Create label encoders
    label_encoders = {}
    categorical_columns = ['Gender', 'Married', 'Dependents', 'Education', 
                          'Self_Employed', 'Property_Area']
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Encode target variable
    target_encoder = LabelEncoder()
    df['Loan_Status'] = target_encoder.fit_transform(df['Loan_Status'])
    label_encoders['Loan_Status'] = target_encoder
    
    return df, label_encoders

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple ML models and return the best one"""
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced'),
        'Decision Tree': DecisionTreeClassifier(random_state=42, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    print("Model Performance Comparison:")
    print("-" * 50)
    
    for name, model in models.items():
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\n{name}:")
        print(f"Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Update best model
        if accuracy > best_score:
            best_score = accuracy
            best_model = model
            best_name = name
    
    print(f"\nBest Model: {best_name} with accuracy: {best_score:.4f}")
    return best_model, best_name

def main():
    """Main training pipeline"""
    print("Starting BALANCED Loan Approval Model Training...")
    print("🎯 Goal: Create a fair model that doesn't reject too many applications")
    
    # Create or load data
    print("Creating balanced sample dataset...")
    df = create_sample_data()
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess data
    print("Preprocessing data...")
    df_processed, label_encoders = preprocess_data(df.copy())
    
    # Prepare features and target
    X = df_processed.drop('Loan_Status', axis=1)
    y = df_processed['Loan_Status']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models with balanced class weights
    print("Training balanced models...")
    best_model, best_name = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Create model directory
    os.makedirs('model', exist_ok=True)
    
    # Save model and preprocessors
    joblib.dump(best_model, 'model/loan_model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    joblib.dump(label_encoders, 'model/label_encoders.pkl')
    joblib.dump(X.columns.tolist(), 'model/feature_columns.pkl')
    
    print(f"\n✅ Model training completed!")
    print(f"🏆 Best model ({best_name}) saved to model/loan_model.pkl")
    print("📊 Scaler saved to model/scaler.pkl")
    print("🏷️ Label encoders saved to model/label_encoders.pkl")
    
    # Feature importance (if available)
    if hasattr(best_model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': best_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📈 Feature Importance:")
        print(feature_importance)
        
        # Save feature importance
        feature_importance.to_csv('model/feature_importance.csv', index=False)
    
    # Test prediction on sample data
    print("\n🧪 Testing model with sample predictions...")
    sample_data = X_test_scaled[:5]
    predictions = best_model.predict(sample_data)
    probabilities = best_model.predict_proba(sample_data)
    
    for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
        status = "Approved" if pred == 1 else "Rejected"
        confidence = max(prob)
        print(f"Sample {i+1}: {status} (Confidence: {confidence:.2%})")

if __name__ == "__main__":
    main()