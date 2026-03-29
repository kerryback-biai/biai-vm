"""
Exercise 1 Solution: Hello World Data Agent
============================================
Complete working agent with the loop filled in.
Keep this in the exercises/ folder (not shared with students).
"""
import anthropic
import duckdb
import json

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """You are a data analyst. You have access to a Salesforce accounts database.

Table: sf_accounts
Columns: AccountId, AccountName, Industry, BillingState, OwnerId, AnnualRevenue, Type

Use the query_database tool to run SQL queries. The table name in SQL is 'sf_accounts'."""

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
    con = duckdb.connect()
    con.execute("CREATE VIEW sf_accounts AS SELECT * FROM read_parquet('data/salesforce/sf_accounts.parquet')")
    result = con.execute(sql)
    columns = [desc[0] for desc in result.description]
    rows = result.fetchall()
    con.close()
    return {"columns": columns, "data": [dict(zip(columns, row)) for row in rows[:50]]}


def ask(question):
    messages = [{"role": "user", "content": question}]

    for _ in range(10):  # max 10 rounds to prevent infinite loops
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=TOOLS,
        )

        # If Claude is done talking, return the text
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return ""

        # If Claude wants to use a tool, execute it
        if response.stop_reason == "tool_use":
            # Find the tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    sql = block.input["sql"]
                    print(f"  [Running SQL: {sql[:80]}...]")
                    result = run_query(sql)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, default=str),
                    })

            # Add the assistant's message and tool results to the conversation
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

    return "Agent reached maximum rounds without finishing."


if __name__ == "__main__":
    print("Meridian Corp Data Agent (Exercise 1 — Solution)")
    print("Type a question about Salesforce accounts, or 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue

        answer = ask(question)
        print(f"\nAgent: {answer}\n")
