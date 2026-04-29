# Demo: Dashboard Replication

## What This Demonstrates
- Claude Code's evaluate/correct loop (writes code, runs it, fixes errors)
- Replacing a traditional dashboard with AI in minutes
- Real charts from real data — same output, fraction of the time

## Tool
Claude Code on AI+Code Lab (ai-lab.rice-business.org)

## Setup
Data files are at `data/` on the AI Lab:
- sales.csv (837 transactions)
- customers.csv (50 customers)
- employees.csv (30 employees)

## Prompt

```
I have three CSV files in data/ for a company called Acme Corp:
- sales.csv (transactions with date, customer, product_line, amount, region, sales_rep)
- customers.csv (customer info with industry, region, status, contract value)
- employees.csv (workforce with department, division, role, salary_band)

Give me a dashboard summary — save all charts as PNGs:
1. Total revenue by product line (bar chart)
2. Revenue by region (bar chart)
3. Top 10 customers by total revenue (table)
4. Monthly revenue trend, 2024 vs 2025 (line chart)
5. Headcount by department (table)
6. Key metrics: total revenue, transaction count, avg deal size, active customers, revenue per employee
```

## Key Narration Points
- "Watch the evaluate/correct loop. It writes Python, runs it, reads the output..."
- "If there's a missing library or wrong column name, it fixes it automatically."
- "Same six views as the static dashboard. Minutes, not days."
- "Notice: it saved real PNG files. You can put these in a slide deck."

## Expected Output
- ~$10.3M total revenue
- 837 transactions
- Top customer: Apex Manufacturing (~$826K)
- Industrial Products is the largest product line

## Timing
~5 minutes (including Claude Code's execution time)
