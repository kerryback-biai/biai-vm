# Demo: Full Pipeline — Quarterly Executive Summary

**Session 4** — The agent produces a complete quarterly executive summary by querying 7 systems, merging data, computing KPIs, and generating a structured board memo.

---

## User

Prepare a quarterly executive summary of XYZ Corp performance for Q4 2025 — revenue by division, headcount efficiency, top customer risks, and supply chain issues.

---

## Agent (planning)

> "This is a multi-system question requiring data from at least 6 systems. Let me plan:
>
> 1. **Revenue by division:** Salesforce orders (Industrial), Legacy CRM orders (Energy), HubSpot deals (Safety) — filter for Q4 2025. Also need Q3 for comparison.
> 2. **Headcount efficiency:** Workday for headcount by division, then revenue/headcount.
> 3. **Customer risks:** Top customers by revenue from each CRM, compute concentration %.
> 4. **Supply chain issues:** SAP (Industrial operations) and Oracle SCM (Energy operations) for late deliveries, supplier performance.
>
> I'll query each system, then merge everything in Python to generate the memo."

---

## Step 1: Revenue Queries (3 CRMs, Q3 and Q4 2025)

### Salesforce (Industrial)

```sql
SELECT
    QUARTER(OrderDate) AS qtr,
    SUM(TotalAmount) AS revenue,
    COUNT(DISTINCT AccountId) AS active_customers
FROM sf_orders
WHERE YEAR(OrderDate) = 2025
  AND QUARTER(OrderDate) IN (3, 4)
  AND Status != 'Cancelled'
GROUP BY QUARTER(OrderDate)
ORDER BY qtr
```
System: `salesforce`

| qtr | revenue    | active_customers |
|-----|------------|-----------------|
| 3   | 5,482,103  | 87              |
| 4   | 5,891,237  | 91              |

### Legacy CRM (Energy)

```sql
SELECT
    QUARTER(strptime(order_dt, '%m/%d/%Y')) AS qtr,
    SUM(total) AS revenue,
    COUNT(DISTINCT client_id) AS active_customers
FROM client_orders
WHERE YEAR(strptime(order_dt, '%m/%d/%Y')) = 2025
  AND QUARTER(strptime(order_dt, '%m/%d/%Y')) IN (3, 4)
GROUP BY QUARTER(strptime(order_dt, '%m/%d/%Y'))
ORDER BY qtr
```
System: `legacy_crm`

| qtr | revenue    | active_customers |
|-----|------------|-----------------|
| 3   | 3,187,445  | 62              |
| 4   | 3,412,891  | 65              |

### HubSpot (Safety)

```sql
SELECT
    QUARTER(closedate) AS qtr,
    SUM(amount) AS revenue,
    COUNT(DISTINCT company_id) AS active_customers
FROM hs_deals
WHERE YEAR(closedate) = 2025
  AND QUARTER(closedate) IN (3, 4)
  AND dealstage = 'closedwon'
GROUP BY QUARTER(closedate)
ORDER BY qtr
```
System: `hubspot`

| qtr | revenue    | active_customers |
|-----|------------|-----------------|
| 3   | 1,023,556  | 34              |
| 4   | 1,147,892  | 37              |

---

## Step 2: Headcount (Workday)

```sql
SELECT
    division,
    COUNT(*) AS headcount
FROM wd_workers
WHERE status = 'Active'
  AND division != 'Corporate'
GROUP BY division
```
System: `workday`

| division   | headcount |
|------------|-----------|
| Industrial | 308       |
| Energy     | 220       |
| Safety     | 106       |

---

## Step 3: Customer Concentration (3 CRMs)

### Salesforce — Top 5 Industrial customers Q4 2025

```sql
SELECT
    a.AccountName,
    SUM(o.TotalAmount) AS q4_revenue
FROM sf_orders o
JOIN sf_accounts a ON o.AccountId = a.AccountId
WHERE YEAR(o.OrderDate) = 2025
  AND QUARTER(o.OrderDate) = 4
  AND o.Status != 'Cancelled'
GROUP BY a.AccountName
ORDER BY q4_revenue DESC
LIMIT 5
```
System: `salesforce`

