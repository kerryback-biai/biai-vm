# Portfolio Rebalancing — Exercise Overview

## The Problem

A portfolio rebalancing decision involves four competing objectives:

1. **Hold only recommended stocks.** Every Sell-rated stock still in the portfolio is a drag — but selling incurs costs.
2. **Minimize capital gains taxes.** Selling triggers realized gains. The tax bill depends on which lot you sell and whether the gain is short-term or long-term.
3. **Minimize sector deviation.** The client has target sector weights. Trading should move actual weights toward targets.
4. **Diversify within sectors.** Concentrating a sector in one or two stocks adds idiosyncratic risk.

These objectives fight each other. Selling every Sell-rated stock maximizes #1 but may be expensive (#2). Doing nothing is tax-free but ignores recommendations and lets drift accumulate.

## Your Data

- `data/portfolio/client_info.md` — the Chens, a moderate-risk couple with a $500K taxable account, sector-weight targets, and constraints (no tobacco, no crypto)
- `data/portfolio/portfolio_lots.xlsx` — 49 stocks across 11 sectors, 167 tax lots with columns: Date, Ticker, Sector, Industry, Size, Shares, Price per Share, Cost
- `data/portfolio/stock_data.md` — MotherDuck database connection with ~4,300 stocks, current prices, price-to-book ratios, and analyst recommendations

## Conversation Arc

### Step 1: Assess the current state
Give Claude the client profile, portfolio, and database access. Ask it to score the portfolio on each objective:
- What fraction of portfolio value is in Sell-rated stocks?
- What is the total sector deviation?
- What is the within-sector concentration?
- What would the tax bill be if you sold everything rated Sell?

### Step 2: Explore the trade-offs
- "If I only sell the three largest Sell-rated positions, how much does sector deviation improve and what does it cost in taxes?"
- "What if I prioritize tax-free trades — selling positions with losses first?"
- "Can you quantify each objective as a score so we can compare plans?"

### Step 3: Ask for an optimized plan
Ask Claude to propose a trading plan that balances all four objectives. Let it choose the approach. Pay attention to whether it explains the trade-offs.

### Step 4: Challenge the result
- "What am I giving up? Show me what happens if we weight taxes more heavily."
- "What if we weight recommendations more heavily?"
- See how the plan shifts.

## What to Watch For

- Does the AI quantify the objectives or stay qualitative?
- Does it surface trade-offs you hadn't considered?
- Does it propose a way to systematically compare alternative plans?
- Does it respect all hard constraints? (max 5% single stock, max 3pp sector deviation, no tobacco, wash sale rule)

## Verification

After you have a proposed plan:

> Generate 1,000 random feasible trading plans. Each plan randomly selects 5-10 stocks to sell and 5-10 to buy, with random dollar amounts, choosing tax lots randomly. Score each plan on all four objectives. Then:
> 1. Plot tax cost vs. sector deviation improvement, coloring points by recommendation alignment
> 2. Show where the AI's proposed plan falls
> 3. Report how many random plans the AI's proposal dominates (better on every objective)
