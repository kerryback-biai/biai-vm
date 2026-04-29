# Demo: Agent Loop Deconstructed

**Session 4** — What happens behind the scenes when the agent answers a cross-system question.

---

## Step 0: System Prompt (excerpt the agent receives)

Before the user says anything, the agent has already loaded a system prompt describing all 10 enterprise systems. Here is the relevant excerpt:

```
## Enterprise Systems: XYZ Corp

XYZ Corp (~$500M revenue) is a B2B industrial supplies distributor
with 3 operating divisions + corporate HQ. Each division runs its own CRM.

| Division     | Revenue | CRM        | Finance           |
|------------- |---------|------------|-------------------|
| Industrial   | ~$250M  | Salesforce | NetSuite          |
| Energy       | ~$150M  | Legacy CRM | QuickBooks        |
| Safety       | ~$100M  | HubSpot   | (shared NetSuite) |

### System: salesforce (XYZ Industrial CRM)
- sf_accounts: AccountId, AccountName, ...
- sf_orders: OrderId, AccountId, TotalAmount, Status, OrderDate

### System: legacy_crm (XYZ Energy CRM)
- clients: client_id, client_name, ...
- client_orders: order_num, client_id, total, order_dt (VARCHAR MM/DD/YYYY)

### System: hubspot (XYZ Safety CRM)
- hs_companies: company_id, name, ...
- hs_deals: deal_id, company_id, amount, dealstage, closedate

### Cross-System Data Challenges
1. Customer Identity: Same company appears under different names across CRMs.
   No mapping table exists. Use fuzzy string matching.
2. You CANNOT join across systems in a single SQL query.
```

The agent also has two tools:
- `query_database(sql, system)` — runs SQL against one system at a time
- `code_execution` — runs Python for merging and analysis

---

## Step 1: User asks the question

**User:** Which division has the highest customer concentration risk?

---

## Step 2: Agent plans its approach (thinking)

The agent reasons:

> "Customer concentration risk means how much revenue depends on a small number of customers. I need revenue by customer for each division. That data lives in three different CRMs — Salesforce (Industrial), Legacy CRM (Energy), and HubSpot (Safety). I'll query each one separately and then merge the results in Python."

---

## Step 3: Query Salesforce (Industrial Division)

**Agent calls tool:** `query_database`

```sql
SELECT
    a.AccountName,
    SUM(o.TotalAmount) AS total_revenue
FROM sf_orders o
JOIN sf_accounts a ON o.AccountId = a.AccountId
WHERE o.Status != 'Cancelled'
GROUP BY a.AccountName
ORDER BY total_revenue DESC
LIMIT 10
```
**System:** `salesforce`

**Raw result:**

| AccountName              | total_revenue |
|--------------------------|---------------|
| General Electric         | 4,217,832     |
| Parker Hannifin Corp     | 3,891,205     |
| Eaton Corporation        | 3,456,019     |
| Illinois Tool Works      | 3,122,740     |
| Honeywell International  | 2,987,661     |
| Danaher Corporation      | 2,754,103     |
| Stanley Black & Decker   | 2,503,882     |
| Dover Corporation        | 2,341,557     |
| Emerson Electric Co.     | 2,198,034     |
| Rockwell Automation      | 1,987,445     |

Also queries total:

```sql
SELECT SUM(TotalAmount) AS division_total
FROM sf_orders
WHERE Status != 'Cancelled'
```

**Result:** division_total = **63,412,877**

---

## Step 4: Query Legacy CRM (Energy Division)

**Agent calls tool:** `query_database`

```sql
SELECT
    c.client_name,
    SUM(o.total) AS total_revenue
FROM client_orders o
JOIN clients c ON o.client_id = c.client_id
GROUP BY c.client_name
ORDER BY total_revenue DESC
LIMIT 10
```
**System:** `legacy_crm`

**Raw result:**

| client_name               | total_revenue |
|---------------------------|---------------|
| CAT Energy Services       | 12,847,231    |
| Emerson Process Mgmt      | 4,102,556     |
| Honeywell Process Solutions | 3,274,889   |
| Parker Energy Division    | 2,891,345     |
| Roper Pump & Energy       | 2,456,102     |
| Dover Energy              | 2,334,778     |
| Fortive Field Solutions   | 1,987,403     |
| Xylem Water Solutions     | 1,765,221     |
| Watts Energy Systems      | 1,542,667     |
| Hubbell Power Systems     | 1,389,004     |

Total query:

```sql
SELECT SUM(total) AS division_total FROM client_orders
```

**Result:** division_total = **37,891,402**

---

## Step 5: Query HubSpot (Safety Division)

