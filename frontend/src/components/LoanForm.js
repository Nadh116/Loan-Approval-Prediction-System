import React, { useState } from 'react';
import './LoanForm.css';

const LoanForm = ({ onSubmit, loading }) => {
    const [formData, setFormData] = useState({
        Gender: '',
        Married: '',
        Dependents: '',
        Education: '',
        Self_Employed: '',
        ApplicantIncome: '',
        CoapplicantIncome: '',
        LoanAmount: '',
        Loan_Amount_Term: '',
        Credit_History: '',
        Property_Area: ''
    });

    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        // Required field validation
        Object.keys(formData).forEach(key => {
            if (!formData[key] && formData[key] !== 0) {
                newErrors[key] = 'This field is required';
            }
        });

        // Numeric field validation
        const numericFields = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount'];
        numericFields.forEach(field => {
            if (formData[field] && isNaN(formData[field])) {
                newErrors[field] = 'Must be a valid number';
            }
            if (formData[field] && parseFloat(formData[field]) < 0) {
                newErrors[field] = 'Must be a positive number';
            }
        });

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (validateForm()) {
            // Convert numeric fields to numbers
            const processedData = {
                ...formData,
                ApplicantIncome: parseInt(formData.ApplicantIncome),
                CoapplicantIncome: parseInt(formData.CoapplicantIncome),
                LoanAmount: parseInt(formData.LoanAmount),
                Loan_Amount_Term: parseInt(formData.Loan_Amount_Term),
                Credit_History: parseInt(formData.Credit_History)
            };

            onSubmit(processedData);
        }
    };

    return (
        <div className="loan-form-container">
            <h2>Loan Application Form</h2>
            <form onSubmit={handleSubmit} className="loan-form">
                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="Gender">Gender</label>
                        <select
                            id="Gender"
                            name="Gender"
                            value={formData.Gender}
                            onChange={handleChange}
                            className={errors.Gender ? 'error' : ''}
                        >
                            <option value="">Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                        {errors.Gender && <span className="error-message">{errors.Gender}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="Married">Marital Status</label>
                        <select
                            id="Married"
                            name="Married"
                            value={formData.Married}
                            onChange={handleChange}
                            className={errors.Married ? 'error' : ''}
                        >
                            <option value="">Select Status</option>
                            <option value="Yes">Married</option>
                            <option value="No">Single</option>
                        </select>
                        {errors.Married && <span className="error-message">{errors.Married}</span>}
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="Dependents">Dependents</label>
                        <select
                            id="Dependents"
                            name="Dependents"
                            value={formData.Dependents}
                            onChange={handleChange}
                            className={errors.Dependents ? 'error' : ''}
                        >
                            <option value="">Select Dependents</option>
                            <option value="0">0</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3+">3+</option>
                        </select>
                        {errors.Dependents && <span className="error-message">{errors.Dependents}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="Education">Education</label>
                        <select
                            id="Education"
                            name="Education"
                            value={formData.Education}
                            onChange={handleChange}
                            className={errors.Education ? 'error' : ''}
                        >
                            <option value="">Select Education</option>
                            <option value="Graduate">Graduate</option>
                            <option value="Not Graduate">Not Graduate</option>
                        </select>
                        {errors.Education && <span className="error-message">{errors.Education}</span>}
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="Self_Employed">Self Employed</label>
                        <select
                            id="Self_Employed"
                            name="Self_Employed"
                            value={formData.Self_Employed}
                            onChange={handleChange}
                            className={errors.Self_Employed ? 'error' : ''}
                        >
                            <option value="">Select Option</option>
                            <option value="Yes">Yes</option>
                            <option value="No">No</option>
                        </select>
                        {errors.Self_Employed && <span className="error-message">{errors.Self_Employed}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="Property_Area">Property Area</label>
                        <select
                            id="Property_Area"
                            name="Property_Area"
                            value={formData.Property_Area}
                            onChange={handleChange}
                            className={errors.Property_Area ? 'error' : ''}
                        >
                            <option value="">Select Area</option>
                            <option value="Urban">Urban</option>
                            <option value="Semiurban">Semiurban</option>
                            <option value="Rural">Rural</option>
                        </select>
                        {errors.Property_Area && <span className="error-message">{errors.Property_Area}</span>}
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="ApplicantIncome">Applicant Income ($)</label>
                        <input
                            type="number"
                            id="ApplicantIncome"
                            name="ApplicantIncome"
                            value={formData.ApplicantIncome}
                            onChange={handleChange}
                            placeholder="Enter monthly income"
                            className={errors.ApplicantIncome ? 'error' : ''}
                        />
                        {errors.ApplicantIncome && <span className="error-message">{errors.ApplicantIncome}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="CoapplicantIncome">Coapplicant Income ($)</label>
                        <input
                            type="number"
                            id="CoapplicantIncome"
                            name="CoapplicantIncome"
                            value={formData.CoapplicantIncome}
                            onChange={handleChange}
                            placeholder="Enter coapplicant income"
                            className={errors.CoapplicantIncome ? 'error' : ''}
                        />
                        {errors.CoapplicantIncome && <span className="error-message">{errors.CoapplicantIncome}</span>}
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="LoanAmount">Loan Amount ($)</label>
                        <input
                            type="number"
                            id="LoanAmount"
                            name="LoanAmount"
                            value={formData.LoanAmount}
                            onChange={handleChange}
                            placeholder="Enter loan amount"
                            className={errors.LoanAmount ? 'error' : ''}
                        />
                        {errors.LoanAmount && <span className="error-message">{errors.LoanAmount}</span>}
                    </div>

                    <div className="form-group">
                        <label htmlFor="Loan_Amount_Term">Loan Term (months)</label>
                        <select
                            id="Loan_Amount_Term"
                            name="Loan_Amount_Term"
                            value={formData.Loan_Amount_Term}
                            onChange={handleChange}
                            className={errors.Loan_Amount_Term ? 'error' : ''}
                        >
                            <option value="">Select Term</option>
                            <option value="120">120 months (10 years)</option>
                            <option value="180">180 months (15 years)</option>
                            <option value="240">240 months (20 years)</option>
                            <option value="300">300 months (25 years)</option>
                            <option value="360">360 months (30 years)</option>
                        </select>
                        {errors.Loan_Amount_Term && <span className="error-message">{errors.Loan_Amount_Term}</span>}
                    </div>
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="Credit_History">Credit History</label>
                        <select
                            id="Credit_History"
                            name="Credit_History"
                            value={formData.Credit_History}
                            onChange={handleChange}
                            className={errors.Credit_History ? 'error' : ''}
                        >
                            <option value="">Select Credit History</option>
                            <option value="1">Good (1)</option>
                            <option value="0">Poor (0)</option>
                        </select>
                        {errors.Credit_History && <span className="error-message">{errors.Credit_History}</span>}
                    </div>
                </div>

                <button
                    type="submit"
                    className="submit-button"
                    disabled={loading}
                >
                    {loading ? 'Predicting...' : 'Predict Loan Approval'}
                </button>
            </form>
        </div>
    );
};

export default LoanForm;