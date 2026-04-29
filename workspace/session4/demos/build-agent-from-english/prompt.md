# Demo: Build a Data Agent from English

## What This Demonstrates
- Going from zero to a working agent in ~3 minutes
- Claude Code generates the entire agent (~50 lines of Python)
- The agent loop: system prompt → LLM → SQL → execute → return
- "You built the same thing the XYZ Corp Chatbot does — just simpler"

## Tool
Claude Code on AI+Code Lab (ai-lab.rice-business.org)

## Setup
Parquet files at `data/` contain XYZ Corp data:
- salesforce/sf_accounts.parquet (Salesforce accounts)
- salesforce/sf_orders.parquet (Salesforce orders)
- workday/wd_workers.parquet (HR data)
- workday/wd_compensation.parquet (compensation)
- workday/wd_system_ids.parquet (cross-system ID mapping)

DuckDB is pre-installed (queries parquet files directly, no database server needed).

## Prompt to Claude Code

```
Build a Python script called agent.py that:
1. Takes a business question as input (from the command line or interactive prompt)
2. Sends it to Claude with a schema description of the parquet files in data/
3. Gets back a SQL query
4. Runs the SQL against the parquet files using DuckDB
5. Prints the results in a formatted table

First, read the parquet files to discover their schemas. Then build the agent.
Make it interactive — loop so I can ask multiple questions without restarting.
```

## Key Narration Points
- "I'm telling Claude Code in plain English to build an agent. Watch."
- "It's reading the files first to discover the schema — smart."
- "About 50 lines of code. There's the system prompt. There's the tool call. There's the execution loop."
- Run it: ask "How many employees does each division have?"
- "From blank file to working agent. About 3 minutes."

## Test Questions (after the agent is built)
```
How many employees does each division have?
What is total revenue by division?
Which customers have the most support tickets?
What is the average deal size in the Energy division?
```

## Teaching Moment
After the demo, show the code briefly:
- "See the system prompt? That's the schema description — same as the XYZ Corp Chatbot."
- "See the while loop? That's the agent loop — same pattern, every agent everywhere."
- "50 lines vs. 3,000 lines. The gap is authentication, error handling, web UI, logging."

## Timing
~3 minutes for the build, ~2 minutes for testing = 5 minutes total
