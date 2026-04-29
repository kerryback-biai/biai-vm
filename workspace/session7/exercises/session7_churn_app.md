# Session 7: Churn Prediction Web App

## Overview

Build a customer churn prediction web app using Claude Code. The app trains a gradient boosting model on telecom customer data and lets a user enter customer attributes to get a churn probability with the top risk factors.

## Data

`data/customer_churn.csv` — 7,043 telecom customers with 21 columns:

- **customerID** — unique identifier
- **Demographics:** gender, SeniorCitizen, Partner, Dependents
- **Account:** tenure, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges
- **Services:** PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies
- **Target:** Churn (Yes/No) — 26.5% churn rate

## Exercise

Paste this prompt into Claude Code:

> Build a customer churn prediction web app using the data at data/customer_churn.csv. Train a gradient boosting model on the telecom churn dataset. The app should let a user enter customer attributes and get a churn probability with the top 3 risk factors.

Then:

1. **Run the app** and test it with different customer profiles
2. **Stretch goal:** "Add a batch mode that reads a CSV and flags all customers above 70% churn risk"

## What to Explore

- Try a month-to-month customer with high monthly charges and short tenure — high churn risk
- Try a 2-year contract customer with long tenure — low churn risk
- Ask Claude: "What are the most common profiles of customers who churn?"
