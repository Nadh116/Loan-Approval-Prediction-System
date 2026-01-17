import React, { useState, useEffect } from 'react';
import LoanForm from './components/LoanForm';
import PredictionResult from './components/PredictionResult';
import { predictLoan, checkHealth } from './api';
import './App.css';

function App() {
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [backendStatus, setBackendStatus] = useState('checking');

    useEffect(() => {
        // Check backend health on component mount
        checkBackendHealth();
    }, []);

    const checkBackendHealth = async () => {
        try {
            await checkHealth();
            setBackendStatus('connected');
        } catch (error) {
            setBackendStatus('disconnected');
            setError('Backend server is not running. Please start the Flask server.');
        }
    };

    const handlePrediction = async (loanData) => {
        setLoading(true);
        setError(null);

        try {
            const result = await predictLoan(loanData);
            setPrediction(result);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setPrediction(null);
        setError(null);
    };

    const retryConnection = () => {
        setBackendStatus('checking');
        setError(null);
        checkBackendHealth();
    };

    return (
        <div className="App">
            <header className="app-header">
                <h1>🏦 Loan Approval Prediction System</h1>
                <p>Get instant loan approval predictions using Machine Learning</p>

                <div className={`status-indicator ${backendStatus}`}>
                    <span className="status-dot"></span>
                    <span className="status-text">
                        {backendStatus === 'connected' && 'Backend Connected'}
                        {backendStatus === 'disconnected' && 'Backend Disconnected'}
                        {backendStatus === 'checking' && 'Checking Connection...'}
                    </span>
                    {backendStatus === 'disconnected' && (
                        <button className="retry-button" onClick={retryConnection}>
                            Retry
                        </button>
                    )}
                </div>
            </header>

            <main className="app-main">
                {error && (
                    <div className="error-banner">
                        <div className="error-content">
                            <span className="error-icon">⚠️</span>
                            <span className="error-message">{error}</span>
                            <button className="error-close" onClick={() => setError(null)}>
                                ×
                            </button>
                        </div>
                    </div>
                )}

                {backendStatus === 'disconnected' ? (
                    <div className="connection-error">
                        <h2>🔌 Backend Connection Required</h2>
                        <p>Please start the Flask backend server to use the prediction system.</p>
                        <div className="setup-instructions">
                            <h3>Quick Setup:</h3>
                            <ol>
                                <li>Navigate to the backend directory</li>
                                <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                                <li>Train the model: <code>python train_model.py</code></li>
                                <li>Start the server: <code>python app.py</code></li>
                            </ol>
                        </div>
                        <button className="retry-button large" onClick={retryConnection}>
                            Check Connection Again
                        </button>
                    </div>
                ) : prediction ? (
                    <PredictionResult result={prediction} onReset={handleReset} />
                ) : (
                    <LoanForm onSubmit={handlePrediction} loading={loading} />
                )}
            </main>

            <footer className="app-footer">
                <p>Built with React + Flask + Machine Learning</p>
                <p>© 2024 Loan Approval Prediction System</p>
            </footer>
        </div>
    );
}

export default App;