"""
Exercise 2: Multi-System Agent
===============================
Extend your agent to query TWO separate systems and merge the results.

Systems:
  - salesforce: sf_accounts, sf_orders (CRM data)
  - workday: wd_workers, wd_compensation (HR data)

The agent should be able to answer questions like:
  "Which sales reps generate the most revenue per dollar of compensation?"

This requires:
  1. Query salesforce for revenue by OwnerId
  2. Query workday for compensation by worker_id
  3. Use the wd_system_ids table to map between them
  4. Merge in Python and compute the ratio

Data files are in:
  data/salesforce/sf_accounts.parquet
  data/salesforce/sf_orders.parquet
  data/workday/wd_workers.parquet
  data/workday/wd_compensation.parquet
  data/workday/wd_system_ids.parquet

Run with: python ex2_multi_system.py
"""
import anthropic
import duckdb
import json

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

# --- System definitions ---
# Each system has its own tables — they cannot be joined in a single query
SYSTEMS = {
    "salesforce": {
        "sf_accounts": "data/salesforce/sf_accounts.parquet",
        "sf_orders": "data/salesforce/sf_orders.parquet",
    },
    "workday": {
        "wd_workers": "data/workday/wd_workers.parquet",
        "wd_compensation": "data/workday/wd_compensation.parquet",
        "wd_system_ids": "data/workday/wd_system_ids.parquet",
    },
}

SYSTEM_PROMPT = """You are a data analyst with access to two enterprise systems:

**salesforce** (Meridian Industrial CRM):
  - sf_accounts: AccountId, AccountName, Industry, BillingState, OwnerId, AnnualRevenue, Type
  - sf_orders: OrderId, AccountId, OpportunityId, OrderDate, TotalAmount, Status

**workday** (Corporate HR):
  - wd_workers: worker_id, first_name, last_name, division, department, job_title, status
  - wd_compensation: comp_id, worker_id, effective_date, base_pay, bonus_target_pct, bonus_actual
  - wd_system_ids: worker_id, system_name, external_id (maps worker_id to Salesforce OwnerId)

You CANNOT join across systems in a single SQL query.
To combine data, query each system separately, then use code_execution to merge with pandas.
Use wd_system_ids to map Salesforce OwnerId to Workday worker_id."""

# --- Tool with system parameter ---
TOOLS = [
    {
        "name": "query_database",
        "description": "Execute SQL against a specific enterprise system.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string"},
                "system": {
                    "type": "string",
                    "enum": ["salesforce", "workday"],
                    "description": "Which system to query",
                },
            },
            "required": ["sql", "system"],
        },
    },
    # TODO: Add the code_execution tool so Claude can merge data with Python
    # Hint: {"type": "code_execution_20250522", "name": "code_execution"}
]


def run_query(sql, system):
    """Execute SQL against a specific system's tables."""
    if system not in SYSTEMS:
        return {"error": f"Unknown system: {system}"}

    con = duckdb.connect()
    for view_name, path in SYSTEMS[system].items():
        con.execute(f"CREATE VIEW {view_name} AS SELECT * FROM read_parquet('{path}')")

    try:
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return {"columns": columns, "data": [dict(zip(columns, row)) for row in rows[:100]]}
    except Exception as e:
        return {"error": str(e)}
    finally:
        con.close()


def ask(question):
    """Send a question to the multi-system agent."""
    messages = [{"role": "user", "content": question}]

    # TODO: Implement the agent loop
    # This is similar to Exercise 1, but now:
    #   - The tool has a "system" parameter — extract it from the tool call
    #   - Claude may make MULTIPLE tool calls (one per system) before giving an answer
    #   - Claude may also use code_execution to merge results with Python
    #   - Keep looping until stop_reason is "end_turn"

    pass  # Replace with your implementation


if __name__ == "__main__":
    print("Meridian Corp Multi-System Agent (Exercise 2)")
    print("You can ask questions that span Salesforce and Workday.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        answer = ask(question)
        if answer:
            print(f"\nAgent: {answer}\n")
