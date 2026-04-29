# Session 5 Demos: Deployment and Governance

All demos run on the XYZ Corp Custom Chatbot showing AI failure modes.

## Demo 1: Failure — Unfiltered Average
Revenue distorted 40% by including cancelled orders in averages. Shows why filtering matters.

## Demo 2: Failure — Silent Date Format
$2.3M revenue understated because Legacy CRM stores dates as MM/DD/YYYY text strings. The agent silently parsed them wrong.

## Demo 3: Failure — Entity Double Count
Customer counts inflated 23% because fuzzy matching created false positives across CRMs.

## Demo 4: Data Security Guardrails
Shows layered defenses: SQL validation (reject non-SELECT), row limits, column redaction, prompt instructions for missing data.