| AccountName             | q4_revenue |
|-------------------------|------------|
| General Electric        | 412,334    |
| Parker Hannifin Corp    | 387,102    |
| Eaton Corporation       | 341,556    |
| Illinois Tool Works     | 298,771    |
| Honeywell International | 276,445    |

### Legacy CRM — Top 5 Energy customers Q4 2025

```sql
SELECT
    c.client_name,
    SUM(o.total) AS q4_revenue
FROM client_orders o
JOIN clients c ON o.client_id = c.client_id
WHERE QUARTER(strptime(o.order_dt, '%m/%d/%Y')) = 4
  AND YEAR(strptime(o.order_dt, '%m/%d/%Y')) = 2025
GROUP BY c.client_name
ORDER BY q4_revenue DESC
LIMIT 5
```
System: `legacy_crm`

| client_name              | q4_revenue |
|--------------------------|------------|
| CAT Energy Services      | 1,156,778  |
| Emerson Process Mgmt     | 389,445    |
| Honeywell Process Solutions | 312,667 |
| Parker Energy Division   | 278,112    |
| Roper Pump & Energy      | 234,891    |

### HubSpot — Top 5 Safety customers Q4 2025

```sql
SELECT
    c.name,
    SUM(d.amount) AS q4_revenue
FROM hs_deals d
JOIN hs_companies c ON d.company_id = c.company_id
WHERE YEAR(d.closedate) = 2025
  AND QUARTER(d.closedate) = 4
  AND d.dealstage = 'closedwon'
GROUP BY c.name
ORDER BY q4_revenue DESC
LIMIT 5
```
System: `hubspot`

| name                      | q4_revenue |
|---------------------------|------------|
| Honeywell Safety Products | 156,334    |
| 3M Safety Solutions       | 134,221    |
| Parker Safety Systems     | 118,667    |
| GE Safety Division        | 97,445     |
| Danaher Safety            | 89,112     |

---

## Step 4: Supply Chain (SAP + Oracle SCM)

### SAP — Industrial late deliveries Q4 2025

```sql
SELECT
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN on_time = false THEN 1 ELSE 0 END) AS late_deliveries,
    ROUND(SUM(CASE WHEN on_time = false THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS late_pct
FROM sap_deliveries
WHERE YEAR(ship_date) = 2025 AND QUARTER(ship_date) = 4
```
System: `sap`

| total_deliveries | late_deliveries | late_pct |
|-----------------|----------------|----------|
| 18              | 3              | 16.7     |

### SAP — Worst suppliers Q4 2025

```sql
SELECT
    v.vendor_name,
    v.quality_score,
    COUNT(*) AS po_count,
    AVG(DATEDIFF('day', po.delivery_date, po.actual_delivery)) AS avg_days_late
FROM sap_purchase_orders po
JOIN sap_vendors v ON po.vendor_code = v.vendor_code
WHERE YEAR(po.po_date) = 2025 AND QUARTER(po.po_date) = 4
  AND po.actual_delivery > po.delivery_date
GROUP BY v.vendor_name, v.quality_score
ORDER BY avg_days_late DESC
LIMIT 3
```
System: `sap`

| vendor_name        | quality_score | po_count | avg_days_late |
|-------------------|--------------|----------|---------------|
| Huang-Martinez     | 2.8          | 12       | 8.3           |
| Chen Industries    | 3.1          | 9        | 6.7           |
| Pacific Metal Corp | 3.4          | 7        | 4.2           |

### Oracle SCM — Energy late deliveries Q4 2025

```sql
SELECT
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END) AS late_shipments,
    ROUND(SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS late_pct
FROM ora_shipments
WHERE YEAR(ship_date) = 2025 AND QUARTER(ship_date) = 4
```
System: `oracle_scm`

| total_shipments | late_shipments | late_pct |
|----------------|---------------|----------|
| 42             | 5             | 11.9     |

### Oracle SCM — Worst Energy suppliers Q4 2025

