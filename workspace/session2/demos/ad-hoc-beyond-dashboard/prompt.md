# Demo: Ad-Hoc Analysis Beyond the Dashboard

## What This Demonstrates
- AI answers questions the dashboard was never designed for
- New analysis code generated on the fly — no pre-built views needed
- The "from BI to AI" transition: any question, not just pre-built ones

## Tool
Claude Code on AI+Code Lab (same session as dashboard replication)

## Prompts (try in sequence)

### Prompt 1: Customer Decline Detection
```
Which customers are declining quarter over quarter? Flag any that dropped more than 20% in spending.
```

### Prompt 2: Revenue Concentration Risk
```
What is our revenue concentration risk? What percentage of total revenue comes from the top 3 customers? The top 5? Show a cumulative concentration curve.
```

### Prompt 3: Cross-File Join
```
Which product line has the best revenue per sales rep? Join sales data with employee data to calculate this.
```

### Prompt 4: Churn Signals (verification exercise)
```
Are any of our churned customers showing declining patterns before they left — shrinking order sizes or fewer transactions per quarter? Show me the evidence.
```

## Key Narration Points
- "This question was never built into any dashboard. No one designed a view for it."
- "Claude Code wrote new analysis code on the fly."
- "For Prompt 4: verify the method carefully. Ask Claude what it defined as 'before they left.'"
- "This is the transition: any question, not just pre-built ones."

## Expected Findings
- Top 3 customers = ~19% of revenue (meaningful concentration)
- Several customers show declining quarterly trends
- Churned customers should show declining order frequency before churn date

## Timing
~3 minutes (pick 1-2 prompts for the live demo; students explore all 4)
