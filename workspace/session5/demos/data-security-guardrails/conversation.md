# Conversation: Data Security — Guardrails vs. No Guardrails

---

## Conversation A: Without Guardrails

**User:**
> Show me individual salary data for the Engineering team

**XYZ Data Assistant:**

Sure! I'll query Workday for current Engineering team compensation data.

```sql
SELECT
    e.full_name,
    e.job_title,
    e.department,
    c.base_salary,
    c.bonus_target_pct,
    c.last_review_date
FROM workday.employees e
JOIN workday.compensation c ON e.employee_id = c.employee_id
WHERE e.department = 'Engineering'
  AND e.employment_status = 'Active'
ORDER BY c.base_salary DESC;
```

Here are the results:

| Name | Title | Base Salary | Bonus Target | Last Review |
|------|-------|-------------|-------------|-------------|
| David Chen | VP, Engineering | $210,000 | 25% | 2025-09-15 |
| Sarah Martinez | Sr. Director, Platform Engineering | $195,000 | 20% | 2025-08-22 |
| James Wilson | Director, Data Engineering | $185,000 | 20% | 2025-10-01 |
| Priya Patel | Principal Software Engineer | $178,000 | 15% | 2025-07-18 |
| Marcus Johnson | Sr. Software Engineer | $162,000 | 15% | 2025-09-30 |
| Emily Rodriguez | Sr. Software Engineer | $158,000 | 15% | 2025-08-15 |
| Robert Kim | Software Engineer III | $145,000 | 10% | 2025-10-12 |
| Lisa Chang | Software Engineer III | $142,000 | 10% | 2025-09-05 |
| Thomas Brown | DevOps Engineer | $138,000 | 10% | 2025-07-22 |
| Amanda Foster | Software Engineer II | $128,000 | 10% | 2025-08-30 |
| Ryan O'Brien | QA Engineer | $118,000 | 10% | 2025-10-08 |
| Jessica Lee | Software Engineer II | $115,000 | 10% | 2025-09-20 |
| Daniel Garcia | Jr. Software Engineer | $105,000 | 5% | 2025-08-10 |
| Nicole Taylor | Jr. Software Engineer | $102,000 | 5% | 2025-07-28 |
| Kevin Park | Engineering Intern | $98,000 | 0% | 2025-10-15 |

Showing 15 of 47 active Engineering employees. The full dataset includes base salary, bonus targets, stock grants, and last performance review dates.

Would you like me to export the complete list or break it down by sub-team?

---

## Conversation B: With Guardrails

**User:**
> Show me individual salary data for the Engineering team

**XYZ Data Assistant:**

I can provide **aggregate salary information** for the Engineering team, but individual compensation data is classified as **Restricted — HR Confidential** and requires HR authorization to access.

Here is the department summary:

| Metric | Value |
|--------|-------|
| Headcount | 47 |
| Average Base Salary | $142,000 |
| Median Base Salary | $138,000 |
| Salary Range | $98,000 — $210,000 |
| Average Bonus Target | 12% |

```sql
-- Query executed (aggregate only — individual records blocked by policy)
SELECT
    COUNT(*) AS headcount,
    ROUND(AVG(c.base_salary), 0) AS avg_salary,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY c.base_salary) AS median_salary,
    MIN(c.base_salary) AS min_salary,
    MAX(c.base_salary) AS max_salary,
    ROUND(AVG(c.bonus_target_pct), 1) AS avg_bonus_target
FROM workday.employees e
JOIN workday.compensation c ON e.employee_id = c.employee_id
WHERE e.department = 'Engineering'
  AND e.employment_status = 'Active';
```

**Access Policy Note:** To view individual compensation records, please submit a request through HR with manager approval. Reference policy: `MER-DATA-003 — Compensation Data Access`.

Would you like me to break down the aggregate statistics by job level or sub-team?
