# Business Intelligence & AI — Lab Workspace

## Environment
- Python 3, Node.js, and common data libraries are pre-installed
- The Anthropic API key is already set in the environment
- Skills for creating Word (.docx), Excel (.xlsx), and PowerPoint (.pptx) documents are installed
- Exercises and demos are organized by session: `session1/` through `session8/`
- Each session folder has a `data/` directory with the datasets for that session

## Session 2: AI vs Dashboards

**Data** in `session2/data/`:
- `sales.csv` — 837 transactions: transaction_id, date, customer_name, product_line, amount, region, sales_rep
- `customers.csv` — 50 customers: customer_id, customer_name, industry, region, acquisition_date, status, annual_contract_value
- `employees.csv` — 30 employees: employee_id, first_name, last_name, department, division, hire_date, role, salary_band
- `ETF-returns.xlsx` — Monthly returns for SPY, GLD, IEF, EFA (2005-present)
- `loan-risk-analysis/` — 220 loans (loan_tape.xlsx), state regulations (PDF), risk policy (Word doc)

Company: Acme Corp, a mid-size B2B industrial supplier. Product lines: Industrial Products, Technical Services, Safety & Compliance. Regions: South, Northeast, Midwest, West.

## Session 3: Navigating Diverse Data Sources

Demos only (no local data). All exercises run on the XYZ Corp Custom Chatbot (separate web app, not the AI Lab terminal). Demos in `session3/demos/` are pre-scripted conversation transcripts for instructor reference.

## Session 4: Building AI Agents

**Data** in `session4/data/`: XYZ Corp, a $500M B2B industrial distributor (3 divisions: Industrial, Energy, Safety).

**Salesforce CRM** (`data/salesforce/`):
- `sf_accounts.parquet` — 120 accounts: AccountId, AccountName, Industry, BillingState, OwnerId, AnnualRevenue, Type
- `sf_orders.parquet` — 585 orders (2023-2025): OrderId, AccountId, OpportunityId, OrderDate, TotalAmount, Status

**Workday HR** (`data/workday/`):
- `wd_workers.parquet` — 100 employees: worker_id, first_name, last_name, division, department, job_title, status
- `wd_compensation.parquet` — 100 records: comp_id, worker_id, effective_date, base_pay, bonus_target_pct, bonus_actual
- `wd_system_ids.parquet` — 45 mappings: worker_id, system_name, external_id (maps Workday worker_id to Salesforce OwnerId)

Query parquet files with DuckDB: `duckdb.sql("SELECT * FROM read_parquet('data/salesforce/sf_accounts.parquet')")`
Use `anthropic` Python package for API calls.

## Session 5: Deployment and Governance

Discussion and writing exercises only (no local data). Exercises in `session5/exercises/`. Demos in `session5/demos/` are pre-scripted failure scenarios for instructor reference.

## Session 6: Decision-Making with AI

**Data** in `session6/data/`:

- `workover_rig_data.md` — 20 oil wells, 3 rigs, travel times, daily production losses
- `portfolio/portfolio_lots.xlsx` — 167 tax lots: Date, Ticker, Sector, Industry, Size, Shares, Price per Share, Cost
- `portfolio/client_info.md` — Margaret and David Chen, ~$500K taxable account, target sector weights, tax preferences, constraints
- `portfolio/stock_data.md` — MotherDuck database connection (stocks, prices, recommendations tables for ~4,300 U.S. equities)

## Session 7: Predictive Modeling

**Data** in `session7/data/`:

- `customer_churn.csv` — 7,043 telecom customers, 21 columns including tenure, MonthlyCharges, TotalCharges, Contract, InternetService, Churn (Yes/No). 26.5% churn rate.

## Session 8: Your AI Strategy (Capstone)

Capstone presentations. Exercises in `session8/exercises/`. Demo in `session8/demos/ai-as-thinking-partner/` is a pre-scripted 4-turn strategic conversation for instructor reference.

## Business Definitions
- **Revenue** means closed/completed transactions only (not pipeline or lost deals)
- **Active customer** means status = "Active" (exclude churned customers unless explicitly asked)
- **Active employee** means status = "Active" in Workday
- When asked for "this year" use 2025; "last year" means 2024
- Cross-system joins: use `wd_system_ids` to map Workday `worker_id` to Salesforce `OwnerId`

## Guidelines
- Write clear, well-structured code
- When generating documents (Word, Excel, PowerPoint), use the installed skills
- For data analysis, use Python with pandas and matplotlib
- Show your work — explain what you are doing and what assumptions you are making