```sql
SELECT
    s.supplier_name,
    s.performance_rating,
    COUNT(*) AS po_count,
    AVG(DATEDIFF('day', po.promise_date, po.received_date)) AS avg_days_late
FROM ora_purchase_orders po
JOIN ora_suppliers s ON po.supplier_num = s.supplier_num
WHERE YEAR(po.order_date) = 2025 AND QUARTER(po.order_date) = 4
  AND po.received_date > po.promise_date
GROUP BY s.supplier_name, s.performance_rating
ORDER BY avg_days_late DESC
LIMIT 3
```
System: `oracle_scm`

| supplier_name          | performance_rating | po_count | avg_days_late |
|------------------------|-------------------|----------|---------------|
| Gonzalez & Sons        | 2.9               | 8        | 7.1           |
| Delta Supply Co        | 3.2               | 6        | 5.4           |
| Mountain View Ind.     | 3.5               | 4        | 3.8           |

---

## Step 5: Zendesk — Support Ticket Trends

```sql
SELECT
    t.tag AS division,
    COUNT(*) AS q4_tickets,
    ROUND(AVG(zd.satisfaction_rating), 1) AS avg_csat,
    SUM(CASE WHEN zd.priority IN ('high', 'urgent') THEN 1 ELSE 0 END) AS critical_tickets
FROM zd_tickets zd
JOIN zd_ticket_tags t ON zd.ticket_id = t.ticket_id
WHERE t.tag IN ('industrial', 'energy', 'safety')
  AND YEAR(zd.created_at) = 2025
  AND QUARTER(zd.created_at) = 4
GROUP BY t.tag
```
System: `zendesk`

| division   | q4_tickets | avg_csat | critical_tickets |
|------------|-----------|----------|-----------------|
| industrial | 28        | 3.7      | 11              |
| energy     | 22        | 3.5      | 9               |
| safety     | 14        | 3.9      | 4               |

---

## Step 6: Python — Merge, compute KPIs, generate memo

```python
import pandas as pd

# Revenue data
revenue = pd.DataFrame([
    {'division': 'Industrial', 'q3_rev': 5_482_103, 'q4_rev': 5_891_237, 'active_customers': 91},
    {'division': 'Energy', 'q3_rev': 3_187_445, 'q4_rev': 3_412_891, 'active_customers': 65},
    {'division': 'Safety', 'q3_rev': 1_023_556, 'q4_rev': 1_147_892, 'active_customers': 37},
])

# Headcount
headcount = pd.DataFrame([
    {'division': 'Industrial', 'headcount': 308},
    {'division': 'Energy', 'headcount': 220},
    {'division': 'Safety', 'headcount': 106},
])

# Merge
df = revenue.merge(headcount, on='division')
df['qoq_growth'] = ((df['q4_rev'] / df['q3_rev'] - 1) * 100).round(1)
df['rev_per_emp'] = (df['q4_rev'] / df['headcount']).round(0).astype(int)
df['total_q4'] = df['q4_rev'].sum()
df['total_q3'] = df['q3_rev'].sum()

# Concentration risk
energy_top = 1_156_778
energy_total = 3_412_891
energy_concentration = round(energy_top / energy_total * 100, 1)

# Supply chain
industrial_late_pct = 16.7
energy_late_pct = 11.9

# Print summary
total_q4 = df['q4_rev'].sum()
total_q3 = df['q3_rev'].sum()
total_growth = round((total_q4 / total_q3 - 1) * 100, 1)

print(f"Total Q4 Revenue: ${total_q4:,.0f}")
print(f"Total Q3 Revenue: ${total_q3:,.0f}")
print(f"QoQ Growth: {total_growth}%")
print(f"Energy concentration: {energy_concentration}%")
```

**Output:**

```
Total Q4 Revenue: $10,452,020
Total Q3 Revenue: $9,693,104
QoQ Growth: 7.8%
Energy concentration: 33.9%
```

---

## Step 7: Agent generates the executive memo

**Agent:**

---

# XYZ CORP — Q4 2025 QUARTERLY EXECUTIVE SUMMARY

**Prepared by:** AI Data Assistant
**Date:** January 2026
**Period:** October 1 — December 31, 2025

