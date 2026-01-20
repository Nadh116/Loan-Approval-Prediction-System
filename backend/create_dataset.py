"""
Create and save the loan dataset as CSV files
This script generates the dataset and saves it for analysis and presentation
"""

import pandas as pd
import numpy as np
import os

def create_loan_dataset():
    """Create comprehensive loan dataset and save as CSV"""
    np.random.seed(42)  # For reproducible results
    n_samples = 1000
    
    print("🏦 Creating Loan Approval Dataset...")
    print(f"📊 Generating {n_samples} loan applications...")
    
    # Generate realistic loan data
    data = {
        'Loan_ID': [f'LP{str(i).zfill(6)}' for i in range(1, n_samples + 1)],
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
    
    # Create BALANCED and FAIR loan approval logic
    print("🎯 Applying balanced approval logic...")
    approval_prob = (
        (df['ApplicantIncome'] > 3000) * 0.25 +  # Lower income threshold
        (df['Credit_History'] == 1) * 0.35 +     # Credit history important
        (df['Education'] == 'Graduate') * 0.15 +  # Education bonus
        (df['Married'] == 'Yes') * 0.1 +          # Married stability
        ((df['ApplicantIncome'] + df['CoapplicantIncome']) > 6000) * 0.2 +  # Combined income
        (df['LoanAmount'] < 400) * 0.15 +         # Reasonable loan amount
        np.random.random(n_samples) * 0.4         # Random factor for diversity
    )
    
    # Ensure balanced dataset - aim for ~65% approval rate
    df['Loan_Status'] = np.where(approval_prob > 0.45, 'Y', 'N')
    
    # Force balance if needed
    approval_rate = (df['Loan_Status'] == 'Y').mean()
    print(f"📈 Initial approval rate: {approval_rate:.2%}")
    
    if approval_rate < 0.6:
        rejected_indices = df[df['Loan_Status'] == 'N'].index
        n_to_flip = int(len(rejected_indices) * 0.3)
        flip_indices = np.random.choice(rejected_indices, n_to_flip, replace=False)
        df.loc[flip_indices, 'Loan_Status'] = 'Y'
        
    final_approval_rate = (df['Loan_Status'] == 'Y').mean()
    print(f"✅ Final approval rate: {final_approval_rate:.2%}")
    
    return df

def save_datasets(df):
    """Save datasets in different formats"""
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # 1. Complete dataset
    df.to_csv('data/loan_dataset.csv', index=False)
    print(f"💾 Saved complete dataset: data/loan_dataset.csv ({len(df)} records)")
    
    # 2. Training dataset (without Loan_ID for ML)
    training_df = df.drop('Loan_ID', axis=1)
    training_df.to_csv('data/loan_training_data.csv', index=False)
    print(f"🤖 Saved training dataset: data/loan_training_data.csv")
    
    # 3. Sample applications for demo
    sample_df = df.head(20)
    sample_df.to_csv('data/sample_applications.csv', index=False)
    print(f"📋 Saved sample applications: data/sample_applications.csv (20 records)")
    
    # 4. Approved loans only
    approved_df = df[df['Loan_Status'] == 'Y']
    approved_df.to_csv('data/approved_loans.csv', index=False)
    print(f"✅ Saved approved loans: data/approved_loans.csv ({len(approved_df)} records)")
    
    # 5. Rejected loans only
    rejected_df = df[df['Loan_Status'] == 'N']
    rejected_df.to_csv('data/rejected_loans.csv', index=False)
    print(f"❌ Saved rejected loans: data/rejected_loans.csv ({len(rejected_df)} records)")

def create_summary_statistics(df):
    """Create summary statistics CSV"""
    
    print("\n📊 Creating Summary Statistics...")
    
    # Basic statistics
    summary_stats = {
        'Metric': [
            'Total Applications',
            'Approved Applications', 
            'Rejected Applications',
            'Approval Rate',
            'Average Applicant Income',
            'Average Loan Amount',
            'Most Common Property Area',
            'Graduate Percentage',
            'Married Percentage',
            'Good Credit History Percentage'
        ],
        'Value': [
            len(df),
            len(df[df['Loan_Status'] == 'Y']),
            len(df[df['Loan_Status'] == 'N']),
            f"{(df['Loan_Status'] == 'Y').mean():.2%}",
            f"${df['ApplicantIncome'].mean():.0f}",
            f"${df['LoanAmount'].mean():.0f}",
            df['Property_Area'].mode()[0],
            f"{(df['Education'] == 'Graduate').mean():.2%}",
            f"{(df['Married'] == 'Yes').mean():.2%}",
            f"{(df['Credit_History'] == 1).mean():.2%}"
        ]
    }
    
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv('data/dataset_summary.csv', index=False)
    print(f"📈 Saved summary statistics: data/dataset_summary.csv")
    
    return summary_df

def main():
    """Main function to create all datasets"""
    print("🚀 Starting Dataset Creation Process...")
    print("=" * 50)
    
    # Create the main dataset
    df = create_loan_dataset()
    
    # Save in different formats
    save_datasets(df)
    
    # Create summary statistics
    summary_df = create_summary_statistics(df)
    
    print("\n" + "=" * 50)
    print("✅ Dataset Creation Complete!")
    print("\n📁 Files Created:")
    print("   📊 data/loan_dataset.csv - Complete dataset with Loan_ID")
    print("   🤖 data/loan_training_data.csv - Training data (no Loan_ID)")
    print("   📋 data/sample_applications.csv - 20 sample records")
    print("   ✅ data/approved_loans.csv - Approved applications only")
    print("   ❌ data/rejected_loans.csv - Rejected applications only")
    print("   📈 data/dataset_summary.csv - Summary statistics")
    
    print(f"\n🎯 Dataset Overview:")
    print(f"   • Total Records: {len(df)}")
    print(f"   • Approval Rate: {(df['Loan_Status'] == 'Y').mean():.2%}")
    print(f"   • Features: {len(df.columns) - 2} (excluding Loan_ID and Loan_Status)")
    print(f"   • Balanced: ✅ Fair approval rate")
    
    print(f"\n📊 Quick Statistics:")
    print(summary_df.to_string(index=False))

if __name__ == "__main__":
    main()