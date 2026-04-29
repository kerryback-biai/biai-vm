import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sales = pd.read_csv('data/sales.csv')
customers = pd.read_csv('data/customers.csv')
employees = pd.read_csv('data/employees.csv')
sales['date'] = pd.to_datetime(sales['date'])
sales['quarter'] = sales['date'].dt.to_period('Q').astype(str)

print("="*60)
print("AD-HOC ANALYSIS: BEYOND THE DASHBOARD")
print("="*60)

# === Prompt 1: Customer Decline Detection ===
print("\n--- 1. Customer Decline Detection (QoQ, >20% drop flagged) ---")
cust_quarterly = sales.groupby(['customer_name', 'quarter'])['amount'].sum().unstack(fill_value=0)
quarters = sorted(cust_quarterly.columns)

declining = []
for cust in cust_quarterly.index:
    for i in range(1, len(quarters)):
        prev = cust_quarterly.loc[cust, quarters[i-1]]
        curr = cust_quarterly.loc[cust, quarters[i]]
        if prev > 0 and curr < prev:
            pct_change = (curr - prev) / prev * 100
            if pct_change < -20:
                declining.append({
                    'Customer': cust,
                    'From Quarter': quarters[i-1],
                    'To Quarter': quarters[i],
                    'Previous Revenue': prev,
                    'Current Revenue': curr,
                    'Change %': pct_change
                })

dec_df = pd.DataFrame(declining).sort_values('Change %')
print(f"  Found {len(dec_df)} quarter-over-quarter declines > 20%")
print(f"  Unique customers with >20% decline: {dec_df['Customer'].nunique()}")
if len(dec_df) > 0:
    print("\n  Top 10 worst declines:")
    for _, row in dec_df.head(10).iterrows():
        print(f"    {row['Customer']}: {row['From Quarter']} -> {row['To Quarter']}: "
              f"${row['Previous Revenue']:,.0f} -> ${row['Current Revenue']:,.0f} ({row['Change %']:.1f}%)")

# === Prompt 2: Revenue Concentration Risk ===
print("\n--- 2. Revenue Concentration Risk ---")
total_rev = sales['amount'].sum()
cust_rev = sales.groupby('customer_name')['amount'].sum().sort_values(ascending=False)
top3_pct = cust_rev.head(3).sum() / total_rev * 100
top5_pct = cust_rev.head(5).sum() / total_rev * 100
top10_pct = cust_rev.head(10).sum() / total_rev * 100

print(f"  Total Revenue: ${total_rev:,.0f}")
print(f"  Top 3 customers: ${cust_rev.head(3).sum():,.0f} ({top3_pct:.1f}%)")
print(f"  Top 5 customers: ${cust_rev.head(5).sum():,.0f} ({top5_pct:.1f}%)")
print(f"  Top 10 customers: ${cust_rev.head(10).sum():,.0f} ({top10_pct:.1f}%)")

# Concentration curve
cumulative = cust_rev.cumsum() / total_rev * 100
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(1, len(cumulative)+1), cumulative.values, 'b-', linewidth=2)
ax.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='80% threshold')
ax.set_xlabel('Number of Customers (ranked by revenue)')
ax.set_ylabel('Cumulative Revenue %')
ax.set_title('Revenue Concentration Curve', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('demos/ad-hoc-beyond-dashboard/concentration_curve.png', dpi=150)
plt.close()
print("  -> Saved demos/ad-hoc-beyond-dashboard/concentration_curve.png")

# === Prompt 3: Revenue per Sales Rep by Product Line ===
print("\n--- 3. Revenue per Sales Rep by Product Line ---")
rev_by_pl_rep = sales.groupby(['product_line', 'sales_rep'])['amount'].sum()
reps_per_pl = sales.groupby('product_line')['sales_rep'].nunique()
rev_per_pl = sales.groupby('product_line')['amount'].sum()
rev_per_rep = (rev_per_pl / reps_per_pl).sort_values(ascending=False)

for pl, val in rev_per_rep.items():
    reps = reps_per_pl[pl]
    print(f"  {pl}: ${val:,.0f} per rep ({reps} reps, ${rev_per_pl[pl]:,.0f} total)")

# === Prompt 4: Churn Signals ===
print("\n--- 4. Churn Signals ---")
churned = customers[customers['status'] == 'Churned']['customer_name'].tolist()
print(f"  Churned customers: {len(churned)}")

churned_sales = sales[sales['customer_name'].isin(churned)]
if len(churned_sales) > 0:
    churned_quarterly = churned_sales.groupby(['customer_name', 'quarter']).agg(
        revenue=('amount', 'sum'),
        txn_count=('transaction_id', 'count'),
        avg_order=('amount', 'mean')
    ).reset_index()

    print("\n  Churned customer transaction patterns:")
    for cust in churned[:5]:
        cdata = churned_quarterly[churned_quarterly['customer_name'] == cust].sort_values('quarter')
        if len(cdata) >= 2:
            print(f"\n  {cust}:")
            for _, row in cdata.iterrows():
                print(f"    {row['quarter']}: {row['txn_count']} txns, ${row['revenue']:,.0f} rev, ${row['avg_order']:,.0f} avg")
else:
    print("  No sales found for churned customers in dataset.")

print("\nAd-hoc analysis complete!")
