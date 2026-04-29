import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sales = pd.read_csv('data/sales.csv')
customers = pd.read_csv('data/customers.csv')
employees = pd.read_csv('data/employees.csv')
sales['date'] = pd.to_datetime(sales['date'])

print("="*60)
print("ITERATE TO EXECUTIVE FORMAT")
print("="*60)

# === Iteration 1: Stacked Area Chart by Product Line ===
print("\n--- Iteration 1: Stacked Area Chart ---")
sales['year_month'] = sales['date'].dt.to_period('M')
monthly_by_pl = sales.groupby(['year_month', 'product_line'])['amount'].sum().unstack(fill_value=0)
monthly_by_pl.index = monthly_by_pl.index.astype(str)

fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#00205B', '#4A90D9', '#7C7E7F']
ax.stackplot(range(len(monthly_by_pl)),
             [monthly_by_pl[col].values for col in monthly_by_pl.columns],
             labels=monthly_by_pl.columns, colors=colors, alpha=0.8)
ax.set_title('Monthly Revenue by Product Line (Stacked Area)', fontsize=14, fontweight='bold')
ax.set_ylabel('Revenue ($)')
ax.set_xticks(range(0, len(monthly_by_pl), 2))
ax.set_xticklabels([monthly_by_pl.index[i] for i in range(0, len(monthly_by_pl), 2)], rotation=45)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('demos/iterate-to-executive-format/stacked_area_chart.png', dpi=150)
plt.close()
print("  -> Saved demos/iterate-to-executive-format/stacked_area_chart.png")

# === Iteration 2: Traffic-Light Dashboard ===
print("\n--- Iteration 2: Traffic-Light Key Metrics ---")
total_revenue = sales['amount'].sum()
txn_count = len(sales)
avg_deal = sales['amount'].mean()
active_customers = customers[customers['status'] == 'Active'].shape[0]
rev_per_employee = total_revenue / len(employees)

# By region metrics
region_metrics = sales.groupby('region').agg(
    Revenue=('amount', 'sum'),
    Transactions=('transaction_id', 'count'),
    Avg_Deal=('amount', 'mean')
).reset_index()
region_metrics['Active_Customers'] = region_metrics['region'].apply(
    lambda r: customers[(customers['region'] == r) & (customers['status'] == 'Active')].shape[0]
)
region_metrics['Rev_per_Employee'] = region_metrics['Revenue'] / (len(employees) / 4)  # rough split

# Traffic light: green if above median, yellow if within 10%, red if below
def traffic_light(val, median):
    if val > median:
        return 'GREEN'
    elif val >= median * 0.9:
        return 'YELLOW'
    else:
        return 'RED'

for col in ['Revenue', 'Transactions', 'Avg_Deal', 'Active_Customers']:
    med = region_metrics[col].median()
    region_metrics[f'{col}_Signal'] = region_metrics[col].apply(lambda x: traffic_light(x, med))

print("\n  Traffic-Light Dashboard by Region:")
print(f"  {'Region':<12} {'Revenue':>12} {'Signal':<8} {'Txns':>6} {'Signal':<8} {'Avg Deal':>10} {'Signal':<8}")
print("  " + "-"*70)
for _, row in region_metrics.iterrows():
    print(f"  {row['region']:<12} ${row['Revenue']:>11,.0f} {row['Revenue_Signal']:<8} "
          f"{row['Transactions']:>6} {row['Transactions_Signal']:<8} "
          f"${row['Avg_Deal']:>9,.0f} {row['Avg_Deal_Signal']:<8}")

# Save traffic light as a visual
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('off')
metrics = ['Revenue', 'Transactions', 'Avg_Deal', 'Active_Customers']
colors_map = {'GREEN': '#2ecc71', 'YELLOW': '#f39c12', 'RED': '#e74c3c'}

table_data = []
for _, row in region_metrics.iterrows():
    table_data.append([row['region']] +
        [f"${row[m]:,.0f}" if m in ['Revenue','Avg_Deal'] else str(int(row[m])) for m in metrics])

table = ax.table(cellText=table_data,
    colLabels=['Region'] + metrics,
    loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)

# Color the cells
for i, row in region_metrics.iterrows():
    for j, m in enumerate(metrics):
        signal = row[f'{m}_Signal']
        table[i+1, j+1].set_facecolor(colors_map[signal])
        table[i+1, j+1].set_alpha(0.6)

ax.set_title('Traffic-Light Key Metrics by Region', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('demos/iterate-to-executive-format/traffic_light_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("  -> Saved demos/iterate-to-executive-format/traffic_light_dashboard.png")

print("\nIteration demo complete!")
