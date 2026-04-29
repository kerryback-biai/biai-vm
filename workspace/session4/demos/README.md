# Session 4 Demos: Building AI Agents

## Demo 1: Agent Loop Explained
Walkthrough of a cross-system agent answering "Which division has the highest customer concentration risk?" Shows the agent loop: question → LLM → SQL → execute → interpret → answer.

## Demo 2: Build Agent from English
Live build of a ~50-line Python agent from a plain English prompt. Claude Code reads parquet schemas, writes the agent loop, and produces a working data agent in ~3 minutes.

## Demo 3: Full Reporting Pipeline
One prompt generates a quarterly executive summary — queries 7 systems (Salesforce, Legacy CRM, HubSpot, Workday, SAP, Oracle SCM, Zendesk), generates charts, writes narrative, produces a board-ready report.

## Demo 4: System Prompt Break/Fix
Shows how removing a join-key from the system prompt breaks cross-system queries. Demonstrates that the system prompt IS the agent's institutional knowledge.

## Demo 5: Three Iteration Drafts
Same data, three prompts: "Summarize Q4" → data dump; + "Traffic-light format" → structured dashboard; + "One page, lead with risk" → executive brief.
