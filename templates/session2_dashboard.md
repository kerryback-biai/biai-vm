# Session 2: AI vs Dashboards

## Data

Three CSV files for Acme Corp (a mid-size B2B industrial supplier) are in `data/`:

- **sales.csv** — 837 transactions: transaction_id, date, customer_name, product_line, amount, region, sales_rep
- **customers.csv** — 50 customers: customer_id, customer_name, industry, region, acquisition_date, status, annual_contract_value
- **employees.csv** — 30 employees: employee_id, first_name, last_name, department, division, hire_date, role, salary_band

## Exercise 1: Replicate the Dashboard

Type this prompt into Claude Code:

> I have three CSV files in data/ for a company called Acme Corp: sales.csv (transactions), customers.csv (customer info), and employees.csv (workforce data).
>
> Give me a dashboard summary:
> 1. Total revenue by product line (with a chart)
> 2. Revenue by region
> 3. Top 10 customers by total revenue
> 4. Monthly revenue trend for 2024 vs 2025
> 5. Headcount by department
> 6. Key metrics: total revenue, transaction count, avg deal size, active customers, revenue per employee

## Exercise 2: Beyond the Dashboard

Try these questions — type them into the same conversation:

- "Which customers are declining quarter over quarter? Flag any that dropped more than 20%."
- "What is our revenue concentration risk? How much revenue comes from the top 3 customers?"
- "Which product line has the best revenue per sales rep?"
- "Are any of our churned customers showing signs before they left — declining order sizes or fewer transactions?"
- "Compare Q4 2024 to Q4 2025 across all metrics. What got better? What got worse?"

## Exercise 3: Iterate

1. "Change the monthly trend to a stacked area chart showing all three product lines"
2. "Reformat the key metrics as a traffic-light dashboard — green if above median, red if below"
3. "Critique your own work. What would a skeptical CFO question about this analysis?"
4. "Generate a one-page executive summary as a Word document"

## Exercise 4: Verify (Maker/Checker)

Check Claude's work:

- **Assumptions:** "Which customers did you include? Active only, or churned too?"
- **Ambiguity:** "Revenue per employee — did you use total headcount or only sales staff?"
- **Code:** "Show me the code that joins sales to customers. What's the join key?"
- **Spot-check:** "What does the raw sum of the amount column in sales.csv equal?"
