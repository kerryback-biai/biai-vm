# Demo: Revenue per Employee by Division

## User prompt

> What is revenue per employee by division?

---

## Agent reasoning (visible to class)

**Step 1 — Plan**

This requires two pieces of data:

1. **Revenue by division** — from each division's CRM (three separate systems)
2. **Headcount by division** — from Workday HR (corporate system)

I'll query 2025 revenue from each CRM, then pull headcount from Workday, and merge on division name.

**Step 2 — Query Salesforce CRM for Industrial revenue (2025)**

```sql
-- System: salesforce_crm
SELECT
    'Industrial' AS division,
    SUM(Amount) AS revenue_2025
FROM sf_opportunities
WHERE StageName = 'Closed Won'
  AND CloseDate >= '2025-01-01'
  AND CloseDate < '2026-01-01';
```

*Result: Industrial revenue = $87.3M*

**Step 3 — Query Legacy CRM for Energy revenue (2025)**

```sql
-- System: legacy_crm
SELECT
    'Energy' AS division,
    SUM(OrderTotal) AS revenue_2025
FROM orders
WHERE OrderStatus = 'Complete'
  AND OrderDate >= '01/01/2025'
  AND OrderDate <= '12/31/2025';
```

*Result: Energy revenue = $52.1M*

**Step 4 — Query HubSpot CRM for Safety revenue (2025)**

```sql
-- System: hubspot_crm
SELECT
    'Safety' AS division,
    SUM(deal_amount) AS revenue_2025
FROM hs_deals
WHERE deal_stage = 'closedwon'
  AND close_date >= '2025-01-01'
  AND close_date < '2026-01-01';
```

*Result: Safety revenue = $34.8M*

**Step 5 — Query Workday for headcount by division**

```sql
-- System: workday_hr
SELECT
    department_division AS division,
    COUNT(*) AS headcount
FROM wd_employees
WHERE employment_status = 'Active'
GROUP BY department_division
ORDER BY division;
```

*Result:*

| division | headcount |
|---|---|
| Corporate | 43 |
| Energy | 134 |
| Industrial | 218 |
| Safety | 87 |

**Step 6 — Merge and compute**

```python
import pandas as pd

revenue = pd.DataFrame({
    'division': ['Industrial', 'Energy', 'Safety'],
    'revenue_2025': [87_300_000, 52_100_000, 34_800_000]
})

headcount = pd.DataFrame({
    'division': ['Industrial', 'Energy', 'Safety', 'Corporate'],
    'headcount': [218, 134, 87, 43]
})

# Merge on division (exclude Corporate — no direct revenue)
merged = revenue.merge(headcount, on='division')
merged['rev_per_employee'] = merged['revenue_2025'] / merged['headcount']
merged = merged.sort_values('rev_per_employee', ascending=False)

# Also compute company-wide figure
total_rev = revenue['revenue_2025'].sum()
total_hc = headcount['headcount'].sum()  # includes Corporate
company_wide = total_rev / total_hc
```

*Merge successful. Revenue per employee computed for each division and company-wide.*

---

## Errors / retries

- **Legacy CRM date format:** As with other Legacy CRM queries, dates are stored as VARCHAR. The agent used the `MM/DD/YYYY` format in the WHERE clause. No retry needed this time — the pattern was cached from the prior demo.
- **Corporate headcount question:** The agent considered whether to allocate Corporate's 43 employees across divisions (shared services model) or exclude them. It chose to show both: per-division figures exclude Corporate, and the company-wide figure includes all 482 employees. This decision was noted in the output.
