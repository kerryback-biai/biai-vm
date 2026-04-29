# Result: Entity Resolution Double-Count

## What the Agent Returned

| Metric | Value |
|--------|-------|
| Total raw records | 1,017 |
| After deduplication | **847** |
| Duplicates removed | 170 |

The agent stated this with full confidence: "XYZ has 847 unique customers across all three divisions."

---

## What the Real Number Is

A manual entity resolution audit (using company tax IDs, addresses, and domain names as ground truth) shows **~690 unique customers**. The agent overcounted by **157 customers (23%)**.

---

## What the Fuzzy Matching Caught

The 85% similarity threshold successfully merged obvious variants:

| Name Variant A | Name Variant B | Similarity | Merged? |
|---------------|---------------|-----------|---------|
| Acme Corp | ACME Corp | 100% | Yes |
| Baker Hughes | baker hughes | 100% | Yes |
| Texas Instruments Inc | Texas Instruments Inc. | 97% | Yes |
| Dow Chemical | DOW CHEMICAL | 100% | Yes |

---

## What the Fuzzy Matching Missed

These are real duplicates (same company) that the agent counted as separate customers:

| Industrial CRM | Energy CRM | Safety CRM | Similarity | Merged? |
|---------------|------------|------------|-----------|---------|
| Acme Corp | ACME Corporation | Acme Corp. | 79% / 93% | Partial — counted as 2 |
| Baker Hughes | Baker Hughes Energy | BHI | 82% / 31% | No — counted as 3 |
| ConocoPhillips | Conoco Phillips Co | COP | 78% / 26% | No — counted as 3 |
| Dow Chemical | Dow Inc | Dow Chemical Company | 64% / 89% | Partial — counted as 2 |
| Schlumberger | SLB | Schlumberger Ltd | 33% / 89% | Partial — counted as 2 |
| Honeywell International | Honeywell | Honeywell Intl Inc | 76% / 82% | Partial — counted as 2 |
| 3M Company | 3M | 3M Co | 67% / 78% | No — counted as 3 |
| General Electric | GE | GE Industrial | 33% / 56% | No — counted as 3 |
| Exxon Mobil | ExxonMobil Corp | Exxon | 74% / 63% | No — counted as 3 |
| Caterpillar Inc | CAT | Caterpillar | 33% / 89% | Partial — counted as 2 |

The pattern: **ticker symbols, abbreviations, legal suffixes (Inc/Corp/Ltd/Co), and name changes** all break fuzzy string matching at the 85% threshold.

---

## Why 85% Was the Wrong Threshold

| Threshold | Duplicates Found | False Merges | Unique Count |
|-----------|-----------------|-------------|-------------|
| 95% | 87 | 0 | 930 |
| 85% (agent's choice) | 170 | 2 | 847 |
| 75% | 248 | 11 | 769 |
| 65% | 310 | 34 | 707 |

No single threshold solves this problem. At 85%, the agent misses abbreviation-based duplicates. At 65%, it starts merging companies that are actually different ("Atlas Steel" and "Atlas Energy" at 71% similarity).

---

## Key Takeaway

The agent reported "847 unique customers" as a fact. It did not say "approximately," did not provide a confidence range, and did not flag that fuzzy string matching on company names is inherently unreliable. The real number is ~690 — a 23% overcount. Entity resolution across siloed systems requires more than string similarity: it needs tax IDs, domain matching, address normalization, and human review. An executive using "847" for strategic planning is making decisions on a number that is significantly inflated.