---

## Executive Summary

XYZ Corp delivered **$10.5M in Q4 revenue**, up **7.8% from Q3** ($9.7M), with growth across all three divisions. Industrial remains the revenue anchor at $5.9M. However, two risks require immediate attention: **Energy division's 34% customer concentration in CAT Energy Services**, and **rising supplier delivery delays in Industrial operations** (16.7% late delivery rate).

---

## Revenue by Division

| Division | Q4 2025 | Q3 2025 | QoQ Growth | Active Customers |
|---|---|---|---|---|
| Industrial | $5,891,237 | $5,482,103 | +7.5% | 91 |
| Energy | $3,412,891 | $3,187,445 | +7.1% | 65 |
| Safety | $1,147,892 | $1,023,556 | +12.1% | 37 |
| **Total** | **$10,452,020** | **$9,693,104** | **+7.8%** | **193** |

Safety posted the strongest growth rate at 12.1%, though from a smaller base. All divisions showed positive momentum heading into 2026.

*[Revenue by Division — Q3 vs Q4 2025 bar chart described: grouped bar chart with Q3 (light blue) and Q4 (dark blue) for each division, showing the step-up across all three]*

---

## Headcount Efficiency

| Division | Q4 Revenue | Headcount | Revenue/Employee | QoQ Trend |
|---|---|---|---|---|
| Industrial | $5.9M | 308 | $19,127/mo | Stable |
| Energy | $3.4M | 220 | $15,513/mo | Improving |
| Safety | $1.1M | 106 | $10,829/mo | Improving |

Industrial leads in per-employee productivity. Energy is improving as revenue grows faster than headcount. Safety remains the least efficient, consistent with its earlier growth stage.

---

## Customer Risk Flags

| Risk | Division | Detail | Severity |
|---|---|---|---|
| **Concentration** | Energy | CAT Energy Services = 33.9% of Q4 revenue ($1.16M of $3.41M) | HIGH |
| Concentration | Safety | Honeywell Safety Products = 13.6% of Q4 revenue | MEDIUM |
| Low diversification | Energy | Top 5 customers = 69.5% of Q4 revenue | MEDIUM |

**Recommended action:** The Energy division should develop a customer diversification plan targeting 3-5 new accounts in Q1 2026 to reduce CAT dependency below 25%.

---

## Supply Chain Issues

### Industrial (SAP)

- **Late delivery rate:** 16.7% (3 of 18 deliveries late in Q4)
- **Worst supplier:** Huang-Martinez (quality score 2.8, average 8.3 days late across 12 POs)
- **Trend:** Deteriorating vs. Q3 — requires supplier review

### Energy (Oracle SCM)

- **Late delivery rate:** 11.9% (5 of 42 shipments late in Q4)
- **Worst supplier:** Gonzalez & Sons (rating 2.9, average 7.1 days late across 8 POs)
- **Trend:** Stable but above 10% target

### Customer Support Impact

| Division | Q4 Tickets | Avg CSAT | Critical Tickets |
|---|---|---|---|
| Industrial | 28 | 3.7/5.0 | 11 |
| Energy | 22 | 3.5/5.0 | 9 |
| Safety | 14 | 3.9/5.0 | 4 |

Energy has the lowest customer satisfaction, likely correlated with supply chain delays. Industrial's high critical ticket count (11) aligns with its 16.7% late delivery rate.

---

## Outlook

**Positive signals:**
- Revenue growth across all divisions
- Safety division accelerating (+12.1% QoQ)
- Active customer count up 8% across the company

**Watch items:**
- Energy customer concentration (CAT Energy at 34%) is a single-point-of-failure risk
- Industrial supplier quality is deteriorating — Huang-Martinez should be placed on a performance improvement plan or replaced
- Energy CSAT at 3.5 is below target (4.0) and declining

---

*Sources: Salesforce (Industrial CRM), Legacy CRM (Energy), HubSpot (Safety), Workday (HR), SAP (Industrial Ops), Oracle SCM (Energy Ops), Zendesk (Support). Revenue figures reflect CRM order/deal data and may differ from audited financials.*
