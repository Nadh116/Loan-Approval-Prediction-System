"""
Test script for the Loan Approval Prediction API
Run this after starting the Flask server to test the API endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    print("\n🔍 Testing model info...")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint with sample data"""
    print("\n🔍 Testing prediction...")
    
    # Sample loan application data
    sample_data = {
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=sample_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_predictions():
    """Test multiple predictions with different scenarios"""
    print("\n🔍 Testing multiple prediction scenarios...")
    
    test_cases = [
        {
            "name": "High Income Graduate",
            "data": {
                "Gender": "Female",
                "Married": "Yes",
                "Dependents": "0",
                "Education": "Graduate",
                "Self_Employed": "No",
                "ApplicantIncome": 8000,
                "CoapplicantIncome": 3000,
                "LoanAmount": 200,
                "Loan_Amount_Term": 360,
                "Credit_History": 1,
                "Property_Area": "Urban"
            }
        },
        {
            "name": "Low Income, Poor Credit",
            "data": {
                "Gender": "Male",
                "Married": "No",
                "Dependents": "2",
                "Education": "Not Graduate",
                "Self_Employed": "Yes",
                "ApplicantIncome": 2000,
                "CoapplicantIncome": 0,
                "LoanAmount": 500,
                "Loan_Amount_Term": 180,
                "Credit_History": 0,
                "Property_Area": "Rural"
            }
        },
        {
            "name": "Medium Income, Good Profile",
            "data": {
                "Gender": "Female",
                "Married": "Yes",
                "Dependents": "1",
                "Education": "Graduate",
                "Self_Employed": "No",
                "ApplicantIncome": 4500,
                "CoapplicantIncome": 2000,
                "LoanAmount": 300,
                "Loan_Amount_Term": 360,
                "Credit_History": 1,
                "Property_Area": "Semiurban"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Result: {result['prediction']}")
                print(f"   Confidence: {result['confidence']:.2%}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 Loan Approval API Test Suite")
    print("=" * 40)
    
    # Test health check
    if not test_health_check():
        print("❌ Health check failed. Make sure the server is running.")
        return
    
    # Test model info
    test_model_info()
    
    # Test single prediction
    test_prediction()
    
    # Test multiple predictions
    test_multiple_predictions()
    
    print("\n✅ All tests completed!")
    print("\n💡 Tips:")
    print("   - Make sure Flask server is running: python app.py")
    print("   - Make sure model is trained: python train_model.py")
    print("   - Check server logs for detailed information")

if __name__ == "__main__":
    main()