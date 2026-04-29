# Chunking Failure — Key Takeaways

## What this demo shows

A realistic RAG failure where the AI returns a confident, well-cited, factually correct answer that is missing a $1.53M termination fee — because the relevant clause was split across two chunks at a page boundary, and the second chunk fell below the retrieval threshold.

## The failure anatomy

```
Page 14 (retrieved, score 0.93):
  Section 12.1 — "Either party may terminate with 90 days written notice..."

--- chunk boundary / page break ---

Page 15 (NOT retrieved, score 0.64):
  Section 12.2 — "...subject to a termination fee of 15% of remaining contract value"
```

The embedding model scored the fee clause at 0.64 because it discusses "termination fee" and "Section 12.1" rather than using the user's phrase "termination penalties." The retrieval threshold was 0.70.

## Why this is dangerous

| Property | This answer |
|---|---|
| Factually correct? | Yes — everything stated is accurate |
| Well-cited? | Yes — section number, page number, document name |
| Confident tone? | Yes — no hedging or uncertainty |
| Complete? | **No** — missing the $1.53M fee |
| Detectable as incomplete? | **No** — no signal that anything is missing |

This is the worst kind of AI error: one that looks exactly like a correct answer. The user has no reason to question it.

## Teaching points

- **Chunking is a design decision with financial consequences.** How you split documents determines what the AI can and cannot find. Page-based chunking is simple but breaks mid-clause. Sentence-based chunking loses context. There is no perfect strategy.
- **Retrieval thresholds create silent omissions.** The fee clause existed in the vector store — it just scored 0.01 below the threshold. Raising the threshold reduces noise; lowering it increases recall. This tradeoff is invisible to the end user.
- **Confidence is not completeness.** The AI cannot distinguish between "I found the answer" and "I found part of the answer." It has no awareness of what it didn't retrieve.
- **Mitigation strategies exist but have costs:**
  - Overlapping chunks (e.g., 200-token overlap) would have caught this — but increase storage and retrieval time
  - Semantic chunking (splitting at paragraph/section boundaries) is better than fixed-size — but requires document structure parsing
  - Asking the AI to flag when retrieved passages seem to reference unretrieved sections — imperfect but useful
  - Always returning the full surrounding pages rather than just the matched chunk — higher cost, better safety
- **This is why verification matters.** The maker-checker pattern applies here too: any high-stakes document AI answer should be verified against the source document before action is taken.

## Connection to Session 5

In Session 5 we will learn that AI outputs need verification before they drive decisions. This demo shows why. The failure mode isn't a hallucination — it's an omission caused by infrastructure (chunking), not by the language model. No amount of prompt engineering fixes this. The defense is process: verify contract AI answers against the actual document before making a $1.53M decision.
