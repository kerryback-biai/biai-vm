import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sales = pd.read_csv('data/sales.csv')
customers = pd.read_csv('data/customers.csv')
employees = pd.read_csv('data/employees.csv')
sales['date'] = pd.to_datetime(sales['date'])

print("="*60)
print("DASHBOARD REPLICATION DEMO")
print("="*60)

# 1. Revenue by product line
rev_by_pl = sales.groupby('product_line')['amount'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
rev_by_pl.plot(kind='bar', ax=ax, color=['#00205B', '#4A90D9', '#7C7E7F'])
ax.set_title('Total Revenue by Product Line', fontsize=14, fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.tick_params(axis='x', rotation=30)
for i, v in enumerate(rev_by_pl):
    ax.text(i, v + 50000, f'${v/1e6:.1f}M', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('demos/dashboard-replication/revenue_by_product_line.png', dpi=150)
plt.close()
print("  1. Revenue by product line chart saved")

# 2. Revenue by region
rev_by_region = sales.groupby('region')['amount'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
rev_by_region.plot(kind='bar', ax=ax, color=['#00205B', '#4A90D9', '#7C7E7F', '#A0C4E8'])
ax.set_title('Revenue by Region', fontsize=14, fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.tick_params(axis='x', rotation=0)
for i, v in enumerate(rev_by_region):
    ax.text(i, v + 30000, f'${v/1e6:.1f}M', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('demos/dashboard-replication/revenue_by_region.png', dpi=150)
plt.close()
print("  2. Revenue by region chart saved")

# 3. Top 10 customers
top10 = sales.groupby('customer_name')['amount'].sum().sort_values(ascending=False).head(10)
print("\n  3. Top 10 Customers:")
for i, (c, v) in enumerate(top10.items(), 1):
    print(f"     {i}. {c}: ${v:,.2f}")

# 4. Monthly trend
sales['year'] = sales['date'].dt.year
sales['month'] = sales['date'].dt.month
monthly = sales.groupby(['year', 'month'])['amount'].sum().unstack(level=0)
fig, ax = plt.subplots(figsize=(10, 5))
for yr in monthly.columns:
    ax.plot(monthly.index, monthly[yr], marker='o', label=str(yr), linewidth=2)
ax.set_title('Monthly Revenue: 2024 vs 2025', fontsize=14, fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('demos/dashboard-replication/monthly_trend.png', dpi=150)
plt.close()
print("  4. Monthly trend chart saved")

# 5. Headcount
hc = employees.groupby('department').size().sort_values(ascending=False)
print("\n  5. Headcount by Department:")
for d, c in hc.items():
    print(f"     {d}: {c}")

# 6. Key metrics
total_rev = sales['amount'].sum()
active = customers[customers['status'] == 'Active'].shape[0]
print(f"\n  6. Key Metrics:")
print(f"     Total Revenue: ${total_rev:,.2f}")
print(f"     Transactions: {len(sales)}")
print(f"     Avg Deal Size: ${sales['amount'].mean():,.2f}")
print(f"     Active Customers: {active}")
print(f"     Revenue/Employee: ${total_rev/len(employees):,.2f}")

# Verify expected output from prompt.md
print("\n--- Verification vs Expected ---")
print(f"  Total revenue ~$10.3M? ${total_rev/1e6:.1f}M  OK" if abs(total_rev - 10300000) < 200000 else "  MISMATCH")
print(f"  837 transactions? {len(sales)}  {'OK' if len(sales) == 837 else 'MISMATCH'}")
print(f"  Top customer Apex ~$826K? ${top10.iloc[0]:,.0f}  {'OK' if abs(top10.iloc[0] - 826000) < 5000 else 'CLOSE'}")

print("\nDashboard replication demo complete!")
