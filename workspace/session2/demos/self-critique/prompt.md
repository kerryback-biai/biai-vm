# Demo: Self-Critique

## What This Demonstrates
- AI can identify weaknesses in its own analysis
- Self-critique catches framing/presentation issues (not data errors)
- The maker/checker framework: AI makes, you check

## Tool
Claude Code on AI+Code Lab (same session)

## Prompt

```
What would a skeptical CFO question about this analysis? What assumptions did you make that I should verify? Be specific — name the assumption and what could go wrong if it's wrong.
```

## Expected Response (typical findings)
Claude will typically flag:
- "I included churned customers in the 'active customer' count" (or vice versa)
- "I used calendar year, not fiscal year — your company may differ"
- "Revenue per employee uses total headcount, not just revenue-generating roles"
- "I didn't distinguish between booked revenue and collected revenue"
- "The concentration risk calculation includes all transactions regardless of status"

## Follow-Up Prompt (verification)
```
You said you may have included churned customers. Check: how many customers in the data have status 'Churned'? Did you include them in the 'active customers' metric? If so, fix it and rerun the key metrics.
```

## Key Narration Points
- "This is the quality control move. Ask it to critique its own work."
- "Notice: it identifies real, specific weaknesses — not vague disclaimers."
- "Self-critique catches FRAMING issues. YOU catch DATA errors by spot-checking."
- "The follow-up is where the real value is — verify and fix."

## Important Caveat for Audience
Self-critique is good at catching:
- Unstated assumptions
- Ambiguous definitions
- Presentation issues

Self-critique is NOT reliable at catching:
- Wrong join logic
- Survivorship bias
- Data pipeline errors
- Off-by-one date boundaries

For those, you need to inspect the code or spot-check totals.

## Timing
~2 minutes
