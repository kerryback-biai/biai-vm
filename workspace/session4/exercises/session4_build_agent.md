# Session 4: Build Your Own Data Agent

Platform: AI+Code Lab (Claude Code)

## Exercise: Build an Agent from English (12 minutes)

Tell Claude Code:

> Build a Python script that takes a business question, sends it to Claude with a description of the XYZ Corp data schema, gets back a SQL query, runs it against the parquet files in data/ using DuckDB, and prints the answer.

Then test it with 2-3 questions:
- "What is total revenue by division?"
- "Which sales rep has the highest total order value?"
- "What is the average deal size in the Energy division?"

Verify the answers against what you know from the XYZ Corp Custom Chatbot.

## Template Files

If you prefer to work from starter code with TODOs to fill in:

- `session4_hello_agent.py` — Single-system agent (Salesforce accounts only)
- `session4_multi_system.py` — Multi-system agent (Salesforce + Workday)
- `session4_web_app.py` — Wrap the agent in a web interface

## Homework (choose one)

**Option 1 — Customer Risk Report:**
"CRM data + support tickets. Flag high-revenue AND high-complaint customers."

**Option 2 — Division P&L Comparison:**
"Revenue by division from CRMs + headcount from Workday. Calculate revenue per employee."

**Option 3 — Board Memo:**
"Q3 vs Q4 across all divisions. Charts, narrative, risk flags. Iterate to one page."

Verification standard: high-stakes (verify every claim).
