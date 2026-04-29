"""Generate Acme Corp dashboard data for Session 2.

Creates three CSV files matching the session 2 slide descriptions:
- sales.csv: 837 transactions (date, customer, product_line, amount, region, sales_rep)
- customers.csv: 50 customers (name, industry, region, acquisition_date, status, contract_value)
- employees.csv: 30 employees (name, department, division, hire_date, role, salary_band)
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

# --- Customers ---
INDUSTRIES = [
    "Manufacturing", "Healthcare", "Technology", "Energy", "Construction",
    "Transportation", "Retail", "Financial Services", "Education", "Agriculture",
]
REGIONS = ["South", "Northeast", "Midwest", "West"]
PRODUCT_LINES = ["Industrial Products", "Technical Services", "Safety & Compliance"]

first_names = [
    "Apex", "Summit", "Horizon", "Pinnacle", "Vanguard", "Atlas", "Beacon",
    "Catalyst", "Dynamo", "Eagle", "Frontier", "Genesis", "Harbor", "Ironclad",
    "Keystone", "Landmark", "Meridian", "Nexus", "Olympus", "Pioneer",
    "Quantum", "Ridgeline", "Sterling", "Titan", "Unified", "Vertex", "Westfield",
    "Zenith", "Alpine", "Bridgeport", "Cascade", "Delta", "Evergreen", "Falcon",
    "Granite", "Highland", "Integrity", "Jasper", "Kingston", "Liberty",
    "Magellan", "Northstar", "Oakridge", "Pacific", "Redwood", "Silverline",
    "Trident", "Upland", "Vista", "Wolverine",
]
suffixes = ["Industries", "Corp", "Solutions", "Group", "Enterprises", "LLC", "Inc", "Co", "Partners", "Systems"]

customers = []
for i in range(50):
    name = f"{first_names[i]} {random.choice(suffixes)}"
    industry = random.choice(INDUSTRIES)
    region = random.choice(REGIONS)
    acq_date = date(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
    status = "Active" if random.random() < 0.82 else "Churned"
    contract_value = round(random.uniform(50000, 800000), 2)
    customers.append({
        "name": name,
        "industry": industry,
        "region": region,
        "acquisition_date": acq_date.isoformat(),
        "status": status,
        "contract_value": contract_value,
    })

with open("customers.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "industry", "region", "acquisition_date", "status", "contract_value"])
    w.writeheader()
    w.writerows(customers)

# --- Employees ---
DEPARTMENTS = [
    "Sales", "Sales", "Sales", "Sales", "Sales",  # weight toward sales
    "Engineering", "Engineering", "Engineering",
    "Marketing", "Marketing",
    "Operations", "Operations", "Operations",
    "Finance", "Finance",
    "HR", "HR",
    "Executive",
]
DIVISIONS = {
    "Sales": "Revenue",
    "Engineering": "Product",
    "Marketing": "Revenue",
    "Operations": "Operations",
    "Finance": "Corporate",
    "HR": "Corporate",
    "Executive": "Corporate",
}
ROLES = {
    "Sales": ["Account Executive", "Sales Manager", "Regional Director", "Sales Rep", "Business Development"],
    "Engineering": ["Engineer", "Senior Engineer", "Tech Lead", "Engineering Manager"],
    "Marketing": ["Marketing Specialist", "Marketing Manager", "Content Lead"],
    "Operations": ["Operations Analyst", "Logistics Coordinator", "Operations Manager"],
    "Finance": ["Financial Analyst", "Controller", "Accountant"],
    "HR": ["HR Specialist", "HR Manager"],
    "Executive": ["CEO", "COO", "CFO"],
}
SALARY_BANDS = ["Band 1", "Band 2", "Band 3", "Band 4", "Band 5"]

emp_first = [
    "James", "Maria", "Robert", "Sarah", "David", "Jennifer", "Michael", "Lisa",
    "William", "Patricia", "Thomas", "Karen", "Daniel", "Nancy", "Christopher",
    "Emily", "Matthew", "Amanda", "Anthony", "Stephanie", "Mark", "Rebecca",
    "Andrew", "Laura", "Joshua", "Ashley", "Ryan", "Megan", "Kevin", "Rachel",
]
emp_last = [
    "Johnson", "Martinez", "Chen", "Williams", "Patel", "Brown", "Kim", "Garcia",
    "Anderson", "Thompson", "Wilson", "Taylor", "Lee", "Harris", "Clark",
    "Robinson", "Lewis", "Walker", "Young", "King", "Wright", "Scott",
    "Adams", "Nelson", "Hill", "Moore", "Jackson", "White", "Mitchell", "Roberts",
]

employees = []
for i in range(30):
    dept = random.choice(DEPARTMENTS)
    employees.append({
        "name": f"{emp_first[i]} {emp_last[i]}",
        "department": dept,
        "division": DIVISIONS[dept],
        "hire_date": (date(2018, 1, 1) + timedelta(days=random.randint(0, 2500))).isoformat(),
        "role": random.choice(ROLES[dept]),
        "salary_band": random.choice(SALARY_BANDS),
    })

with open("employees.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "department", "division", "hire_date", "role", "salary_band"])
    w.writeheader()
    w.writerows(employees)

# --- Sales Transactions ---
active_customers = [c for c in customers if c["status"] == "Active"]
sales_reps = [e["name"] for e in employees if e["department"] == "Sales"]

sales = []
for _ in range(837):
    cust = random.choice(active_customers)
    txn_date = date(2024, 1, 1) + timedelta(days=random.randint(0, 545))  # 2024-01-01 to 2025-07-01
    product_line = random.choice(PRODUCT_LINES)

    # Vary amount by product line (calibrated to ~$15.4M total across 837 txns)
    if product_line == "Industrial Products":
        amount = round(random.uniform(4000, 60000), 2)
    elif product_line == "Technical Services":
        amount = round(random.uniform(1500, 30000), 2)
    else:
        amount = round(random.uniform(800, 18000), 2)

    sales.append({
        "date": txn_date.isoformat(),
        "customer": cust["name"],
        "product_line": product_line,
        "amount": amount,
        "region": cust["region"],
        "sales_rep": random.choice(sales_reps),
    })

with open("sales.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["date", "customer", "product_line", "amount", "region", "sales_rep"])
    w.writeheader()
    w.writerows(sales)

# Summary
total_rev = sum(s["amount"] for s in sales)
print(f"Generated:")
print(f"  customers.csv: {len(customers)} customers ({sum(1 for c in customers if c['status']=='Active')} active, {sum(1 for c in customers if c['status']=='Churned')} churned)")
print(f"  employees.csv: {len(employees)} employees")
print(f"  sales.csv: {len(sales)} transactions, total revenue ${total_rev:,.2f}")
