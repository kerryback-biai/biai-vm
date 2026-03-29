# Using Claude Code on the Workshop VM

Claude Code is an AI coding assistant that runs in your terminal. In this workshop, you'll use it on a shared Linux server rather than your own computer. This guide explains what's different and what to expect.

## Connecting

You access the VM over SSH from your laptop's terminal:

```
ssh yourname@server-address
```

Once logged in, navigate to your workspace and launch Claude Code:

```
cd workspace
claude
```

That's it — you're now in an interactive conversation with Claude right in your terminal. You can ask it questions, and it can read files, write code, and run commands on the server on your behalf.

## What's already set up for you

On your own computer, getting Claude Code working requires several setup steps: installing Node.js, installing the `claude-code` package, obtaining an API key, and installing whatever Python libraries your project needs. On the VM, **all of this is done for you**:

- **Claude Code** is pre-installed and ready to go.
- **Your API key** is already configured in the environment. You don't need to sign up for an Anthropic account or enter a key.
- **Python libraries** — `anthropic`, `duckdb`, `pandas`, `numpy`, `matplotlib`, `fastapi`, and `uvicorn` — are pre-installed system-wide. You can import any of them immediately.

## Installing additional Python libraries

On your own computer, you can install any library you want with `pip install`. On the VM, you can do the same thing:

```
pip install some-library
```

Claude Code can also run this command for you if it decides a library is needed. The difference is that on the VM, libraries install into the shared system Python rather than a personal virtual environment. This is fine for the workshop — just be aware that everyone shares the same Python installation.

## Tool permissions

This is the biggest difference from running Claude Code on your own machine.

On a personal computer, Claude Code starts in a mode where it asks your permission before running any shell command, writing any file, or taking any action. You approve or deny each one, and you can grant blanket permissions as you go.

On the VM, **permissions are pre-configured** so that Claude Code can do common tasks without asking you each time. Specifically, it can:

| Action | Example |
|---|---|
| Run Python scripts | `python ex1_hello_agent.py` |
| Install Python packages | `pip install requests` |
| Run DuckDB queries | `duckdb data/sf_accounts.parquet` |
| List and view files | `ls data/`, `cat ex1_hello_agent.py` |
| Read, write, and edit files | Creating and modifying your `.py` files |
| Run Node.js scripts | Used by the pptx skill to create slides |
| Convert documents | `pandoc report.docx -o report.md` |
| Use LibreOffice | Recalculate formulas, convert formats |
| File operations | `cp`, `mv`, `mkdir`, `zip`, `unzip` |

Claude Code **cannot** run arbitrary shell commands beyond these. For example, it can't use `curl` to download files from the internet, it can't install system packages with `apt`, and it can't access other students' home directories. This keeps the shared environment stable and secure.

If Claude Code tries to do something outside these permissions, it will tell you the action was denied. This is normal — it just means that particular command isn't on the approved list. You can usually accomplish the same goal a different way (for example, using Python's `requests` library instead of `curl`).

## Office document skills

Claude Code supports **skills** — bundles of specialized knowledge and workflows that extend what it can do. On the VM, three Office document skills are pre-installed for every student:

- **xlsx** — Create, edit, and analyze Excel spreadsheets. Claude uses real Excel formulas (not hardcoded values), applies formatting, and recalculates formulas automatically via LibreOffice.
- **docx** — Create and edit Word documents. Claude can work with tracked changes, comments, and formatting. It uses pandoc for reading and OOXML for precise editing.
- **pptx** — Create and edit PowerPoint presentations. Claude can build slide decks from scratch or modify existing ones, including layouts, speaker notes, and images.

These skills activate automatically when you ask Claude Code to work with the relevant file type. For example:

- *"Create an Excel workbook summarizing revenue by industry."*
- *"Write up our findings as a Word document."*
- *"Make a short slide deck presenting the top 5 accounts."*

On your own computer, you would install these skills yourself (or they may come pre-installed with Claude Code). On the VM, they're already in place — along with all the system tools they depend on (LibreOffice, pandoc, Node.js, and the necessary Python and npm packages).

## Your workspace

Your files live in `~/workspace/`. Inside, you'll find:

- **Exercise starter files** (`ex1_hello_agent.py`, `ex2_multi_system.py`, etc.) — these are your working copies to edit and run.
- **`data/`** — a link to the shared data directory containing the Parquet files you'll query. This data is read-only; you can query it but not modify it.

Claude Code can read and edit any file in your workspace. When you ask it for help with an exercise, it will typically read your current code, suggest changes, and (with your approval flow already handled by the pre-set permissions) write those changes directly into your file.

## What this means in practice

When you're working through the exercises, you can interact with Claude Code naturally:

- *"Read ex1_hello_agent.py and explain what the TODO section needs to do."*
- *"Help me write the agent loop — start with just the first API call."*
- *"Run the script and see if it works."*
- *"Install the tabulate library so I can format the output as a table."*

Claude Code will read your files, write code, run your Python scripts, and show you the results — all within the same terminal session. The pre-configured permissions mean you spend less time approving actions and more time learning.

## Summary of differences

| | Your own computer | Workshop VM |
|---|---|---|
| **Setup** | You install everything yourself | Pre-configured and ready to go |
| **API key** | You provide your own | Shared key, already set |
| **Python libraries** | Install into your own environment | Install into shared system Python |
| **Tool permissions** | You approve each action interactively | Common actions pre-approved; others blocked |
| **File access** | Full access to your machine | Limited to your workspace and shared data |
| **Shell commands** | Anything you allow | Whitelisted set only (python, pip, ls, etc.) |
| **Office skills** | Install yourself or use defaults | xlsx, docx, pptx pre-installed |
