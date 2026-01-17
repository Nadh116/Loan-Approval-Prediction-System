import React from 'react';
import './PredictionResult.css';

const PredictionResult = ({ result, onReset }) => {
    const isApproved = result.prediction === 'Approved';

    return (
        <div className="prediction-result-container">
            <div className={`result-card ${isApproved ? 'approved' : 'rejected'}`}>
                <div className="result-icon">
                    {isApproved ? '✅' : '❌'}
                </div>

                <h2 className="result-title">
                    Loan {result.prediction}
                </h2>

                <div className="confidence-section">
                    <p className="confidence-label">Confidence Score</p>
                    <div className="confidence-bar">
                        <div
                            className="confidence-fill"
                            style={{ width: `${result.confidence * 100}%` }}
                        ></div>
                    </div>
                    <p className="confidence-value">{(result.confidence * 100).toFixed(1)}%</p>
                </div>

                <div className="result-message">
                    {isApproved ? (
                        <p>🎉 Congratulations! Your loan application has been approved based on the provided information.</p>
                    ) : (
                        <p>We're sorry, but your loan application was not approved at this time. Please consider improving your financial profile and reapplying.</p>
                    )}
                </div>

                {result.feature_importance && (
                    <div className="feature-importance">
                        <h3>Key Factors Considered</h3>
                        <div className="importance-list">
                            {Object.entries(result.feature_importance)
                                .slice(0, 5)
                                .map(([feature, importance]) => (
                                    <div key={feature} className="importance-item">
                                        <span className="feature-name">
                                            {feature.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim()}
                                        </span>
                                        <div className="importance-bar">
                                            <div
                                                className="importance-fill"
                                                style={{ width: `${importance * 100}%` }}
                                            ></div>
                                        </div>
                                        <span className="importance-value">
                                            {(importance * 100).toFixed(1)}%
                                        </span>
                                    </div>
                                ))}
                        </div>
                    </div>
                )}

                <div className="input-summary">
                    <h3>Application Summary</h3>
                    <div className="summary-grid">
                        <div className="summary-item">
                            <span className="summary-label">Applicant Income:</span>
                            <span className="summary-value">${result.input_data.ApplicantIncome?.toLocaleString()}</span>
                        </div>
                        <div className="summary-item">
                            <span className="summary-label">Loan Amount:</span>
                            <span className="summary-value">${result.input_data.LoanAmount?.toLocaleString()}</span>
                        </div>
                        <div className="summary-item">
                            <span className="summary-label">Credit History:</span>
                            <span className="summary-value">{result.input_data.Credit_History === 1 ? 'Good' : 'Poor'}</span>
                        </div>
                        <div className="summary-item">
                            <span className="summary-label">Education:</span>
                            <span className="summary-value">{result.input_data.Education}</span>
                        </div>
                    </div>
                </div>

                <button className="new-application-button" onClick={onReset}>
                    New Application
                </button>
            </div>
        </div>
    );
};

export default PredictionResult;