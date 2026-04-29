# Demo: Failure — Date Format Mismatch

## Session Context
Session 5 — Deployment and Governance (Failure #2)

## Prompt
> Show me Q4 2025 revenue by division

## Purpose
Demonstrate how cross-system date format inconsistencies cause silent data errors. Salesforce stores dates as `YYYY-MM-DD` (ISO standard). The legacy CRM used by the Energy division stores dates as `VARCHAR` in `MM/DD/YYYY` format. The agent's date parsing treats some November dates as January dates, understating Energy revenue by ~$2.3M.

## What to Watch For
- The agent queries two different systems with different date storage formats
- String comparison on `MM/DD/YYYY` format: `'11/15/2025' < '10/01/2025'` evaluates to TRUE because `'1' < '1'` is false but `'11' > '10'` ... except lexicographic sort means `'01'` (from dates like `01/xx`) gets mixed in
- The Energy division number looks plausible but is ~15% too low
- No error is thrown — the result is silently wrong
