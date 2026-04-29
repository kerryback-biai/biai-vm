# Demo: Failure — Entity Resolution Double-Count

## Session Context
Session 5 — Deployment and Governance (Failure #3)

## Prompt
> How many unique customers do we have across all divisions?

## Purpose
Demonstrate how entity resolution failures cause customer double-counting across systems. XYZ has ~25 customers that appear under different names in different divisions' CRMs. The agent uses fuzzy matching to deduplicate but misses many variants, reporting 847 unique customers when the true number is ~690 — a 23% overcount.

## What to Watch For
- The agent queries 3 separate CRMs
- Fuzzy matching catches obvious cases ("Acme Corp" vs "ACME Corp") but misses others
- Examples of missed duplicates: "Acme Corp" / "ACME Corporation" / "Acme Corp." counted as 3
- The agent sets a similarity threshold of 0.85 — too high to catch abbreviation and suffix variants
- The final number (847) is stated with confidence and no uncertainty range
