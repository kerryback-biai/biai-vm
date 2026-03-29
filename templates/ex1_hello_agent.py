"""
Exercise 1: Hello World Data Agent
===================================
Build a simple agent that:
  1. Takes a question about sales data
  2. Sends it to Claude with a description of the database
  3. Claude generates SQL
  4. You execute the SQL against a parquet file
  5. Send results back to Claude
  6. Claude writes a natural language answer

The data file is: data/salesforce/sf_accounts.parquet
It contains: AccountId, AccountName, Industry, BillingState, OwnerId, AnnualRevenue, Type

Run with: python ex1_hello_agent.py
"""
import anthropic
import duckdb
import json

# --- Step 1: Set up the Claude client ---
client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY from environment
MODEL = "claude-sonnet-4-20250514"

# --- Step 2: Define the system prompt ---
# Tell Claude what database is available and how to query it
SYSTEM_PROMPT = """You are a data analyst. You have access to a Salesforce accounts database.

Table: sf_accounts
Columns: AccountId, AccountName, Industry, BillingState, OwnerId, AnnualRevenue, Type

Use the query_database tool to run SQL queries. The table name in SQL is 'sf_accounts'."""

# --- Step 3: Define the tool ---
# This tells Claude it can call a function called "query_database"
TOOLS = [
    {
        "name": "query_database",
        "description": "Execute a SQL query against the Salesforce accounts database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "SQL query to execute"}
            },
            "required": ["sql"],
        },
    }
]


def run_query(sql):
    """Execute SQL against the parquet file and return results."""
    con = duckdb.connect()
    con.execute("CREATE VIEW sf_accounts AS SELECT * FROM read_parquet('data/salesforce/sf_accounts.parquet')")
    result = con.execute(sql)
    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()
    con.close()
    return {"columns": columns, "data": [dict(zip(columns, row)) for row in rows[:50]]}


def ask(question):
    """Send a question to the agent and get an answer."""
    messages = [{"role": "user", "content": question}]

    # --- Step 4: The agent loop ---
    # TODO: Fill in the agent loop
    # Hint: Call client.messages.create() with model, system, messages, tools
    # Then check if stop_reason is "tool_use"
    # If so, extract the SQL, run it, and send results back
    # Keep looping until stop_reason is "end_turn"

    pass  # Replace this with your implementation


# --- Main ---
if __name__ == "__main__":
    print("Meridian Corp Data Agent (Exercise 1)")
    print("Type a question about Salesforce accounts, or 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        answer = ask(question)
        if answer:
            print(f"\nAgent: {answer}\n")
