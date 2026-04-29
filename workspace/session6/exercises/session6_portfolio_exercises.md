# Session 6: Portfolio Decision-Making Exercises

Platform: AI+Code Lab (Claude Code). Data in `data/portfolio/`.

## Exercise 1: Assess the Current Portfolio (10 minutes)

```
Read the client profile, the portfolio lots, and connect to the stock database.
Give me a portfolio assessment:

1. Current value and total unrealized gain/loss
2. Current sector weights vs. target weights — flag any that are more than 3% off target
3. Any single stock over 5% of portfolio
4. Stocks in the portfolio with a Sell or Strong Buy recommendation
5. For the Sell-rated stocks, show me the tax lots — what would it cost in taxes to sell
   each one? Assume top federal rates: 20% long-term and 37% short-term capital gains.
```

## Exercise 2: Explore the Tradeoffs (12 minutes)

Try these what-if questions:

1. "If I sell all Sell-rated stocks using the highest-cost-basis lots first, what is the total tax bill? How do the sector weights change?"

2. "If I only sell Sell-rated stocks where I can use lots with less than $1,000 in gains, which trades qualify? How much sector improvement do I get?"

3. "What if I ignore the Sell recommendations entirely and only rebalance sectors? What is the cheapest set of trades to get every sector within 3% of target?"

4. "Show me the tradeoff: for each additional $1,000 in tax cost, how much closer to target weights can I get?"

## Exercise 3: Optimization (8 minutes)

```
Here is what I want to accomplish, in priority order:

1. Get every sector within 3% of its target weight (hard constraint)
2. Keep every stock under 5% of portfolio (hard constraint)
3. Minimize the total capital gains tax from trades
4. As a tiebreaker when tax costs are within $500 of each other, prefer trades
   that follow analyst recommendations

Find the set of trades that satisfies the constraints while minimizing tax cost.
Use any optimization approach you think is appropriate (this is a mixed-integer
problem — lot selection is discrete). Show me the proposed trades, the resulting
sector weights, and the total tax bill.
```

Spot-check: manually calculate the tax on the two largest recommended trades.

## Exercise 4: AI as Discussion Partner (12 minutes)

Try 2-3 of these:

1. "The optimizer says to hold the AAPL lots even though AAPL is rated Sell. Walk me through the reasoning. What am I giving up by holding? What would it cost to sell?"

2. "I'm willing to pay up to $5,000 more in taxes if it significantly improves my sector alignment. Re-run the optimization with that budget. How much better do the sector weights get?"

3. "Suppose the client now tells you they might need college withdrawals in 5 years. How does that change which lots I should sell now vs. later?"

4. "What would a conservative wealth manager do here vs. an aggressive one? Show me both plans side by side."

5. "Given everything we have discussed, what would you recommend? Explain your reasoning and tell me where reasonable people might disagree."

## Breakout: Your Multi-Objective Decision (15 minutes)

For each person (1 minute):

1. Name a decision you face with multiple conflicting objectives (be specific)
2. List the objectives (hard constraints, soft constraints, goals)
3. Identify the key tradeoff where two objectives conflict most sharply
4. Draft three what-if questions you would ask AI to explore the tradeoff
