# Result: Unfiltered Average Deal Size

## What the Agent Returned

| Metric | Value |
|--------|-------|
| Total Deals | 312 |
| Average Deal Size | **$48,100** |
| Total Pipeline Value | $15,006,200 |

This looks clean, plausible, and confident.

---

## What the Answer Should Have Been

The user asked about "deal size" — in any sales context, that means **closed-won deals**. Here is what a filtered query returns:

```sql
SELECT
    COUNT(*) AS total_deals,
    ROUND(AVG(amount), 0) AS avg_deal_size,
    ROUND(SUM(amount), 0) AS total_revenue
FROM salesforce.opportunities
WHERE close_date >= '2025-10-01'
  AND close_date <= '2025-12-31'
  AND stage = 'Closed Won';
```

| Metric | Unfiltered (Agent's Answer) | Closed-Won Only (Correct) |
|--------|---------------------------|--------------------------|
| Deal Count | 312 | 134 |
| Average Deal Size | $48,100 | $78,400 |
| Total Value | $15,006,200 | $10,505,600 |

The agent's answer is **39% lower** than the actual closed-won average.

---

## Why It Went Wrong

The 312 deals include:
- **134 Closed Won** — avg $78,400
- **89 Closed Lost** — avg $28,100 (prospects who dropped off early tend to have smaller estimated values)
- **89 Open/In Progress** — avg $22,500 (early-stage deals with preliminary estimates)

The lost and open deals drag down the average significantly. The SQL is technically valid — it does compute an average of deals in Q4 — but it answers a different question than the one the user intended.

---

## Key Takeaway

The agent produced a technically correct result for a query it was never asked. "Average deal size" in a business context means closed-won deals. A human analyst would know this; the AI did not disambiguate. The danger: **$48K looks reasonable enough to use in a board presentation without verification.**
