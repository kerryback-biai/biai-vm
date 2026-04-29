# Cross-System Q&A — Key Takeaways

## What this demo shows

A single question that neither document AI nor database AI could answer alone. The agent combines contract retrieval (RAG) with live database queries (CRM) to produce an actionable analysis.

## The two-system synthesis

| Capability | Source | What it provided |
|---|---|---|
| Document AI (RAG) | GE Master Service Agreement | $4.2M minimum commitment, discount tiers, shortfall clause, renewal terms |
| Database AI (SQL) | Salesforce + Legacy CRM + HubSpot | Actual spending by division and year: $4.28M (2024), $3.80M (2025) |

Neither source alone answers the question. The contract says what we promised; the database says what actually happened. The insight — a $404K shortfall with a renewal deadline 92 days away — only emerges when both are combined.

## Teaching points

- **This is the real value of enterprise AI.** Most valuable business questions span structured data and unstructured documents. An AI that can only do one is half-useful.
- **Cross-system identity resolution still matters.** GE appears as "General Electric" in Salesforce, "GE Industrial Solutions" in the contract, and "GE Safety Division" in HubSpot. The agent must reconcile these.
- **Actionable output, not just retrieval.** The agent didn't just return the contract terms and the spending numbers — it calculated the gap, identified the penalty exposure, flagged the declining trend, and noted the 90-day renewal window. This is what separates useful AI from a search engine.
- **Citations from both systems.** The response cites the specific MSA section for the commitment and identifies which CRM system produced each spending figure. A decision-maker can verify both sides independently.

## Connection to Earlier Demo

Earlier in this session, we identified GE as a $18.4M multi-division customer using fuzzy name matching across CRMs. This demo adds the contract dimension — not just how much GE spends with us, but how much they're supposed to spend, and what happens when there's a gap.
