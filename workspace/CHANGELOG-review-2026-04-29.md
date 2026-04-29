# Workspace & Slides Review & Fixes — April 29, 2026

All exercises, demos, and slide decks were reviewed by parallel analysis agents. Issues were categorized by severity and fixed in place. This document records every change made.

---

## High Priority Fixes

### 1. Session 2 Exercise: Impossible Q4 2025 comparison
**File:** `session2/exercises/session2_dashboard.md`
**Issue:** Exercise 2 asked "Compare Q4 2024 to Q4 2025" but the sales data ends June 2025 — Q4 2025 doesn't exist.
**Fix:** Changed to "Compare H1 2024 to H1 2025 across all metrics."

### 2. Session 6 Exercise: Wrong tax rates in portfolio rebalancing solution
**File:** `session6/exercises/portfolio_rebalancing.py`
**Issue:** Solution used 15% long-term / 24% short-term tax rates, but the exercise prompt (`session6_portfolio_exercises.md`) specifies 20% long-term / 37% short-term (top federal rates).
**Fix:** Updated rates to 20%/37%. Also fixed the loss offset logic to apply the correct rate by character (long-term losses at 20%, short-term losses at 37%) instead of a flat 15% benefit rate.

### 3. Session 5 Demos: Wrong session numbers (×3)
**Files:**
- `session5/demos/failure-unfiltered-average/prompt.md`
- `session5/demos/failure-silent-date-format/prompt.md`
- `session5/demos/failure-entity-double-count/prompt.md`

**Issue:** All three said "Session 6 — AI Failures and Limitations" but live in the `session5` directory.
**Fix:** Changed to "Session 5 — Deployment and Governance" in all three files.

### 4. Session 7 Demo: Unrealistic dollar figures for telecom data
**File:** `session7/demos/model-evaluation/prompt.md`
**Issue:** Used "$42K average annual contract value" and "$500 retention offer" — B2B figures applied to a B2C telecom dataset where monthly charges are $20-$100. Also inconsistent with the churn-classification demo which uses $50/$75.
**Fix:** Changed to "$50 retention offer" and "$75 average monthly revenue per customer (i.e., ~$900/year)" to match the telecom dataset and be consistent with the churn-classification demo.

### 5. Session 4 Demos: Wrong session labels (×2)
**Files:**
- `session4/demos/agent-loop-explained/conversation.md`
- `session4/demos/system-prompt-breakfix/conversation.md`

**Issue:** Both said "Session 3" but are in the `session4` directory.
**Fix:** Changed to "Session 4" in both files.

---

## Medium Priority Fixes

### 6. Session 3 README: Demo 4 description mismatch
**File:** `session3/demos/README.md`
**Issue:** Described Demo 4 as "Structured Extraction from Contracts" with "Which vendor contracts are up for renewal?" but the actual demo is about RAG chunking failure with termination penalties.
**Fix:** Updated description to "RAG Chunking Failure" with the actual prompt and a summary of what the demo demonstrates ($1.53M fee missed due to chunking).

### 7. Session 8 Demo: Incorrect session cross-references
**File:** `session8/demos/ai-as-thinking-partner/result.md`
**Issue:** Referenced "Session 3: Agent loop" (no session 3 demos exist) and "Session 7: Document AI" (Session 7 is Predictive Modeling).
**Fix:** Updated to: Session 2 (data analysis), Session 4 (agent loop), Session 5 (reliability awareness), Session 7 (predictive modeling).

### 8. Session 5 Demo: Numerical inconsistency in unfiltered-average
**Files:**
- `session5/demos/failure-unfiltered-average/result.md`
- `session5/demos/failure-unfiltered-average/prompt.md`

**Issue:** The breakdown (134×$78,400 + 89×$28,100 + 89×$22,500 = $15,009,000) didn't match the stated agent total of $14,726,400 (312×$47,200). Off by ~$283K.
**Fix:** Adjusted the agent's reported average to $48,100 and total to $15,006,200 to be consistent with the breakdown. The teaching point (agent ~39% lower than $78,400 closed-won average) is preserved.

