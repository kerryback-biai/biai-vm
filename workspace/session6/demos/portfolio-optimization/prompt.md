# Demo: Portfolio Optimization (Constrained)

## What This Demonstrates
- Describing an optimization problem in plain English
- AI writes and runs the solver code (PuLP, scipy, or cvxpy)
- Mixed-integer optimization — lot selection is discrete
- The result is a starting point for conversation, not a final answer

## Tool
Claude Code on AI+Code Lab

## Prompt

```
Here is what I want to accomplish, in priority order:

1. Get every sector within 3% of its target weight (hard constraint)
2. Keep every stock under 5% of portfolio (hard constraint)
3. Minimize the total capital gains tax from trades
4. As a tiebreaker: prefer trades that follow analyst recommendations (sell Sell-rated, buy Strong-Buy-rated)

Find the set of trades (sells and buys) that satisfies the constraints while minimizing tax cost. Use a mixed-integer optimization approach since lot selection is discrete.

Show me:
- The proposed sells (which lots, which stocks, tax cost per trade)
- The proposed buys (which stocks, how much)
- Resulting sector weights vs. target
- Total tax bill
- A summary: "These N trades cost $X in taxes and bring every sector within 3% of target"
```

## Key Narration Points
- "You describe objectives and constraints in English. AI writes the optimization code."
- "This is a mixed-integer problem — lot selection is binary (sell or don't sell)."
- "The result is mathematically optimal FOR THESE PRIORITIES. Change the priorities, change the answer."
- "Spot-check: manually verify the tax on the two largest trades."

## Follow-Up (Critical Teaching Moment)
```
Wait — who decided that tax minimization was priority #3 and following recommendations was priority #5? What if the client cares more about tracking recommendations? Re-run with recommendations as priority #3 and tax as priority #5. How different is the answer?
```

## Expected Behavior
- Claude installs PuLP or uses scipy.optimize
- Formulates as MILP (Mixed Integer Linear Program)
- Runs solver, reports solution
- May take 1-2 iterations if the first formulation is infeasible

## Timing
~4 minutes
