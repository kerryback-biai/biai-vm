# Demo: Iteration — Three Drafts of the Same Request

**Session 4** — Show how prompt specificity drives output quality. Three iterations of the same request, each with a more specific prompt, producing progressively better results.

---

## Draft 1

### User

Summarize Q4 performance.

### Agent (queries run behind the scenes)

The agent queries Salesforce, Legacy CRM, HubSpot, and Workday — same queries as the full pipeline demo. It receives the revenue and headcount numbers and produces a generic summary.

### Agent response

> **XYZ Corp Q4 2025 Summary**
>
> XYZ Corp generated $10.5M in revenue during Q4 2025, up from $9.7M in Q3 2025, representing 7.8% quarter-over-quarter growth.
>
> **Revenue by division:**
> - Industrial: $5.9M (56% of total)
> - Energy: $3.4M (33% of total)
> - Safety: $1.1M (11% of total)
>
> **Headcount:**
> - Industrial: 308 employees
> - Energy: 220 employees
> - Safety: 106 employees
> - Corporate: 71 employees
>
> All three divisions showed positive revenue growth compared to Q3. Safety had the highest growth rate at 12.1%. The company has 193 active customers across divisions.
>
> Revenue per employee ranges from $10,829/month (Safety) to $19,127/month (Industrial).

### What's wrong with Draft 1

- Generic — reads like a data dump, not an executive summary
- No prioritization — all information is treated as equally important
- No risk flags or action items
- No comparison to plan or targets
- A manager reading this would say: "So what? What should I do?"

---

## Draft 2

### User

Redo this in traffic-light format — green/yellow/red for each division. Flag any metric more than 10% off plan.

### Agent (queries additional data)

The agent now queries `netsuite_corporate.ns_corp_budget` for plan figures and computes variances. It also pulls supply chain and customer concentration data to assess risk.

**Additional query — Budget vs Actual:**

```sql
SELECT
    division,
    SUM(amount) AS q4_budget
FROM ns_corp_budget
WHERE fiscal_year = 2025
  AND fiscal_month BETWEEN 10 AND 12
  AND account_code = 'REV-001'
GROUP BY division
```
System: `netsuite_corporate`

| division   | q4_budget  |
|------------|------------|
| Industrial | 6,200,000  |
| Energy     | 3,100,000  |

### Agent response

> **XYZ Corp Q4 2025 — Traffic Light Dashboard**
>
> | Division | Revenue | vs Plan | Headcount Eff. | Customer Risk | Supply Chain | Overall |
> |---|---|---|---|---|---|---|
> | **Industrial** | $5.9M | -5.0% below plan | $19.1K/emp | Low (top customer 7%) | Late deliveries 16.7% | YELLOW |
> | **Energy** | $3.4M | +10.1% above plan | $15.5K/emp | HIGH — CAT Energy 34% | Late shipments 11.9% | RED |
> | **Safety** | $1.1M | N/A (no budget data) | $10.8K/emp | Medium (top customer 14%) | N/A | YELLOW |
>
> **RED flags (>10% off plan):**
> - Energy customer concentration: CAT Energy Services at 33.9% of division revenue (threshold: 10%)
> - Industrial late delivery rate: 16.7% (target: <10%)
>
> **YELLOW flags:**
> - Industrial revenue 5.0% below plan ($5.9M vs $6.2M target)
> - Safety revenue per employee lowest at $10.8K/month
> - Energy CSAT score 3.5/5.0 (below 4.0 target)
>
> **GREEN:**
> - Energy revenue +10.1% above plan
> - Overall revenue growth +7.8% QoQ
> - Safety growth rate +12.1% QoQ — strongest division momentum

### What improved in Draft 2

- Traffic-light format gives instant visual prioritization
- Comparison to plan surfaces variances, not just trends
- Red/yellow/green makes it scannable in 10 seconds
- But: still no recommended actions; still fairly long; no clear "lead" finding

---

## Draft 3

### User

One page maximum. Lead with the biggest risk. End with three recommended actions.

### Agent response

> # Q4 2025 EXECUTIVE BRIEF — XYZ CORP
>
> ## Biggest risk: Energy division depends on a single customer
>
> CAT Energy Services generated **$1.16M in Q4** — **34% of the Energy division's revenue**. If this relationship deteriorates, Energy loses one-third of its business in a single event. No other division has a customer above 14%.
>
> ---
>
> ## Scorecard
>
> | | Industrial | Energy | Safety |
> |---|---|---|---|
> | Q4 Revenue | $5.9M | $3.4M | $1.1M |
> | vs Plan | -5% | +10% | N/A |
> | QoQ Growth | +7.5% | +7.1% | +12.1% |
> | Rev/Employee | $19.1K/mo | $15.5K/mo | $10.8K/mo |
> | Top Customer % | 7.0% | **33.9%** | 13.6% |
> | On-Time Delivery | 83.3% | 88.1% | N/A |
> | CSAT | 3.7 | **3.5** | 3.9 |
> | **Status** | YELLOW | **RED** | YELLOW |
>
> **Company total: $10.5M revenue, +7.8% QoQ, 634 employees across divisions**
>
> ---
>
> ## Three recommended actions
>
> 1. **Diversify Energy's customer base.** Task the Energy sales team with adding 3-5 new accounts in Q1 2026 to reduce CAT dependency below 25%. Assign a dedicated account development manager.
>
> 2. **Fix Industrial supplier quality.** Place Huang-Martinez (quality score 2.8, avg 8 days late) on a 60-day performance improvement plan. Qualify a backup vendor for their material categories.
>
> 3. **Investigate Energy CSAT decline.** At 3.5/5.0, Energy has the lowest satisfaction score. Cross-reference Zendesk tickets with late shipments to determine if supply chain delays are the root cause, and present findings at the February operations review.

### What improved in Draft 3

- Leads with the single most important finding — a reader knows the headline in 5 seconds
- Compact scorecard fits on one page with all KPIs visible at once
- Traffic-light colors retained but simplified into a status row
- Ends with three concrete, assignable actions with owners and timelines
- Executive-ready: a board member could read this in 90 seconds and know exactly what to do

---

## The Lesson

The same data, the same agent, the same systems — but three very different outputs. The quality of the output is determined by the specificity of the prompt:

| Draft | Prompt specificity | Output quality |
|---|---|---|
| 1 | "Summarize Q4 performance" | Data dump — no prioritization or insight |
| 2 | "Traffic-light format, flag >10% off plan" | Structured dashboard — scannable but no actions |
| 3 | "One page, lead with risk, end with actions" | Executive brief — prioritized, actionable, board-ready |

The AI had all the same data each time. **The human's prompt was the variable that mattered.**
