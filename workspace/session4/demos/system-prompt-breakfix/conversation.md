# Demo: System Prompt Break/Fix

**Session 4** — Demonstrate that removing join key documentation from the system prompt breaks the agent.

The same question is asked twice: once with the full system prompt, once with cross-system join key documentation removed.

---

# Conversation A: With Full System Prompt (Working)

## System prompt includes:

```
### Cross-System Data Challenges

1. Customer Identity: Same company appears under different names across CRMs.
   No mapping table exists. Use fuzzy string matching.

2. Employee ID Mapping: Use workday.wd_system_ids to map worker_id to CRM
   rep IDs (Salesforce OwnerId, Legacy CRM rep_code, HubSpot owner_id).

3. Account Code Mapping: Use netsuite_corporate.ns_acct_mapping to reconcile
   Industrial's 5-digit codes (40000) with Energy's 4-digit codes (4000)
   for consolidated reporting.
```

## User

Show me revenue and headcount by division.

## Agent (thinking)

> "Revenue by division requires querying each division's financial data. Headcount comes from Workday. I need to:
> 1. Get revenue from each CRM (Salesforce orders for Industrial, Legacy CRM orders for Energy, HubSpot deals for Safety)
> 2. Get headcount from Workday, grouped by division
> 3. Merge them in Python on the division name"

## Agent queries

**Query 1:** Salesforce (Industrial revenue)

```sql
SELECT SUM(TotalAmount) AS revenue
FROM sf_orders
WHERE Status != 'Cancelled'
```
System: `salesforce`

Result: **63,412,877**

**Query 2:** Legacy CRM (Energy revenue)

```sql
SELECT SUM(total) AS revenue
FROM client_orders
```
System: `legacy_crm`

Result: **37,891,402**

**Query 3:** HubSpot (Safety revenue)

```sql
SELECT SUM(amount) AS revenue
FROM hs_deals
WHERE dealstage = 'closedwon'
```
System: `hubspot`

Result: **12,204,518**

**Query 4:** Workday (headcount by division)

```sql
SELECT
    division,
    COUNT(*) AS headcount
FROM wd_workers
WHERE status = 'Active'
GROUP BY division
ORDER BY headcount DESC
```
System: `workday`

Result:

| division   | headcount |
|------------|-----------|
| Industrial | 308       |
| Energy     | 220       |
| Safety     | 106       |
| Corporate  | 71        |

## Agent merges in Python

```python
import pandas as pd

revenue = pd.DataFrame([
    {'division': 'Industrial', 'revenue': 63_412_877},
    {'division': 'Energy', 'revenue': 37_891_402},
    {'division': 'Safety', 'revenue': 12_204_518},
])

headcount = pd.DataFrame([
    {'division': 'Industrial', 'headcount': 308},
    {'division': 'Energy', 'headcount': 220},
    {'division': 'Safety', 'headcount': 106},
    {'division': 'Corporate', 'headcount': 71},
])

merged = revenue.merge(headcount, on='division', how='left')
merged['rev_per_employee'] = (merged['revenue'] / merged['headcount']).round(0).astype(int)

print(merged.to_string(index=False))
```

## Agent response (correct)

> Here is revenue and headcount by division:
>
> | Division | Revenue | Headcount | Revenue per Employee |
> |---|---|---|---|
> | **Industrial** | $63.4M | 308 | $205,886 |
> | **Energy** | $37.9M | 220 | $172,234 |
> | **Safety** | $12.2M | 106 | $115,137 |
>
> Industrial leads in both absolute revenue and efficiency. The Energy division generates solid revenue per head at $172K. Safety has the lowest efficiency, though as the smallest division it may still be scaling.
>
> *Note: Corporate headcount (71 employees) is excluded from division metrics since corporate does not generate direct revenue. Revenue is from CRM order/deal data; headcount is from Workday active employees.*

---

# Conversation B: Without Join Keys (Broken)

## System prompt has been modified — cross-system section removed:

The schema still lists all tables and columns, but the "Cross-System Data Challenges" section and all join key hints have been deleted. No mention of:
- `wd_system_ids` mapping table
- `ns_acct_mapping` for account code reconciliation
- Division-to-CRM mapping
- Which CRM belongs to which division

