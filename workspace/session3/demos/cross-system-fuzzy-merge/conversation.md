# Demo: Cross-System Customer Merge

## User prompt

> Which customers buy from multiple divisions?

---

## Agent reasoning (visible to class)

**Step 1 — Plan**

To answer this, I need to pull customer lists from all three division CRMs and then match them. Each division uses a different CRM system, so I'll query each one separately.

- **Industrial** — Salesforce CRM
- **Energy** — Legacy CRM (custom-built)
- **Safety** — HubSpot CRM

**Step 2 — Query Salesforce CRM (Industrial Division)**

```sql
-- System: salesforce_crm
SELECT
    AccountId,
    AccountName,
    Industry,
    SUM(Amount) AS total_revenue
FROM sf_opportunities
WHERE StageName = 'Closed Won'
  AND CloseDate >= '2023-01-01'
GROUP BY AccountId, AccountName, Industry
ORDER BY total_revenue DESC;
```

*Result: 47 customer accounts, $248.7M total revenue.*

**Step 3 — Query Legacy CRM (Energy Division)**

```sql
-- System: legacy_crm
SELECT
    CustID,
    CustName,
    SUM(OrderTotal) AS total_revenue
FROM orders
WHERE OrderStatus = 'Complete'
  AND OrderDate >= '01/01/2023'
GROUP BY CustID, CustName
ORDER BY total_revenue DESC;
```

*Result: 31 customer accounts, $147.2M total revenue.*

Note: Legacy CRM stores dates as VARCHAR in MM/DD/YYYY format. The agent adjusted the date filter accordingly.

**Step 4 — Query HubSpot CRM (Safety Division)**

```sql
-- System: hubspot_crm
SELECT
    company_id,
    company_name,
    SUM(deal_amount) AS total_revenue
FROM hs_deals
WHERE deal_stage = 'closedwon'
  AND close_date >= '2023-01-01'
GROUP BY company_id, company_name
ORDER BY total_revenue DESC;
```

*Result: 28 customer accounts, $98.4M total revenue.*

**Step 5 — Attempt exact matching**

I'll first try exact name matching across all three customer lists.

```python
import pandas as pd

industrial = pd.DataFrame(sf_results)
energy = pd.DataFrame(legacy_results)
safety = pd.DataFrame(hubspot_results)

# Normalize column names
industrial = industrial.rename(columns={'AccountName': 'name'})
energy = energy.rename(columns={'CustName': 'name'})
safety = safety.rename(columns={'company_name': 'name'})

# Exact match across systems
all_names = set(industrial['name']) | set(energy['name']) | set(safety['name'])
exact_matches = []
for name in all_names:
    divisions = []
    if name in set(industrial['name']): divisions.append('Industrial')
    if name in set(energy['name']): divisions.append('Energy')
    if name in set(safety['name']): divisions.append('Safety')
    if len(divisions) >= 2:
        exact_matches.append((name, divisions))

print(f"Exact matches found: {len(exact_matches)}")
```

*Result: Only 3 exact matches found.* That seems low — many companies are likely recorded under slightly different names in each system. Let me try fuzzy matching.

**Step 6 — Fuzzy matching**

```python
from thefuzz import fuzz, process

# Build candidate pairs across systems
threshold = 82

matches = []
for ind_name in industrial['name']:
    for eng_name in energy['name']:
        score = fuzz.token_sort_ratio(ind_name.lower(), eng_name.lower())
        if score >= threshold:
            matches.append({
                'industrial_name': ind_name,
                'energy_name': eng_name,
                'score': score
            })
    for saf_name in safety['name']:
        score = fuzz.token_sort_ratio(ind_name.lower(), saf_name.lower())
        if score >= threshold:
            matches.append({
                'industrial_name': ind_name,
                'safety_name': saf_name,
                'score': score
            })

for eng_name in energy['name']:
    for saf_name in safety['name']:
        score = fuzz.token_sort_ratio(eng_name.lower(), saf_name.lower())
        if score >= threshold:
            matches.append({
                'energy_name': eng_name,
                'safety_name': saf_name,
                'score': score
            })

# Deduplicate and group into clusters
```

*Fuzzy matching identified 10 customer clusters appearing in 2+ divisions.*

**Step 7 — Merge revenue by matched customer**

The agent consolidated fuzzy-matched names into canonical customer names and summed revenue across divisions. Two matches were flagged as uncertain (score between 82 and 85) and manually verified against address and industry fields.

---

## Errors / retries

- **Date format mismatch:** The first Legacy CRM query used ISO date format (`2023-01-01`) and returned 0 rows. The agent detected the empty result, checked the schema, found `OrderDate VARCHAR(10)` with sample value `01/15/2023`, and rewrote the filter as `OrderDate >= '01/01/2023'`.
- **Fuzzy false positive:** "National Oilwell Varco" (Energy) initially matched "National Safety Supply" (Safety) at score 83. The agent cross-checked industry fields (Oil & Gas vs. PPE Distribution) and excluded the match.
