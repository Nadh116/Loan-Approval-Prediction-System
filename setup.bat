@echo off
echo 🏦 Loan Approval Prediction System Setup
echo =====================================

echo.
echo 📦 Setting up Backend...
cd backend
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 🤖 Training ML Model...
python train_model.py

echo.
echo 📦 Setting up Frontend...
cd ../frontend
echo Installing Node.js dependencies...
npm install

echo.
echo ✅ Setup Complete!
echo.
echo 🚀 To start the application:
echo    1. Backend: cd backend && python app.py
echo    2. Frontend: cd frontend && npm start
echo.
echo 🌐 Frontend will be available at: http://localhost:3000
echo 🔧 Backend API will be available at: http://localhost:5000
echo.
pause