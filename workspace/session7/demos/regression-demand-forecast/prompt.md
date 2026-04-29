# Demo: Regression — Demand Forecasting

## What This Demonstrates
- Regression (predicting a number) vs. classification (predicting a category)
- Same gradient boosting method, different evaluation metrics (MAE, R²)
- Practical application: inventory planning, staffing

## Tool
Claude Code on AI+Code Lab

## Setup
Use the Acme Corp sales data from Session 2:
`../session2/data/sales.csv`

## Prompt

```
Using the sales data at ../session2/data/sales.csv, build a model to forecast monthly revenue:

1. Aggregate sales to monthly totals
2. Create features: month number, quarter, year, lag-1 revenue, lag-2 revenue, rolling 3-month average
3. Train a gradient boosting regressor to predict next month's revenue
4. Show me:
   - Mean Absolute Error and R² on held-out months
   - Actual vs. predicted chart (line plot, both on same axis)
   - Feature importance
5. Predict the next 3 months beyond the data and show the forecast with a confidence band
```

## Key Narration Points
- "Same method — gradient boosting — but now predicting a dollar amount, not yes/no."
- "MAE tells you: on average, how many dollars off is the forecast?"
- "R² tells you: what fraction of the variation does the model explain?"
- "With only 18 months of data, the model may struggle — that's a lesson too."

## Expected Behavior
- With ~18 months of monthly data (18 rows after aggregation), the model will have limited training data
- This is intentional: it demonstrates that ML needs volume, and small datasets may be better served by simpler methods
- Claude may suggest ARIMA or simple moving average as alternatives — that's fine

## Teaching Moment
```
We only have 18 months of data. Is gradient boosting the right method here, or should we use something simpler? What would you recommend for a dataset this small?
```

Expected: Claude recommends simpler time-series methods (ARIMA, exponential smoothing) for small datasets and gradient boosting for larger ones (100+ time periods or rich cross-sectional features).

## Timing
~4 minutes
