# Demo: Document Q&A with Citations

## Question 1

> What is XYZ's policy on remote work for the Energy Division?

---

### Agent reasoning (visible to class)

**Step 1 — Retrieve relevant documents**

Searching document store for: "remote work policy Energy Division"

*Retrieved chunks:*
- `employee_handbook.pdf` — Section 4.3: "Flexible Work Arrangements" (pp. 28-29, relevance: 0.94)
- `employee_handbook.pdf` — Section 4.1: "Standard Work Hours" (p. 26, relevance: 0.81)
- `energy_division_addendum.pdf` — Section 2: "Division-Specific Policies" (p. 3, relevance: 0.88)

**Step 2 — Synthesize answer**

Based on the retrieved documents, here is XYZ's remote work policy as it applies to the Energy Division:

**General Policy:** XYZ's Employee Handbook permits up to 2 days of remote work per week for all corporate and administrative staff, subject to manager approval and a 30-day trial period (Employee Handbook, Section 4.3, p. 28).

**Energy Division Exception:** The Energy Division Addendum imposes additional restrictions. Field operations staff, warehouse personnel, and on-site technical support roles are classified as "location-essential" and are not eligible for remote work. For eligible Energy Division employees (account managers, analysts, division finance), remote work is limited to 1 day per week due to the division's requirement for in-person coordination with field teams (Energy Division Addendum, Section 2, p. 3).

**Approval Process:** All remote work arrangements require written approval from the division VP and must be reviewed quarterly. Employees must maintain a dedicated home workspace and be available during core hours of 8:00 AM - 3:00 PM Central Time (Employee Handbook, Section 4.3, p. 29).

**Sources:**
- *Employee Handbook* (v2025.2), Section 4.3, pp. 28-29
- *Energy Division Addendum* (effective January 2025), Section 2, p. 3

---

## Question 2

> Which vendor contracts are up for renewal in Q2 2026?

---

### Agent reasoning (visible to class)

**Step 1 — Retrieve relevant documents**

Searching document store for: "vendor contract renewal Q2 2026"

*Retrieved chunks:*
- `vendor_contract_registry.xlsx` — "Active Contracts Summary" (Sheet 1, rows 1-45, relevance: 0.96)
- `procurement_policy.pdf` — Section 7: "Contract Renewal Procedures" (pp. 15-16, relevance: 0.78)
- `board_minutes_2025_Q4.pdf` — Item 6: "Procurement Update" (p. 9, relevance: 0.72)

**Step 2 — Extract and filter**

Filtering the vendor contract registry for contracts with renewal dates between April 1 and June 30, 2026.

**Q2 2026 Vendor Contract Renewals:**

| Vendor | Contract Type | Division | Annual Value | Renewal Date | Term |
|---|---|---|---|---|---|
| Apex Industries | Master Service Agreement | Industrial | $6.8M | April 15, 2026 | 3-year |
| Parker Hannifin | Supply Agreement | Industrial | $3.1M | May 1, 2026 | 2-year |
| Honeywell Process Solutions | Technology License | Energy | $1.9M | May 22, 2026 | 1-year |
| Grainger | Distribution Agreement | Safety | $2.4M | June 1, 2026 | 2-year |
| National Oilwell Varco | Preferred Supplier | Energy | $4.5M | June 30, 2026 | 3-year |

**Total at risk:** $18.7M in annual contract value across 5 vendors.

**Note:** Per XYZ's Procurement Policy (Section 7, p. 15), contracts over $2M require a 120-day advance review by the Procurement Committee. The Apex Industries and Parker Hannifin renewals are within that window now. The Honeywell license auto-renews unless notice is given 60 days prior (March 23, 2026), which has already passed — this contract will auto-renew at current terms (Vendor Contract Registry, Notes column).

**Sources:**
- *Vendor Contract Registry* (updated February 2026), Sheet 1
- *Procurement Policy* (v2024.1), Section 7, pp. 15-16

---

## Question 3

> What did the board approve regarding the Safety Division expansion?

---

### Agent reasoning (visible to class)

**Step 1 — Retrieve relevant documents**

Searching document store for: "board approval Safety Division expansion"

*Retrieved chunks:*
- `board_minutes_2025_Q4.pdf` — Item 3: "Safety Division Strategic Plan" (pp. 4-6, relevance: 0.97)
- `board_minutes_2026_Q1.pdf` — Item 2: "Capital Expenditure Approvals" (pp. 2-3, relevance: 0.93)
- `strategic_plan_2026.pdf` — Section 5.2: "Safety Division Growth Initiatives" (pp. 22-24, relevance: 0.86)

**Step 2 — Synthesize across documents**

The board addressed the Safety Division expansion across two consecutive meetings:

**Q4 2025 Board Meeting (October 17, 2025):**
The board reviewed and approved in principle the Safety Division's proposal to expand into the Gulf Coast region, subject to final budget approval. Key terms approved:
- New regional distribution center in Houston, TX (40,000 sq ft lease)
- Hiring plan for 18 FTEs: 1 regional manager, 4 account executives, 8 warehouse staff, 3 delivery drivers, 2 admin support
- Target launch date: Q3 2026
- Projected first-year revenue: $8.2M with breakeven in 14 months

(Board Minutes Q4 2025, Item 3, pp. 4-5)

**Q1 2026 Board Meeting (January 22, 2026):**
The board gave final approval for $3.4M in capital expenditure:
- $1.8M — warehouse fit-out and racking systems
- $0.9M — fleet (4 delivery vehicles)
- $0.4M — IT infrastructure (HubSpot CRM expansion, inventory management)
- $0.3M — hiring and training costs

The board also required quarterly progress reports to the Operations Committee and set a gate review at 6 months post-launch. If the Houston center does not reach 60% of projected revenue by Month 6, the board directed management to present a revised plan or exit strategy.

(Board Minutes Q1 2026, Item 2, pp. 2-3)

**Strategic Context:** The 2026 Strategic Plan identifies the Safety Division expansion as one of three "Horizon 1" growth initiatives, alongside Energy Division digital transformation and the cross-division enterprise pricing program (Strategic Plan 2026, Section 5.2, p. 22).

**Sources:**
- *Board Meeting Minutes, Q4 2025* (October 17, 2025), Item 3, pp. 4-6
- *Board Meeting Minutes, Q1 2026* (January 22, 2026), Item 2, pp. 2-3
- *Strategic Plan 2026*, Section 5.2, pp. 22-24