### 9. Session 5 Demo: Split-bug narrative in date-format failure
**File:** `session5/demos/failure-silent-date-format/result.md`
**Issue:** The explanation jumped between two different bugs (VARCHAR string comparison in SQL and Python strptime format mismatch), creating a confusing narrative.
**Fix:** Streamlined to focus on the Python `strptime` format mismatch as the primary failure, removing the awkward mid-section that hedged between both bugs.

### 10. Session 4 Exercise: Port conflict
**File:** `session4/exercises/session4_web_app.py`
**Issue:** Used port 8000, which conflicts with the lab's `login-app.py` running on the same port.
**Fix:** Changed to port 8080 (both in the code and the docstring).

### 11. Session 4 Exercises: Broken relative paths (×3)
**Files:**
- `session4/exercises/session4_hello_agent.py`
- `session4/exercises/session4_multi_system.py`

**Issue:** Scripts in `exercises/` referenced `data/salesforce/...` paths, which only resolve if CWD is `session4/`. Running `python session4_hello_agent.py` from the `exercises/` directory would fail.
**Fix:** Changed all data paths to `../data/salesforce/...` and `../data/workday/...` so they resolve correctly when run from the `exercises/` directory.

---

## Low Priority Fixes

### 12. Session 3 Demo: Wrong cross-reference in documents-plus-database
**File:** `session3/demos/documents-plus-database/result.md`
**Issue:** Referenced "Session 2 demo" for the GE fuzzy merge, but that demo is in Session 3.
**Fix:** Changed to "Earlier in this session."

### 13. Session 3 Demo: Unrealistic fuzzy match score
**File:** `session3/demos/cross-system-fuzzy-merge/result.md`
**Issue:** Showed a fuzzy match score of 100 for "General Electric" vs "GE Safety Division." Real `fuzz.token_sort_ratio` would produce ~55-65.
**Fix:** Changed score to 62.

### 14. Session 6 Demo: Wrong data path
**File:** `session6/demos/what-if-scenarios/prompt.md`
**Issue:** Referenced `~/workspace/data/portfolio/` which doesn't account for the session6 subdirectory.
**Fix:** Changed to `data/portfolio/` with note "(in the session6 folder)."

### 15. Session 3 Demo: Unclear forward-reference to Session 6
**File:** `session3/demos/structured-extraction-contracts/result.md`
**Issue:** Referenced "Session 6" for the maker-checker pattern. The concept is introduced in Session 2 and the session numbering was wrong.
**Fix:** Changed "This is why Session 6 matters" to "This is why verification matters" and updated "Connection to Session 6" to "Connection to Session 5" (where deployment and governance are covered).

### 16. Session 2 Exercise: Missing comment about vintage risk simplification
**File:** `session2/exercises/loan_risk_analysis.py`
**Issue:** The vintage risk flag only checks origination date, but the policy also requires "no payment history update in the last 6 months." The dataset lacks this column.
**Fix:** Added a comment explaining the simplification.

### 17. Session 7 Exercise: Overly specific feature importance expectation
**File:** `session7/exercises/session7_churn_exercises.md`
**Issue:** Said "contract type, tenure, monthly charges should be top" but the actual model shows TotalCharges and InternetService ranking higher than contract type.
**Fix:** Softened to "tenure, charges, and contract type should be prominent."

### 18. Session 3 Exercise: Missing platform clarification
**File:** `session3/exercises/session3_enterprise_queries.md`
**Issue:** Said "Platform: XYZ Corp Custom Chatbot" with no note that this is a separate platform, potentially confusing students who expect to use the AI Lab.
**Fix:** Added "(separate web app, not the AI Lab terminal)."

---

## Items Reviewed — No Changes Needed

These were checked and confirmed correct:

