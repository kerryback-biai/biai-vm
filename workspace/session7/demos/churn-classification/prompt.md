# Demo: Churn Classification with Gradient Boosting

## What This Demonstrates
- Building a predictive model from plain English instructions
- AI writes all the ML code (XGBoost/LightGBM) — you evaluate the results
- The confusion matrix and what it means for business decisions
- Feature importance: which signals matter most?

## Tool
Claude Code on AI+Code Lab

## Setup
Data at `data/customer_churn.csv` (from the session7 folder)
- 7,043 telecom customers, 21 columns
- Target column: "Churn" (Yes/No), ~26.5% churn rate
- Features: tenure, MonthlyCharges, TotalCharges, Contract, InternetService, OnlineSecurity, TechSupport, etc.

## Prompt

```
I have a customer churn dataset at data/customer_churn.csv.
The target column is "Churn" (Yes = churned, No = stayed).

Build a gradient boosting classifier to predict which customers will churn:
1. Explore the data first — show me dimensions, missing values, and churn distribution
2. Handle any data quality issues (e.g., blank TotalCharges)
3. Encode categorical features and split into train (80%) and test (20%) with stratification
4. Train an XGBoost or LightGBM model
5. Show me:
   - Accuracy, precision, recall, and F1 on the test set
   - The confusion matrix (with labels: predicted vs actual)
   - Top 10 most important features (bar chart)
   - Cross-validation scores (5-fold) to confirm the model isn't overfit
6. Save the feature importance chart as a PNG
```

## Key Narration Points
- "You described what you want in English. Claude wrote all the ML code."
- "Look at the confusion matrix: how many churners did we catch? How many false alarms?"
- "Feature importance tells you WHY the model predicts churn — contract type and tenure are typically top drivers."
- "Cross-validation confirms this isn't just memorizing the training data."

## Expected Results (approximate)
- Accuracy: ~80-83%
- Recall (churn class): ~53-55% (catches about half of churners)
- Precision (churn class): ~66-68%
- F1 (churn): ~59-61%
- Top features: Contract (month-to-month), tenure, MonthlyCharges, InternetService (fiber optic), TotalCharges
- Key pattern: month-to-month contracts churn at ~42% vs 11% for 2-year contracts

## Follow-Up Prompt (Business Translation)
```
Translate this into business terms:
- If we flag everyone the model predicts will churn and offer them a retention discount, how many customers do we contact? How many of those would have stayed anyway (wasted discounts)?
- If the retention discount costs $50 per customer and saves 60% of true churners, and the average monthly revenue per churner is $75/month — what is the annual ROI of this model?
```

## Timing
~5 minutes (model trains fast on 7,043 rows)
