# Result: Date Format Mismatch

## What the Agent Returned

| Division | Q4 2025 Revenue |
|----------|----------------|
| Industrial | $62,400,000 |
| Energy | $35,200,000 |
| Safety | $24,800,000 |
| **Total** | **$122,400,000** |

Industrial and Safety numbers are correct (Salesforce uses proper `DATE` types). Energy is wrong.

---

## The Bug: VARCHAR Date Comparison

The Legacy CRM stores `close_date` as `VARCHAR` in `MM/DD/YYYY` format. The agent's SQL uses **string comparison**:

```sql
WHERE close_date >= '10/01/2025'
  AND close_date <= '12/31/2025'
```

String comparison is **lexicographic** (character by character, left to right). This means:

| Date String | Compared to `'10/01/2025'` | Included? | Correct? |
|-------------|---------------------------|-----------|----------|
| `'10/15/2025'` | `'10' >= '10'` | Yes | Yes |
| `'11/08/2025'` | `'11' >= '10'` | Yes | Yes |
| `'12/22/2025'` | `'12' >= '10'` | Yes | Yes |
| `'01/14/2025'` | `'01' >= '10'`? No — `'0' < '1'` | No | Correct (Jan is not Q4) |

So far so good. But the `<= '12/31/2025'` upper bound is the problem:

| Date String | Compared to `'12/31/2025'` | Included? | Correct? |
|-------------|---------------------------|-----------|----------|
| `'11/30/2025'` | `'11' <= '12'` | Yes | Yes |
| `'12/15/2025'` | `'12' <= '12'`, then `'15' <= '31'` | Yes | Yes |
| `'11/05/2025'` | `'11' <= '12'` | Yes | Yes |

The real failure is in the agent's post-processing Python code. After pulling the raw data via SQL, the agent parsed the `VARCHAR` dates into proper `datetime` objects for aggregation — but used the wrong format string:

```python
# Agent's post-processing
from datetime import datetime
parsed = datetime.strptime('11/03/2025', '%d/%m/%Y')  # Reads as March 11!
```

The Legacy CRM stores dates as `MM/DD/YYYY`, but the agent used `%d/%m/%Y` (day-first). For ambiguous dates where the day value is <= 12 (e.g., `11/03`, `12/05`, `10/08`), the parser swapped month and day. Transactions on `11/03/2025` (November 3), `11/05/2025` (November 5), and `12/06/2025` (December 6) were reassigned to March, May, and June — falling outside Q4 in the final aggregation.

---

## Correct vs. Reported

| Division | Agent's Answer | Correct Value | Error |
|----------|---------------|---------------|-------|
| Industrial | $62,400,000 | $62,400,000 | -- |
| Energy | $35,200,000 | $37,500,000 | -$2,300,000 |
| Safety | $24,800,000 | $24,800,000 | -- |
| **Total** | **$122,400,000** | **$124,700,000** | **-$2,300,000** |

Energy revenue is understated by **$2.3M (6.1%)**.

---

## Key Takeaway

The agent produced no errors and no warnings. The result looks plausible — Energy is the second-largest division, and $35.2M is in the right ballpark. But $2.3M vanished because dates stored as strings in a legacy system were parsed inconsistently. This is the kind of bug that survives in production for months because the numbers always look "close enough."
