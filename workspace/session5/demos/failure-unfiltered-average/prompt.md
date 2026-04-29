# Demo: Failure — Unfiltered Average Deal Size

## Session Context
Session 5 — Deployment and Governance (Failure #1)

## Prompt
> What is our average deal size this quarter?

## Purpose
Demonstrate how a technically correct SQL query can produce a misleading business answer. The agent calculates an average across all deal stages — won, lost, and open — when the user almost certainly means closed-won deals only. The result looks plausible, so no one questions it.

## What to Watch For
- The SQL has no `WHERE` clause filtering on deal stage
- The returned average ($48K) is ~39% lower than the closed-won average ($78K)
- Lost deals tend to be smaller (prospects who never committed); open deals skew early-stage
- The number looks reasonable enough that a manager might use it in a board deck without checking