- **Session 2 data files:** All CSVs match schema descriptions (837 transactions, 50 customers, 30 employees)
- **Session 2 loan risk solution:** Tier classification, state regulations, and reserve calculations all match policy documents
- **Session 4 parquet schemas:** All 5 files match template descriptions exactly
- **Session 6 workover scheduling:** All 20 wells match data file; travel time formula, optimization, and histogram are correct
- **Session 7 churn data:** 7,043 rows, 26.5% churn rate, 11 blank TotalCharges — all match
- **All Session 1 demos:** Clean and ready for live use
- **All Session 2 demo Python code:** Correct and produces expected charts
- **Session 3 conversation scripts:** Realistic agent reasoning and error recovery
- **Session 4 three-iteration-drafts:** Pedagogically excellent, no issues
- **Session 5 data-security-guardrails:** Aggregate stats consistent, great contrast demo
- **Session 6 multi-objective-tradeoffs:** Best pedagogical demo in Session 6
- **Session 8 ai-as-thinking-partner:** Outstanding capstone demo

---

---

## Slide Deck Fixes (biai-course/slides/)

### 19. Session 2 slides: Q4 2025 comparison matches fixed exercise
**File:** `biai-course/slides/2_ai-versus-dashboards.qmd`
**Issue:** Slide listed "Compare Q4 2024 to Q4 2025" in the "Questions No Dashboard Can Answer" section — same impossible comparison as the exercise.
**Fix:** Changed to "Compare H1 2024 to H1 2025" to match the fixed exercise prompt.

### 20. Session 4 slides: Data path references (×4)
**File:** `biai-course/slides/4_building-ai-agents.qmd`
**Issue:** Four references to `~/workspace/data/` for the parquet files, but the actual workspace structure puts them in `~/workspace/session4/data/`.
**Fix:** Changed all four occurrences to `~/workspace/session4/data/` (in the demo narration, demo instructions, exercise prompt, and exercise notes).

### 21. Session 5 slides: Unfiltered average percentage
**File:** `biai-course/slides/5_deployment-and-governance.qmd`
**Issue:** Speaker notes said "forty percent lower than reality" for the unfiltered average demo, but the workspace was corrected to ~39%.
**Fix:** Changed to "nearly 40 percent lower than reality" for consistency.

### 22. Session 6 slides: Portfolio data path
**File:** `biai-course/slides/6_decision-making-with-ai.qmd`
**Issue:** Referenced `~/workspace/data/portfolio/` but the actual workspace path is `~/workspace/session6/data/portfolio/`.
**Fix:** Changed to `~/workspace/session6/data/portfolio/`.

---

---

## Cross-Check Fixes (Round 2)

### 23. Session 2 slides: Data path `~/workspace/data/dashboard/` → `~/workspace/session2/data/`
**File:** `biai-course/slides/2_ai-versus-dashboards.qmd` (all occurrences)
**Issue:** Slides referenced a `data/dashboard/` subdirectory that doesn't exist. Actual workspace structure is `session2/data/`.

### 24. Session 2 demos README: "Q4 vs Q4" → "H1 2024 vs H1 2025"
**File:** `workspace/session2/demos/README.md`
**Issue:** Still referenced old Q4 comparison after the exercise was fixed.

### 25. Session 3 slides: Handbook citation updated to match demo
**File:** `biai-course/slides/3_navigating-diverse-data-sources.qmd`
**Issue:** Slides said "Employee Handbook, Section 4.2, p. 12" and "Energy Division Policies, Section 2.1". Demo says "Section 4.3, pp. 28-29" and "Energy Division Addendum, Section 2".
**Fix:** Changed slides to match workspace demo citations.

### 26. Session 3 slides: GE shortfall $400K → $404K, renewal 90 → 92 days
**File:** `biai-course/slides/3_navigating-diverse-data-sources.qmd` (3 locations)
**Issue:** Slides rounded the shortfall and deadline; workspace demo has exact figures.
**Fix:** Updated to $404K and 92 days throughout.

### 27. Session 3 slides: Multi-division revenue percentage ~11% → 11.4%
**File:** `biai-course/slides/3_navigating-diverse-data-sources.qmd`
**Issue:** Slides said "~11%", workspace demo result says "11.4%".

### 28. Session 4 slides: Last remaining `~/workspace/data/` path fix
**File:** `biai-course/slides/4_building-ai-agents.qmd` (line 631 in speaker notes)
**Issue:** Narration script still had old path without `session4/`.

