# Demo: Model Evaluation — Is It Trustworthy?

## What This Demonstrates
- How to evaluate whether a model's predictions are actionable
- The precision/recall tradeoff and its business implications
- Threshold tuning: adjusting the decision boundary
- Connecting predictions back to Session 6 (decisions under uncertainty)

## Tool
Claude Code on AI+Code Lab (continuation of churn model)

## Prompts (sequential)

### Prompt 1: Precision-Recall Tradeoff
```
For the churn model we just built:
1. Plot the precision-recall curve
2. Show me what happens at different thresholds:
   - Threshold 0.3: catch more churners but more false alarms
   - Threshold 0.5: balanced (the default)
   - Threshold 0.7: fewer false alarms but miss more churners
3. For each threshold, show: how many flagged, how many true churners caught, how many false alarms
```

### Prompt 2: Business Cost Analysis
```
Assume:
- Retention offer costs $50 per customer
- Average monthly revenue per customer: $75 (i.e., ~$900/year)
- Retention offer saves 60% of true at-risk customers
- False alarms waste $50 (discount given to customer who would have stayed)

For each threshold (0.3, 0.5, 0.7), calculate:
- Total cost of retention campaign
- Revenue saved from retained customers
- Net ROI
- Which threshold maximizes ROI?
```

### Prompt 3: Where the Model Fails
```
Show me the customers where the model is most wrong:
1. Customers predicted to stay (low churn probability) who actually churned — what do they have in common?
2. Customers predicted to churn (high probability) who actually stayed — what's different about them?

These are the model's blind spots. What additional data would help?
```

## Key Narration Points
- "The threshold is a BUSINESS decision, not a statistical one. How much do false alarms cost you?"
- "Prompt 2 connects prediction to Session 6: this IS a tradeoff problem."
- "Prompt 3 reveals blind spots — the model may miss churners who leave for reasons not in the data (competitor poaching, leadership change)."
- "A model is trustworthy when you understand WHERE it fails, not just its average accuracy."

## The Bridge to Session 6
Make this explicit: "Prediction tells you WHAT IS LIKELY. The decision framework from Session 6 tells you WHAT TO DO ABOUT IT. The threshold choice IS a multi-objective tradeoff — minimize wasted discounts vs. maximize saved customers."

## Timing
~4 minutes (pick prompts 1-2 for live demo; prompt 3 for student exercise)
