# Demo: What-If Scenarios

## What This Demonstrates
- AI as a what-if engine — exploring tradeoffs quantitatively in seconds
- Each scenario that would take an hour in a spreadsheet takes seconds
- Speed changes how you think: explore 20 options, not 2

## Tool
Claude Code on AI+Code Lab

## Setup
Data at `data/portfolio/` (in the session6 folder):
- portfolio_lots.xlsx (or .csv) — 167 tax lots
- client_info.md — client profile and constraints

## Prompts (sequential, building on each other)

### Prompt 1: Assess Current State
```
Read the client profile and portfolio lots. Connect to the stock database on MotherDuck for current prices. Give me:
1. Total portfolio value and unrealized gain/loss
2. Current sector weights vs. target — flag any >3% off
3. Any single stock over 5% of portfolio
4. Stocks rated Sell — show the tax cost if I sold each one (highest-cost-basis lots first)
```

### Prompt 2: What If We Follow All Recommendations?
```
If I sell all Sell-rated stocks using highest-cost-basis lots first, what is the total tax bill? How do the sector weights change after selling?
```

### Prompt 3: What If We Only Act Where Cheap?
```
If I only sell Sell-rated stocks where I can use lots with less than $1,000 total gain, which trades qualify? How much sector improvement do I get for that limited tax cost?
```

### Prompt 4: The Tradeoff Curve
```
Show me the tradeoff: create a table with 5 scenarios ranging from "$0 tax budget" to "unlimited tax budget." For each, show the best sector alignment achievable and which trades are needed. Plot the tradeoff — tax cost on x-axis, max sector deviation on y-axis.
```

## Key Narration Points
- "Each of these scenarios would take an hour in a spreadsheet. Here, seconds."
- "The speed changes how you think — you explore more options, find better tradeoffs."
- "Prompt 4 is the power move: the tradeoff curve shows you exactly what each additional dollar buys."

## Timing
~5 minutes (pick prompts 1 and 4 for live demo)
