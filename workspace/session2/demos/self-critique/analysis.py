import pandas as pd

sales = pd.read_csv('data/sales.csv')
customers = pd.read_csv('data/customers.csv')
employees = pd.read_csv('data/employees.csv')
sales['date'] = pd.to_datetime(sales['date'])

print("="*60)
print("SELF-CRITIQUE DEMO: Verification Points")
print("="*60)

# Point 1: Active vs Churned customers
churned = customers[customers['status'] == 'Churned']
active = customers[customers['status'] == 'Active']
print(f"\n1. Customer Status Check:")
print(f"   Active customers: {len(active)}")
print(f"   Churned customers: {len(churned)}")
print(f"   All churned customers have sales data: {all(c in sales['customer_name'].values for c in churned['customer_name'])}")
print(f"   => If 'active customers' metric included churned, it would be {len(customers)} instead of {len(active)}")

# Point 2: Revenue per employee - total vs sales staff
total_emp = len(employees)
sales_emp = len(employees[employees['department'] == 'Sales'])
total_rev = sales['amount'].sum()
print(f"\n2. Revenue per Employee Ambiguity:")
print(f"   Total headcount: {total_emp}")
print(f"   Sales department only: {sales_emp}")
print(f"   Rev/employee (all): ${total_rev/total_emp:,.2f}")
print(f"   Rev/employee (sales only): ${total_rev/sales_emp:,.2f}")
print(f"   => 6x difference depending on definition!")

# Point 3: Calendar year vs fiscal year
print(f"\n3. Date Range Check:")
print(f"   Earliest transaction: {sales['date'].min().strftime('%Y-%m-%d')}")
print(f"   Latest transaction: {sales['date'].max().strftime('%Y-%m-%d')}")
years = sales['date'].dt.year.unique()
print(f"   Years covered: {sorted(years)}")

# Point 4: Revenue definition
print(f"\n4. Revenue Definition:")
print(f"   Raw sum of amount column: ${total_rev:,.2f}")
print(f"   No 'status' column in sales.csv - all transactions treated as completed revenue")
print(f"   No distinction between booked vs collected")

# Point 5: Churned revenue in totals
sales_m = sales.merge(customers[['customer_name','status']], on='customer_name', how='left')
churned_rev = sales_m[sales_m['status'] == 'Churned']['amount'].sum()
print(f"\n5. Churned Customer Revenue in Totals:")
print(f"   Revenue from churned customers: ${churned_rev:,.2f} ({churned_rev/total_rev*100:.1f}% of total)")
print(f"   => This revenue IS included in total revenue and concentration calculations")

# Follow-up: fix active customers metric
print(f"\n--- Follow-up Fix ---")
print(f"   Corrected 'active customers' metric: {len(active)} (excluding {len(churned)} churned)")

print("\nSelf-critique demo complete!")
