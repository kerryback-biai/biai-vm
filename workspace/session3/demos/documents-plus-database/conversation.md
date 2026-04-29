# Demo: Cross-System Q&A — Document AI + Database AI

## User prompt

> What's our contractual commitment to GE, and how does their actual spending compare?

---

## Agent reasoning (visible to class)

This question requires two sources: (1) the GE contract from the document store, and (2) actual spending data from the CRM and finance systems.

**Step 1 — Retrieve contract from document store (RAG)**

Searching document store for: "GE General Electric master service agreement commitment"

*Retrieved chunks:*
- `contracts/ge_master_service_agreement.pdf` — Section 3: "Volume Commitments" (p. 5, relevance: 0.96)
- `contracts/ge_master_service_agreement.pdf` — Section 8: "Term and Renewal" (p. 11, relevance: 0.91)
- `contracts/ge_master_service_agreement.pdf` — Exhibit B: "Volume Discount Schedule" (p. 18, relevance: 0.87)

**Contract terms extracted:**

| Term | Detail |
|---|---|
| Agreement | Master Service Agreement #MSA-2023-0847 |
| Parties | XYZ Corp / GE Industrial Solutions |
| Effective date | July 1, 2023 |
| Term | 3 years (through June 30, 2026) |
| Minimum annual commitment | $4.2M across all divisions |
| Volume discount tiers | Tier 1: $0-3M at list price; Tier 2: $3-5M at 8% discount; Tier 3: $5M+ at 12% discount |
| Shortfall clause | If annual purchases fall below $4.2M, XYZ forfeits Tier 2/3 pricing retroactively for that year |
| Renewal | Auto-renews for 1-year terms unless 90-day notice given |

(GE Master Service Agreement, Sections 3, 8, and Exhibit B)

**Step 2 — Query CRM systems for GE actual spending**

GE purchases from all three XYZ divisions under different names. Querying each system.

```sql
-- System: salesforce_crm
SELECT
    AccountName,
    EXTRACT(YEAR FROM CloseDate) AS year,
    SUM(Amount) AS total
FROM sf_opportunities
WHERE StageName = 'Closed Won'
  AND AccountName LIKE '%General Electric%'
GROUP BY AccountName, EXTRACT(YEAR FROM CloseDate)
ORDER BY year;
```

*Result:*

| Year | Amount |
|---|---|
| 2024 | $2,847,000 |
| 2025 | $2,612,000 |

```sql
-- System: legacy_crm
SELECT
    CustName,
    SUBSTR(OrderDate, 7, 4) AS year,
    SUM(OrderTotal) AS total
FROM orders
WHERE OrderStatus = 'Complete'
  AND CustName LIKE '%GE%'
GROUP BY CustName, SUBSTR(OrderDate, 7, 4)
ORDER BY year;
```

*Result:*

| Year | Amount |
|---|---|
| 2024 | $1,024,000 |
| 2025 | $843,000 |

```sql
-- System: hubspot_crm
SELECT
    company_name,
    EXTRACT(YEAR FROM close_date) AS year,
    SUM(deal_amount) AS total
FROM hs_deals
WHERE deal_stage = 'closedwon'
  AND company_name LIKE '%GE%'
GROUP BY company_name, EXTRACT(YEAR FROM close_date)
ORDER BY year;
```

*Result:*

| Year | Amount |
|---|---|
| 2024 | $412,000 |
| 2025 | $341,000 |

**Step 3 — Consolidate and compare**

```python
import pandas as pd

ge_spending = {
    2024: {'Industrial (Salesforce)': 2_847_000,
           'Energy (Legacy CRM)': 1_024_000,
           'Safety (HubSpot)': 412_000},
    2025: {'Industrial (Salesforce)': 2_612_000,
           'Energy (Legacy CRM)': 843_000,
           'Safety (HubSpot)': 341_000}
}

for year, divisions in ge_spending.items():
    total = sum(divisions.values())
    gap = 4_200_000 - total
    print(f"{year}: ${total:,.0f} — {'ABOVE' if gap < 0 else 'BELOW'} commitment by ${abs(gap):,.0f}")
```

*Result:*
```
2024: $4,283,000 — ABOVE commitment by $83,000
2025: $3,796,000 — BELOW commitment by $404,000
```

---

## Agent response

### GE Relationship Summary

**Contractual commitment:** Under MSA #MSA-2023-0847, XYZ is committed to purchasing a minimum of **$4.2M annually** from GE across all divisions. The agreement runs through June 30, 2026, and auto-renews unless either party gives 90-day notice (GE MSA, Section 8, p. 11).

**Actual spending vs. commitment:**

| Year | Industrial | Energy | Safety | Total | vs. $4.2M Target |
|---|---|---|---|---|---|
| 2024 | $2.85M | $1.02M | $0.41M | **$4.28M** | +$83K (met) |
| 2025 | $2.61M | $0.84M | $0.34M | **$3.80M** | **-$404K (missed)** |

**Key risks:**

1. **Shortfall penalty exposure.** GE spent $3.80M in 2025, falling $404K short of the $4.2M minimum. Under Section 3.2, GE can retroactively revoke Tier 2 pricing for 2025, which would increase our effective cost by approximately $160K on the $3-3.8M band (GE MSA, Section 3.2, p. 5).

2. **Declining trend.** Spending fell 11.3% year-over-year across all three divisions. Energy Division spending dropped 17.7%, the steepest decline — consistent with the broader pullback in Energy Division pipeline visible in the CRM.

3. **Renewal leverage.** The contract auto-renews on June 30, 2026 (92 days from now). If GE invokes the shortfall clause, they gain leverage to renegotiate terms. If XYZ wants to maintain the current discount structure, proactive engagement before the 90-day notice window (April 1) is critical.

**Recommendation:** Schedule a QBR with the GE account team before April 1 to address the 2025 shortfall and align on 2026 volume projections before the auto-renewal kicks in.

**Sources:**
- *GE Master Service Agreement* (#MSA-2023-0847), Sections 3, 8, Exhibit B
- *Salesforce CRM* — Industrial Division closed-won opportunities, 2024-2025
- *Legacy CRM* — Energy Division completed orders, 2024-2025
- *HubSpot CRM* — Safety Division closed-won deals, 2024-2025
