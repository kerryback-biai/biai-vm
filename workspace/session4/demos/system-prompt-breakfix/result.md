# Result: System Prompt Break/Fix

## Side-by-side comparison

### With full system prompt (correct)

| Division | Revenue | Headcount | Rev/Employee |
|---|---|---|---|
| Industrial | $63.4M | 308 | $205,886 |
| Energy | $37.9M | 220 | $172,234 |
| Safety | $12.2M | 106 | $115,137 |

### Without join key documentation (incorrect)

| Division | Revenue | Headcount |
|---|---|---|
| Industrial | $81.2M | 308 |
| Energy | $48.7M | 220 |
| Safety | $17.9M | 106 |

### What broke

| Problem | With full prompt | Without join keys |
|---|---|---|
| Revenue source | CRM orders (correct) | Mixed: corporate actuals + unfiltered HubSpot deals |
| Safety revenue | $12.2M (closed-won deals only) | $17.9M (all deals including lost/open — 47% overstated) |
| Industrial revenue | $63.4M (Salesforce orders) | $81.2M (NetSuite accrual figure — different metric) |
| Revenue/employee | Computed and explained | Not computed |
| Source transparency | Each system named | No source attribution |
| Sanity check | Consistent methodology | Numbers from different systems compared as if equivalent |

### The lesson

The system prompt is not just documentation. It is the agent's understanding of the business. Without cross-system join keys and division-to-system mappings, the agent does not fail loudly — it produces **plausible-looking wrong answers**. The table is well-formatted, the language is confident, and every number is wrong. This is the most dangerous failure mode in enterprise AI.