The division structure table is also removed. The agent just sees a flat list of 10 systems with their tables.

## User

Show me revenue and headcount by division.

## Agent (thinking)

> "Revenue and headcount by division. I see Workday has a division field on wd_workers. For revenue... I need to figure out which system has revenue. I see sf_orders has TotalAmount, legacy_crm has client_orders with a total field, and HubSpot has hs_deals with amount. But I don't see a 'division' column on any of these tables. Let me check the financial systems — NetSuite has ns_transactions and ns_corp_actuals which might have division."

## Agent queries

**Query 1:** Workday (headcount — this works fine)

```sql
SELECT
    division,
    COUNT(*) AS headcount
FROM wd_workers
WHERE status = 'Active'
GROUP BY division
ORDER BY headcount DESC
```
System: `workday`

Result:

| division   | headcount |
|------------|-----------|
| Industrial | 308       |
| Energy     | 220       |
| Safety     | 106       |
| Corporate  | 71        |

**Query 2:** Agent tries NetSuite Corporate for revenue (wrong approach)

```sql
SELECT
    division,
    SUM(amount) AS revenue
FROM ns_corp_actuals
WHERE account_code = 'REV-001'
GROUP BY division
```
System: `netsuite_corporate`

Result:

| division   | revenue    |
|------------|------------|
| Industrial | 81,203,445 |
| Energy     | 48,721,667 |

**Problem:** Only two divisions appear. Safety revenue is missing from ns_corp_actuals because Safety shares NetSuite with Industrial and its revenue is consolidated there. The agent does not know this.

## Agent tries to fill the gap

> "I only see Industrial and Energy in the corporate actuals. Let me check if there's a Safety entry..."

**Query 3:** Check for Safety in corporate actuals

```sql
SELECT DISTINCT division FROM ns_corp_actuals
```
System: `netsuite_corporate`

Result:

| division   |
|------------|
| Industrial |
| Energy     |

**Query 4:** Agent tries HubSpot as a guess

```sql
SELECT SUM(amount) AS revenue FROM hs_deals
```
System: `hubspot`

Result: **17,891,233** (all deals, not just closed-won)

The agent grabs this number but does not filter for `closedwon` deals — it has no schema hint that `dealstage = 'closedwon'` is the correct filter. The prompt just says the column exists.

## Agent response (wrong)

> Here is revenue and headcount by division:
>
> | Division | Revenue | Headcount |
> |---|---|---|
> | Industrial | $81.2M | 308 |
> | Energy | $48.7M | 220 |
> | Safety | $17.9M | 106 |
> | Corporate | — | 71 |
>
> Industrial is the dominant division with $81.2M in revenue and the largest workforce.

### What went wrong

| Issue | Impact |
|---|---|
| Used `ns_corp_actuals` instead of CRM orders | Numbers are budget/accrual figures, not order revenue — different magnitude and meaning |
| Safety revenue pulled from unfiltered HubSpot deals | Includes open, lost, and stalled deals — overstates Safety revenue by ~47% |
| No mention that data comes from different sources | Industrial/Energy from one system, Safety from another — apples to oranges |
| No revenue-per-employee calculation | The agent did not think to compute efficiency because it was focused on just getting the numbers to appear |
| Numbers don't reconcile | $81.2M + $48.7M + $17.9M = $147.8M, but XYZ is a ~$500M company — the agent doesn't flag the mismatch |

### Root cause

Without the join key documentation, the agent:

1. **Did not know which CRM maps to which division** — so it went to the financial consolidation system instead of querying each CRM directly
2. **Did not know to filter HubSpot deals by `closedwon`** — the stage filter was in the schema but the agent had no guidance on what constitutes "revenue"
3. **Could not reconcile the numbers** — it had no mental model of how the 10 systems fit together, so it could not sanity-check its own output
4. **Produced a confident-sounding but misleading answer** — the table looks clean and professional, but every number is wrong

---

## The lesson

The system prompt is not just documentation — it is the agent's understanding of the business. Remove the cross-system mapping instructions and the agent does not produce errors or refuse to answer. It produces **plausible-looking wrong answers**. This is the most dangerous failure mode in enterprise AI.
