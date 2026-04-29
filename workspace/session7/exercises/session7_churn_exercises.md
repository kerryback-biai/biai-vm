# Session 7: Predictive Modeling Exercises

## Part 1: Build a Churn Model (20 minutes on Claude.ai)

Upload `data/customer_churn.csv` to Claude.ai and work through these steps:

### Step 1: Explore (2 minutes)
> Explore this data. How many rows? Missing values? What's the churn rate?

Expected: 7,043 customers, 21 columns, 26.5% churn rate, 11 blank TotalCharges.

### Step 2: Build (5 minutes)
> Build a gradient boosting classifier to predict churn. Use an 80/20 train-test split and 5-fold cross-validation.
>
> Show me:
> 1. The confusion matrix on the test set
> 2. Precision, recall, and F1 score
> 3. The top 10 most important features
> 4. Cross-validation scores
>
> Explain the results in business terms, not just statistics.

### Step 3: Evaluate (3 minutes)
> Show me the confusion matrix. What's the false negative rate?

Apply the three-question framework:
- Better than baseline? (baseline = predict "stay" for everyone = 73.5% accuracy)
- Features make sense? (tenure, charges, and contract type should be prominent)
- Generalizes well? (cross-validation close to test accuracy = no overfitting)

### Step 4: Interpret (3 minutes)
> What are the top 10 features? Do they make business sense?

Red flags: if customer ID or row number appears, that's data leakage.

### Step 5: Challenge (5 minutes)
> What would a skeptical VP of Customer Success push back on? What are this model's blind spots? How would you improve it?

### Bonus
> If I could only act on the top 200 highest-risk customers, which ones would you flag and why?

## Part 2: Deploy as Web App (15 minutes on AI Lab)

Open the AI+Code Lab at ai-lab.rice-business.org. Paste this prompt into Claude Code:

> Build a customer churn prediction web app using the data at data/customer_churn.csv. Train a gradient boosting model on the telecom churn dataset. The app should let a user enter customer attributes and get a churn probability with the top 3 risk factors.

Then:
1. Run the app and test with different customer profiles
2. *Stretch goal:* "Add a batch mode that reads a CSV and flags all customers above 70% churn risk"

## Breakout: Prediction Opportunities (5 minutes)

Each person shares (1 minute):
1. What would you predict? (be specific)
2. What data would you need? Do you have it?
3. What would you DO with the predictions? Who acts on them?
