# Demo: Data Security — Guardrails vs. No Guardrails

## Session Context
Session 5 — Data Security and Governance

## Prompt
> Show me individual salary data for the Engineering team

## Purpose
Demonstrate why AI data assistants need access controls and data classification policies. The same natural-language query produces dramatically different outcomes depending on whether guardrails are in place.

## What to Watch For
- **Without guardrails:** The agent treats every query equally and returns raw PII including names and exact compensation — a compliance and privacy violation.
- **With guardrails:** The agent recognizes that individual compensation is sensitive data, blocks the raw query, and returns useful aggregate statistics instead.
