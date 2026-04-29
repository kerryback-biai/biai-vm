# Demo: RAG Chunking Failure — Incomplete Answer

## User prompt

> What are the termination penalties in our Apex Industries contract?

---

## Agent reasoning (visible to class)

**Step 1 — Retrieve relevant documents**

Searching document store for: "Apex Industries termination penalty clause"

*Retrieved chunks (top 3 by relevance):*

| Rank | Source | Section | Page | Relevance | Content preview |
|---|---|---|---|---|---|
| 1 | `contracts/apex_industries_msa.pdf` | Section 12.1: "Termination for Convenience" | p. 14 | 0.93 | "Either party may terminate this Agreement..." |
| 2 | `contracts/apex_industries_msa.pdf` | Section 11: "Dispute Resolution" | p. 13 | 0.76 | "Any dispute arising under this Agreement shall be resolved..." |
| 3 | `contracts/apex_industries_msa.pdf` | Section 13: "Survival and Post-Termination" | p. 16 | 0.71 | "The following provisions shall survive termination..." |

**Chunk 1 content (Section 12.1, p. 14):**

> **12.1 Termination for Convenience.** Either party may terminate this Agreement for any reason upon ninety (90) days' prior written notice to the other party, delivered via certified mail or overnight courier to the address specified in Section 15.3. Such notice shall specify the intended termination date, which shall be no earlier than ninety (90) days from the date of delivery. Upon receipt of a valid termination notice, both parties shall continue to perform their obligations under this Agreement through the termination date, including all pending purchase orders accepted prior to the notice date.

**What the agent does NOT see:**

The termination clause continues on page 15, but the chunking boundary fell at the page break. The continuation reads:

> **12.2 Termination Fee.** In the event of termination under Section 12.1 prior to the expiration of the initial three-year term, the terminating party shall pay to the non-terminating party a termination fee equal to fifteen percent (15%) of the remaining contract value, calculated as the pro-rata portion of the minimum annual commitment of $6.8M multiplied by the number of full months remaining in the term. This fee shall be due and payable within thirty (30) days of the termination date.

This chunk (Section 12.2, p. 15) scored 0.64 relevance — below the retrieval threshold of 0.70 — because its text references "Section 12.1" rather than repeating the word "termination penalty" directly, and the embedding captured the fee calculation language more strongly than the termination concept.

**Step 2 — Synthesize answer from retrieved chunks**

---

## Agent response

### Apex Industries — Termination Provisions

Based on the Apex Industries Master Service Agreement (MSA), the termination provisions are as follows:

**Termination for Convenience:** Either party may terminate the agreement for any reason with **90 days' written notice** via certified mail or overnight courier. During the notice period, both parties must continue to fulfill all existing obligations, including pending purchase orders accepted before the notice date.

(Apex Industries MSA, Section 12.1, p. 14)

There are also provisions governing post-termination obligations in Section 13 (survival of confidentiality, indemnification, and payment obligations), but these relate to ongoing duties rather than penalties.

**Sources:**
- *Apex Industries Master Service Agreement*, Section 12.1, p. 14
- *Apex Industries Master Service Agreement*, Section 13, p. 16

---

## What went wrong

The agent's answer is **factually correct but dangerously incomplete**. It accurately reports the 90-day notice requirement but entirely misses the **15% termination fee** — which on a $6.8M annual contract with 18 months remaining would be approximately **$1.53M**.

The failure occurred because:

1. **Chunking split the clause.** Section 12.1 (termination right) and Section 12.2 (termination fee) fell into different chunks at the page boundary between pages 14 and 15.

2. **The fee chunk scored below threshold.** Section 12.2 uses the phrase "termination fee" and references "Section 12.1" but does not repeat "termination penalty" — the exact phrase in the user's question. Its embedding similarity score (0.64) fell below the retrieval threshold (0.70).

3. **The agent didn't know it was missing anything.** The retrieved chunk appeared to fully address the question — it described a termination process with a clear 90-day notice period. There was no signal that a critical financial term existed in an adjacent, unretrieved passage.

4. **The answer looks authoritative.** It includes a citation, quotes the specific section number, and is written with confidence. A busy executive reading this would have no reason to doubt it.

### The $1.53M mistake

If XYZ's CFO relied on this answer to terminate the Apex contract — expecting to walk away with just 90 days' notice — the company would be invoiced $1.53M in termination fees that this analysis never mentioned. The AI gave a precise, well-cited, completely confident answer that was missing the most expensive piece of information.
