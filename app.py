import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time as time_module
import requests

# Set page configpwd
st.set_page_config(
    page_title="Credit Card Fraud Detection 💳",
    page_icon="🔒",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .fraud-alert {
        padding: 20px;
        border-radius: 10px;
        background-color: #ff4b4b;
        color: white;
    }
    .safe-alert {
        padding: 20px;
        border-radius: 10px;
        background-color: #00cc00;
        color: white;
    }
    .warning-alert {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffa500;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def create_synthetic_data():
    # Load the actual credit card data
    df = pd.read_csv('creditcard.csv')
    
    # Convert Time to hours (assuming Time is in seconds)
    df['Time_of_Day'] = (df['Time'] % 86400) / 3600  # Convert seconds to hours
    
    # Create more sophisticated features
    df['Distance_from_Home'] = abs(df['V1'] * 50)  # Scale V1 to create distance-like values
    df['Transaction_Velocity'] = df['Amount'] / (df['Time'] + 1)  # Amount per second
    df['Transaction_Frequency'] = df.groupby('Time')['Time'].transform('count')
    df['Amount_Deviation'] = (df['Amount'] - df['Amount'].mean()) / df['Amount'].std()
    
    # Create time-based features
    df['Is_Night'] = (df['Time_of_Day'] < 6) | (df['Time_of_Day'] > 22)
    df['Is_Weekend'] = (df['Time'] % 7) >= 5  # Assuming Time starts from Monday
    
   
    
    # Rename Amount to Transaction_Amount
    df['Transaction_Amount'] = df['Amount']
    
    # Add timestamp
    df['Timestamp'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(df['Time'], unit='s')
    df['Transaction_Date'] = df['Timestamp'].dt.date
    
    # Select and reorder columns
    features = ['Transaction_Amount', 'Distance_from_Home', 'Time_of_Day', 
                'Transaction_Frequency', 'Transaction_Velocity', 'Amount_Deviation',
                'Is_Night', 'Is_Weekend', 'Merchant_Category', 'Class', 'Timestamp', 'Transaction_Date']
    
    return df[features]

def create_visualizations(df):
    # 1. Amount Distribution
    fig_amount = px.histogram(
        df, 
        x='Transaction_Amount',
        color='Class',
        nbins=50,
        title='Distribution of Transaction Amounts',
        color_discrete_map={0: 'blue', 1: 'red'},
        labels={'Class': 'Transaction Type', 'Transaction_Amount': 'Amount ($)'}
    )
    fig_amount.update_layout(bargap=0.1)
    
    # 2. Time of Day Pattern
    fig_time = px.scatter(
        df,
        x='Time_of_Day',
        y='Transaction_Amount',
        color='Class',
        title='Transaction Patterns by Time of Day',
        color_discrete_map={0: 'blue', 1: 'red'},
        labels={'Class': 'Transaction Type', 'Time_of_Day': 'Hour of Day', 'Transaction_Amount': 'Amount ($)'}
    )
    
    # 3. Distance vs Amount
    fig_distance = px.scatter(
        df,
        x='Distance_from_Home',
        y='Transaction_Amount',
        color='Class',
        title='Transaction Amount vs Distance from Home',
        color_discrete_map={0: 'blue', 1: 'red'},
        labels={'Class': 'Transaction Type', 'Distance_from_Home': 'Distance (miles)', 'Transaction_Amount': 'Amount ($)'}
    )
    
    # 4. Fraud Trend Over Time
    daily_fraud = df[df['Class']==1].groupby('Transaction_Date').size().reset_index()
    daily_fraud.columns = ['Date', 'Fraud_Count']
    fig_trend = px.line(
        daily_fraud,
        x='Date',
        y='Fraud_Count',
        title='Daily Fraud Transactions',
        labels={'Fraud_Count': 'Number of Fraudulent Transactions', 'Date': 'Date'}
    )
    
    return fig_amount, fig_time, fig_distance, fig_trend

def train_or_load_model():
    model_path = 'fraud_model_improved.joblib'
    scaler_path = 'scaler_improved.joblib'
    encoder_path = 'encoder_improved.joblib'
    
    # Create and prepare data
    df = create_synthetic_data()
    
    # Split features and target
    # Exclude Timestamp and Transaction_Date as they are not features for the model
    X = df.drop(['Class', 'Timestamp', 'Transaction_Date'], axis=1)
    y = df['Class']
    
    # Identify categorical and numerical features
    categorical_features = ['Merchant_Category']
    numerical_features = X.select_dtypes(include=np.number).columns.tolist()
    numerical_features.remove('Time_of_Day') # Keep Time_of_Day separate for now, or include it?
    # Let's assume Time_of_Day and other numerical features are fine as is initially for scaling
    numerical_features = ['Transaction_Amount', 'Distance_from_Home', 'Time_of_Day', 
                          'Transaction_Frequency', 'Transaction_Velocity', 'Amount_Deviation']

    # Create a column transformer for preprocessing
    # Apply OneHotEncoder to categorical features and RobustScaler to numerical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', RobustScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough') # Keep other columns (like Is_Night, Is_Weekend) as is

    # Create a pipeline that first preprocesses and then trains the model
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('classifier', RandomForestClassifier(
                                         n_estimators=100,
                                         max_depth=10,
                                         min_samples_split=5,
                                         class_weight={0:1, 1:10},
                                         random_state=42
                                     ))])

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train the pipeline
    model_pipeline.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model_pipeline.predict(X_test)
    st.sidebar.write("### Model Performance")
    st.sidebar.write(classification_report(y_test, y_pred))
    
    # Save the trained pipeline
    joblib.dump(model_pipeline, model_path)
    
    # We also need to save the fitted preprocessor to use it for individual predictions
    joblib.dump(preprocessor, 'preprocessor_improved.joblib')
    
    return model_pipeline, preprocessor, df

def calculate_risk_score(transaction_data, model_pipeline, preprocessor):
    # Prepare input data as a Pandas DataFrame to work with ColumnTransformer
    input_df = pd.DataFrame([{
        'Transaction_Amount': transaction_data['amount'],
        'Distance_from_Home': transaction_data['distance'],
        'Time_of_Day': transaction_data['time'],
        'Transaction_Frequency': transaction_data['frequency'],
        'Transaction_Velocity': transaction_data['amount'] / (transaction_data['time'] + 1),  # Transaction velocity
        'Amount_Deviation': (transaction_data['amount'] - 100) / 50,  # Amount deviation (assuming mean=100, std=50)
        'Is_Night': int(transaction_data['time'] < 6 or transaction_data['time'] > 22),  # Is night
        'Is_Weekend': int(False),  # Is weekend (assuming we don't have this info)
        'Merchant_Category': transaction_data['merchant_category']  # Merchant category
    }])
    
    # Preprocess the input data using the fitted preprocessor
    input_processed = preprocessor.transform(input_df)
    
    # Predict probability using the trained model pipeline
    probability = model_pipeline.predict_proba(input_processed)[0][1]
    
    # Calculate risk factors
    risk_factors = []
    risk_score = 0
    
    # Amount risk
    if transaction_data['amount'] > 1000:
        risk_factors.append("High transaction amount (>$1000)")
        risk_score += 0.3
    elif transaction_data['amount'] > 500:
        risk_factors.append("Moderate transaction amount (>$500)")
        risk_score += 0.15
    
    # Distance risk
    if transaction_data['distance'] > 100:
        risk_factors.append("Transaction far from home (>100 miles)")
        risk_score += 0.2
    elif transaction_data['distance'] > 50:
        risk_factors.append("Transaction moderately far from home (>50 miles)")
        risk_score += 0.1
    
    # Time risk
    if transaction_data['time'] < 6 or transaction_data['time'] > 22:
        risk_factors.append("Unusual transaction time (outside 6 AM - 10 PM)")
        risk_score += 0.2
    
    # Frequency risk
    if transaction_data['frequency'] > 10:
        risk_factors.append("Very high transaction frequency (>10 in 24h)")
        risk_score += 0.3
    elif transaction_data['frequency'] > 5:
        risk_factors.append("High transaction frequency (>5 in 24h)")
        risk_score += 0.15
    
    # Merchant category risk
    high_risk_merchants = ['Online', 'Travel']
    medium_risk_merchants = ['Entertainment']
    
    if transaction_data['merchant_category'] in high_risk_merchants:
        risk_factors.append(f"High-risk merchant category: {transaction_data['merchant_category']}")
        risk_score += 0.2
    elif transaction_data['merchant_category'] in medium_risk_merchants:
        risk_factors.append(f"Medium-risk merchant category: {transaction_data['merchant_category']}")
        risk_score += 0.1
    
    # Combine model probability with risk factors
    final_score = (probability * 0.7) + (risk_score * 0.3)
    
    return final_score, risk_factors

def create_gauge_chart(score, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    return fig

def main():
    st.title("Credit Card Fraud Detection System🏦")
    st.markdown("### 🛡 Protect Your Transactions")
    
    # Sidebar
    st.sidebar.header("ℹ About")
    st.sidebar.info(
        "This application uses machine learning to detect potentially fraudulent "
        "credit card transactions. Enter your transaction details to check if "
        "it's safe! 🔒"
    )
    
    # Create tabs
    tab1, tab2 = st.tabs(["Transaction Check", "Analytics Dashboard"])
    
    with tab1:
        st.write("### 📝 Enter Transaction Details")
        
        # Input fields
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Transaction Amount ($)", value=5000.0, min_value=0.0)
            distance = st.number_input("Distance from Home (miles)", value=100.0, min_value=0.0)
            merchant_category = st.selectbox(
                "Merchant Category",
                ['Retail', 'Restaurant', 'Travel', 'Entertainment', 'Gas', 'Online', 'Other']
            )
        
        with col2:
            time = st.number_input("Time of Day (24h format)", value=12.0, min_value=0.0, max_value=24.0)
            frequency = st.number_input("Transactions in Last 24h", value=10.0, min_value=0.0)

        # Check transaction button
        if st.button("🔍 Check Transaction"):
            try:
                # Load model and preprocessor
                # Check if model and preprocessor files exist
                model_path = 'fraud_model_improved.joblib'
                preprocessor_path = 'preprocessor_improved.joblib'
                
                if os.path.exists(model_path) and os.path.exists(preprocessor_path):
                    st.sidebar.write("Loading existing model and preprocessor...")
                    model_pipeline = joblib.load(model_path)
                    preprocessor = joblib.load(preprocessor_path)
                    # Load data for analytics tab only if needed later
                    df = create_synthetic_data() # Still need data for analytics tab
                else:
                    st.sidebar.write("Training new model and preprocessor...")
                    model_pipeline, preprocessor, df = train_or_load_model()
                
                # Prepare transaction data
                transaction_data = {
                    'amount': amount,
                    'distance': distance,
                    'time': time,
                    'frequency': frequency,
                    'merchant_category': merchant_category
                }
                
                # Calculate risk score and factors
                risk_score, risk_factors = calculate_risk_score(transaction_data, model_pipeline, preprocessor)
                
                # Display result
                st.write("### 🔍 Analysis Result")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if risk_score > 0.7:
                        st.markdown(
                            """
                            <div class='fraud-alert'>
                                ⚠ <b>High Risk - Potential Fraud Detected!</b><br>
                                This transaction shows multiple patterns of fraudulent activities.
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    elif risk_score > 0.4:
                        st.markdown(
                            """
                            <div class='warning-alert'>
                                ⚠ <b>Medium Risk - Suspicious Transaction</b><br>
                                This transaction shows some patterns that require attention.
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            """
                            <div class='safe-alert'>
                                ✅ <b>Low Risk - Transaction Appears Safe</b><br>
                                Our analysis suggests this is a legitimate transaction.
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    if risk_factors:
                        st.write("### ⚠ Risk Factors Identified:")
                        for factor in risk_factors:
                            st.write(f"- {factor}")
                
                with col2:
                    # Create gauge chart
                    fig = create_gauge_chart(
                        risk_score,
                        "Risk Score"
                    )
                    st.plotly_chart(fig)
                
                # Transaction details
                st.write("### 📋 Transaction Details")
                st.write(f"Transaction ID: {int(time_module.time())}")
                st.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"Model Confidence: {risk_score:.2%}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with tab2:
        st.write("### 📊 Transaction Analytics")
        
        try:
            # Get the data
            _, _, df = train_or_load_model()
            
            # Create visualizations
            fig_amount, fig_time, fig_distance, fig_trend = create_visualizations(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_amount)
                st.plotly_chart(fig_distance)
            
            with col2:
                st.plotly_chart(fig_time)
                st.plotly_chart(fig_trend)
                
        except Exception as e:
            st.error(f"Unable to load analytics data: {str(e)}")

if __name__ == "__main__":
    main()