### 29. Session 4 slides + exercise: "support tickets" test question replaced
**Files:** `biai-course/slides/4_building-ai-agents.qmd`, `workspace/session4/exercises/session4_build_agent.md`
**Issue:** "Which customers have the most support tickets?" cannot be answered — no Zendesk data in session 4.
**Fix:** Changed to "Which sales rep has the highest total order value?" (answerable from sf_orders + wd_workers via wd_system_ids).

### 30. Session 7 slides: All simulated model metrics updated
**File:** `biai-course/slides/7_predictive-modeling-with-ai.qmd` (14 locations)
**Issue:** Simulated recall (72.7%) and F1 (69.3%) were far above workspace expected ranges (recall 53-55%, F1 59-61%). Lost customer value was $1,200/year but workspace demos use $75/month ($900/year).
**Fix:** Updated confusion matrix (TN=930, FP=106, FN=168, TP=205), accuracy (80.6%), precision (65.9%), recall (55.0%), F1 (59.9%), training (83.5%), CV (79.2% ± 2.1%). Changed lost customer value to $900/year. Recalculated all derived figures.

### 31. Session 5 workspace: conversation.md numbers aligned with result.md
**File:** `workspace/session5/demos/failure-unfiltered-average/conversation.md`
**Issue:** Still had old $47,200 average / $14,726,400 total while result.md was corrected to $48,100 / $15,006,200.

### 32. Session 6 workspace: Demo prompts aligned with exercises
**Files:** `workspace/session6/demos/what-if-scenarios/prompt.md`, `workspace/session6/demos/multi-objective-tradeoffs/prompt.md`, `workspace/session6/demos/README.md`
**Issue:** Demo used $2,000 threshold (exercises say $1,000) and NFLX (exercises say AAPL).
**Fix:** Changed to $1,000 and AAPL throughout.

### 33. Session 8 workspace: Plenary timing and course arc
**Files:** `workspace/session8/exercises/session8_capstone.md`, `workspace/session8/demos/ai-as-thinking-partner/result.md`
**Issue:** Capstone said "25 minutes" for plenary but 5 × 8 min = 40 min. Result.md omitted Session 6 from course arc.
**Fix:** Changed to 40 minutes. Added Session 6 to course arc.

### 34. Workspace CLAUDE.md: Added missing sessions
**File:** `workspace/CLAUDE.md`
**Issue:** Only listed sessions 2, 4, 6, 7. Sessions 1, 3, 5, 8 directories exist but were undocumented.
**Fix:** Added sections for sessions 3, 5, and 8. Updated header to reference all sessions.

---

## Known Limitations (Not Fixed)

- **Session 6 `portfolio_rebalancing.py` line 65:** Hardcoded `datetime(2026, 4, 28)` for holding period calculation. Will need updating for future cohorts.
- **Session 6 `session6_workover_scheduling.md`:** Title says "Exercise 5" in a session 6 folder. May be intentional global numbering across the course. Workover exercise has no corresponding coverage in the Session 6 slides (appears to be supplementary material).
- **Session 4 full-reporting-pipeline demo:** Says "634 employees" without noting Corporate headcount exclusion; ~$500M company description vs ~$113M in CRM data is not reconciled. Both are acceptable in context. Slides and demo README say "6 systems" but conversation.md queries 7 distinct systems.
- **Session 2 slides vs exercise:** Iteration and verification prompt wording differs (slides are more detailed for instructor use). Intentional — slides serve as instructor guide, exercises are student-facing.
- **Session 3 chunking failure:** Slides reference "Atherton case" ($1.5M) as a reading assignment; workspace demo uses "Apex Industries" ($1.53M). These appear to be intentionally separate (case study vs demo), but the similar scenario could confuse students.
- **Session 1 slides vs workspace:** Slides script 2 demos; workspace has 4 fully developed demos. The extra demos (interactive artifact sliders, multi-deliverable web search) are available for instructor use but not scripted in the slides.
- **Session 6 demo `portfolio-optimization/prompt.md`:** Adds "No more than 20 trades total" as priority #4, not present in slides or exercises. This is additional instructor demo content.
- **Session 4 exercise Python files:** Use relative paths (`../data/`) that assume CWD is the `exercises/` subdirectory. Slides reference `~/workspace/session4/data/` (absolute). Both work in their respective contexts.
