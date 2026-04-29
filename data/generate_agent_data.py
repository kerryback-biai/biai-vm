"""
Generate synthetic Salesforce and Workday parquet files for XYZ Corp.
XYZ Corp: $500M B2B industrial distributor, 3 divisions (Industrial, Energy, Safety).

Output:
  data/salesforce/sf_accounts.parquet
  data/salesforce/sf_orders.parquet
  data/workday/wd_workers.parquet
  data/workday/wd_compensation.parquet
  data/workday/wd_system_ids.parquet
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
DIVISIONS = ["Industrial", "Energy", "Safety"]

INDUSTRIES = {
    "Industrial": [
        "Manufacturing", "Automotive", "Aerospace", "Construction",
        "Heavy Equipment", "Metal Fabrication", "Plastics", "Chemicals",
    ],
    "Energy": [
        "Oil & Gas", "Utilities", "Renewable Energy", "Mining",
        "Pipeline Services", "Drilling", "Power Generation",
    ],
    "Safety": [
        "Healthcare", "Government", "Education", "Food Processing",
        "Pharmaceuticals", "Transportation", "Warehousing",
    ],
}

STATES = [
    "TX", "CA", "OH", "PA", "IL", "MI", "LA", "OK", "CO", "WA",
    "NY", "FL", "GA", "NC", "IN", "WI", "MN", "AL", "TN", "VA",
]

FIRST_NAMES = [
    "James", "Maria", "Robert", "Jennifer", "Michael", "Linda", "David",
    "Sarah", "Richard", "Patricia", "Thomas", "Elizabeth", "Daniel",
    "Barbara", "Matthew", "Susan", "Christopher", "Jessica", "Andrew",
    "Karen", "Joseph", "Nancy", "Charles", "Lisa", "Steven", "Betty",
    "Kevin", "Margaret", "Brian", "Sandra", "George", "Ashley",
    "Edward", "Dorothy", "Ronald", "Kimberly", "Timothy", "Emily",
    "Jason", "Donna", "Ryan", "Michelle", "Jacob", "Carol",
    "Gary", "Amanda", "Nicholas", "Deborah", "Eric", "Stephanie",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts",
]

COMPANY_PREFIXES = [
    "General", "Pacific", "National", "American", "Western", "Southern",
    "Northern", "Central", "Atlantic", "Global", "United", "Premier",
    "Advanced", "Precision", "Superior", "Liberty", "Eagle", "Summit",
    "Apex", "Frontier", "Cascade", "Sterling", "Titan", "Pinnacle",
    "Vanguard", "Horizon", "Cornerstone", "Keystone", "Continental",
    "Meridian",
]

COMPANY_SUFFIXES = {
    "Industrial": [
        "Manufacturing", "Industries", "Fabrication", "Engineering",
        "Machine Works", "Tool & Die", "Systems", "Solutions",
        "Components", "Products",
    ],
    "Energy": [
        "Energy", "Petroleum", "Resources", "Power", "Drilling",
        "Pipeline Services", "Oilfield Services", "Utilities",
        "Gas & Electric", "Exploration",
    ],
    "Safety": [
        "Safety Products", "Protection Systems", "PPE Supply",
        "Health & Safety", "Environmental Services", "Compliance Solutions",
        "Fire Protection", "Safety Equipment", "Medical Supplies",
        "Protective Gear",
    ],
}

ACCOUNT_TYPES = ["Customer", "Customer", "Customer", "Customer", "Prospect"]

JOB_TITLES_SALES = [
    "Account Executive", "Senior Account Executive", "Regional Sales Manager",
    "Sales Representative", "Business Development Manager",
    "Key Account Manager", "Sales Director", "Territory Manager",
]

JOB_TITLES_OTHER = [
    "Operations Manager", "Supply Chain Analyst", "Warehouse Supervisor",
    "Customer Service Representative", "Financial Analyst",
    "Marketing Coordinator", "HR Business Partner", "IT Support Specialist",
    "Logistics Coordinator", "Quality Assurance Manager",
    "Product Manager", "Data Analyst", "Procurement Specialist",
    "Training Coordinator", "Compliance Officer",
]

DEPARTMENTS = {
    "Industrial": ["Sales", "Operations", "Engineering", "Quality", "Logistics"],
    "Energy": ["Sales", "Field Operations", "Technical Services", "Safety", "Logistics"],
    "Safety": ["Sales", "Product Management", "Customer Service", "Compliance", "Warehouse"],
}

ORDER_STATUSES = ["Completed", "Completed", "Completed", "Completed",
                  "Completed", "Shipped", "Shipped", "Processing", "Cancelled"]


def make_sf_id(prefix, n):
    return [f"{prefix}{str(i).zfill(5)}" for i in range(1, n + 1)]


# ---------------------------------------------------------------------------
# 1. Salesforce Accounts
# ---------------------------------------------------------------------------
N_ACCOUNTS = 120  # ~40 per division

accounts = []
for i in range(N_ACCOUNTS):
    div = DIVISIONS[i % 3]
    industry = rng.choice(INDUSTRIES[div])
    prefix = rng.choice(COMPANY_PREFIXES)
    suffix = rng.choice(COMPANY_SUFFIXES[div])
    name = f"{prefix} {suffix}"
    # Ensure unique names
    name = f"{name}" if i < 90 else f"{name} {rng.choice(STATES)}"
    state = rng.choice(STATES)
    acct_type = rng.choice(ACCOUNT_TYPES)
    # Revenue: big range, skewed
    if acct_type == "Prospect":
        revenue = 0
    else:
        revenue = int(rng.lognormal(mean=13.5, sigma=1.2))
        revenue = min(revenue, 50_000_000)
        revenue = max(revenue, 50_000)
        revenue = round(revenue, -3)

    accounts.append({
        "AccountId": f"ACC{str(i+1).zfill(5)}",
        "AccountName": name,
        "Industry": industry,
        "BillingState": state,
        "OwnerId": None,  # filled after we create sales reps
        "AnnualRevenue": revenue,
        "Type": acct_type,
    })

df_accounts = pd.DataFrame(accounts)

# ---------------------------------------------------------------------------
# 2. Workday Workers — create sales reps first, then other staff
# ---------------------------------------------------------------------------
N_SALES_REPS = 25
N_OTHER_WORKERS = 75
N_WORKERS = N_SALES_REPS + N_OTHER_WORKERS

workers = []
used_names = set()

for i in range(N_WORKERS):
    while True:
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        if (first, last) not in used_names:
            used_names.add((first, last))
            break

    div = DIVISIONS[i % 3]
    if i < N_SALES_REPS:
        dept = "Sales"
        title = rng.choice(JOB_TITLES_SALES)
    else:
        dept = rng.choice(DEPARTMENTS[div])
        title = rng.choice(JOB_TITLES_OTHER)

    status = "Active" if rng.random() < 0.92 else "Inactive"
    worker_id = f"WD-{str(i+1).zfill(4)}"

    workers.append({
        "worker_id": worker_id,
        "first_name": first,
        "last_name": last,
        "division": div,
        "department": dept,
        "job_title": title,
        "status": status,
    })

df_workers = pd.DataFrame(workers)

# Assign sales rep OwnerId to accounts
sales_rep_ids = df_workers[df_workers["department"] == "Sales"]["worker_id"].tolist()
owner_ids = [f"OWN{str(i+1).zfill(5)}" for i in range(len(sales_rep_ids))]
rep_to_owner = dict(zip(sales_rep_ids, owner_ids))

# Assign accounts to reps (each rep gets ~4-5 accounts)
active_accounts = df_accounts[df_accounts["Type"] == "Customer"].index.tolist()
rng.shuffle(active_accounts)
for idx, acct_idx in enumerate(active_accounts):
    rep_idx = idx % len(sales_rep_ids)
    df_accounts.at[acct_idx, "OwnerId"] = owner_ids[rep_idx]

# Prospects get random owners too
prospect_idx = df_accounts[df_accounts["Type"] == "Prospect"].index.tolist()
for idx in prospect_idx:
    df_accounts.at[idx, "OwnerId"] = rng.choice(owner_ids)

# ---------------------------------------------------------------------------
# 3. System ID mapping (Workday worker_id <-> Salesforce OwnerId)
# ---------------------------------------------------------------------------
system_ids = []
for wid, oid in rep_to_owner.items():
    system_ids.append({
        "worker_id": wid,
        "system_name": "salesforce",
        "external_id": oid,
    })

df_system_ids = pd.DataFrame(system_ids)

# ---------------------------------------------------------------------------
# 4. Salesforce Orders (2023-2025)
# ---------------------------------------------------------------------------
customer_accounts = df_accounts[df_accounts["Type"] == "Customer"]
orders = []
order_id = 1

for _, acct in customer_accounts.iterrows():
    # Number of orders proportional to revenue
    n_orders = max(2, int(acct["AnnualRevenue"] / 200_000))
    n_orders = min(n_orders, 40)
    # Spread across 2023-2025
    for _ in range(n_orders):
        year = rng.choice([2023, 2023, 2024, 2024, 2024, 2025, 2025])
        month = rng.integers(1, 13)
        day = rng.integers(1, 29)
        order_date = f"{year}-{month:02d}-{day:02d}"

        base_amount = acct["AnnualRevenue"] / n_orders
        amount = base_amount * rng.uniform(0.5, 1.5)
        amount = round(amount, 2)

        status = rng.choice(ORDER_STATUSES)
        if status == "Cancelled":
            amount = 0

        orders.append({
            "OrderId": f"ORD{str(order_id).zfill(6)}",
            "AccountId": acct["AccountId"],
            "OpportunityId": f"OPP{str(order_id).zfill(6)}",
            "OrderDate": order_date,
            "TotalAmount": amount,
            "Status": status,
        })
        order_id += 1

df_orders = pd.DataFrame(orders)

# ---------------------------------------------------------------------------
# 5. Workday Compensation
# ---------------------------------------------------------------------------
comp = []
comp_id = 1

for _, w in df_workers.iterrows():
    if w["department"] == "Sales":
        base = rng.integers(75_000, 140_000)
        bonus_target = rng.choice([0.15, 0.20, 0.25, 0.30])
    else:
        base = rng.integers(55_000, 120_000)
        bonus_target = rng.choice([0.05, 0.08, 0.10, 0.12, 0.15])

    # Round base to nearest 1000
    base = int(round(base, -3))
    bonus_actual = round(base * bonus_target * rng.uniform(0.6, 1.3), 2)

    # Effective date: beginning of current year or mid-year raise
    eff_date = rng.choice(["2025-01-01", "2024-07-01", "2024-01-01"])

    comp.append({
        "comp_id": f"CMP{str(comp_id).zfill(5)}",
        "worker_id": w["worker_id"],
        "effective_date": eff_date,
        "base_pay": base,
        "bonus_target_pct": bonus_target,
        "bonus_actual": bonus_actual,
    })
    comp_id += 1

df_comp = pd.DataFrame(comp)

# ---------------------------------------------------------------------------
# Write parquet files
# ---------------------------------------------------------------------------
os.makedirs("data/salesforce", exist_ok=True)
os.makedirs("data/workday", exist_ok=True)

df_accounts.to_parquet("data/salesforce/sf_accounts.parquet", index=False)
df_orders.to_parquet("data/salesforce/sf_orders.parquet", index=False)
df_workers.to_parquet("data/workday/wd_workers.parquet", index=False)
df_comp.to_parquet("data/workday/wd_compensation.parquet", index=False)
df_system_ids.to_parquet("data/workday/wd_system_ids.parquet", index=False)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("Generated XYZ Corp agent data:")
print(f"  sf_accounts.parquet:    {len(df_accounts):>4} rows  ({df_accounts['Type'].value_counts().to_dict()})")
print(f"  sf_orders.parquet:      {len(df_orders):>4} rows  (2023-2025)")
print(f"  wd_workers.parquet:     {len(df_workers):>4} rows  ({df_workers['status'].value_counts().to_dict()})")
print(f"  wd_compensation.parquet:{len(df_comp):>4} rows")
print(f"  wd_system_ids.parquet:  {len(df_system_ids):>4} rows  (maps {len(sales_rep_ids)} sales reps)")
print()
print("Revenue range:", f"${df_accounts['AnnualRevenue'].min():,.0f} - ${df_accounts['AnnualRevenue'].max():,.0f}")
print("Order amount range:", f"${df_orders[df_orders['TotalAmount']>0]['TotalAmount'].min():,.2f} - ${df_orders['TotalAmount'].max():,.2f}")
print("Divisions:", df_workers["division"].value_counts().to_dict())