**Agent calls tool:** `query_database`

```sql
SELECT
    c.name,
    SUM(d.amount) AS total_revenue
FROM hs_deals d
JOIN hs_companies c ON d.company_id = c.company_id
WHERE d.dealstage = 'closedwon'
GROUP BY c.name
ORDER BY total_revenue DESC
LIMIT 10
```
**System:** `hubspot`

**Raw result:**

| name                     | total_revenue |
|--------------------------|---------------|
| Honeywell Safety Products| 1,687,234     |
| 3M Safety Solutions      | 1,342,891     |
| Parker Safety Systems    | 1,178,556     |
| GE Safety Division       | 1,045,223     |
| Danaher Safety           | 891,102       |
| Eaton Safety             | 834,667       |
| Dover Safety             | 723,445       |
| Fortive Safety Tech      | 612,334       |
| Graco Safety Equipment   | 534,112       |
| Lincoln Safety Products  | 489,667       |

Total query:

```sql
SELECT SUM(amount) AS division_total
FROM hs_deals
WHERE dealstage = 'closedwon'
```

**Result:** division_total = **12,204,518**

---

## Step 6: Merge and calculate in Python

**Agent calls tool:** `code_execution`

```python
import pandas as pd

# Data from the three queries
industrial = {
    'division': 'Industrial',
    'total_revenue': 63_412_877,
    'top_customer': 'General Electric',
    'top_customer_revenue': 4_217_832,
}
energy = {
    'division': 'Energy',
    'total_revenue': 37_891_402,
    'top_customer': 'CAT Energy Services',
    'top_customer_revenue': 12_847_231,
}
safety = {
    'division': 'Safety',
    'total_revenue': 12_204_518,
    'top_customer': 'Honeywell Safety Products',
    'top_customer_revenue': 1_687_234,
}

df = pd.DataFrame([industrial, energy, safety])
df['concentration_pct'] = (df['top_customer_revenue'] / df['total_revenue'] * 100).round(1)
df = df.sort_values('concentration_pct', ascending=False)

print(df[['division', 'top_customer', 'top_customer_revenue', 'total_revenue', 'concentration_pct']].to_string(index=False))
```

**Output:**

```
 division          top_customer  top_customer_revenue  total_revenue  concentration_pct
   Energy   CAT Energy Services              12847231       37891402               33.9
   Safety Honeywell Safety Prod               1687234       12204518               13.8
Industrial    General Electric               4217832       63412877                6.6
```

---

## Step 7: Agent reviews results and notices the risk

The agent sees that **Energy division's top customer (CAT Energy Services) accounts for 33.9% of division revenue** — far above the other two divisions. It flags this as the key finding.

---

## Step 8: Final answer delivered to user

**Agent:**

> **Energy division has the highest customer concentration risk by a wide margin.**
>
> | Division | Top Customer | Top Customer Revenue | Division Total | Concentration |
> |---|---|---|---|---|
> | **Energy** | CAT Energy Services | $12.8M | $37.9M | **33.9%** |
> | Safety | Honeywell Safety Products | $1.7M | $12.2M | 13.8% |
> | Industrial | General Electric | $4.2M | $63.4M | 6.6% |
>
> **Key finding:** CAT Energy Services represents 34% of the Energy division's total revenue. This is a significant concentration risk — if this single customer were lost, the Energy division would lose one-third of its revenue.
>
> For context, the generally accepted threshold for customer concentration risk is 10%. Energy exceeds this by 3x. Safety is also above the threshold at 14%, while Industrial is well-diversified at 7%.
>
> **Note:** Revenue figures are based on order data from each division's CRM (Salesforce for Industrial, Legacy CRM for Energy, HubSpot for Safety). These may differ slightly from financial system totals due to timing differences and order cancellations.

---

## Summary: What happened behind the scenes

| Step | What the agent did | Tool used |
|---|---|---|
| 1 | Read the system prompt to understand which systems exist | (built-in) |
| 2 | Planned: need revenue by customer from 3 CRMs | (reasoning) |
| 3 | Queried Salesforce for Industrial revenue by customer | `query_database` |
| 4 | Queried Legacy CRM for Energy revenue by customer | `query_database` |
| 5 | Queried HubSpot for Safety revenue by customer | `query_database` |
| 6 | Wrote Python to merge results and compute concentration % | `code_execution` |
| 7 | Reviewed the numbers, spotted the 34% outlier | (reasoning) |
| 8 | Delivered narrative answer with table and context | (text generation) |

**Total tool calls:** 7 (6 queries + 1 code execution)
**Total agent loop rounds:** 4 (plan, query x3, compute, respond)
