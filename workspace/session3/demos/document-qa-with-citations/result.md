# Document Q&A — Key Takeaways

## What this demo shows

The AI assistant retrieves information from XYZ's internal document corpus — employee handbook, vendor contracts, board minutes, strategic plans — and answers natural-language questions with specific citations (document name, section, page number).

## Three question types demonstrated

1. **Policy lookup** (remote work) — single document with a division-specific override requiring synthesis across two sources
2. **Structured data extraction** (vendor renewals) — pulling tabular data from a registry, filtering by date, and adding procedural context from a separate policy document
3. **Multi-document synthesis** (board approval) — assembling a narrative across board minutes from two quarters plus the strategic plan

## Teaching points

- **Citations matter.** Every claim traces to a specific document, section, and page. This is what makes document AI usable in a corporate setting — the user can verify.
- **Cross-document reasoning.** Question 3 required the agent to connect information across three documents and two time periods. A keyword search would have found one of these; the AI found and synthesized all three.
- **Procedural awareness.** In Question 2, the agent didn't just list renewals — it flagged the 120-day review requirement and noted that one contract had already auto-renewed. This is the kind of insight that gets lost when policies live in unread PDFs.
- **Limitations are real.** The agent only knows what's in the document corpus. If a policy was communicated via email but never added to the handbook, it doesn't exist to the AI.
