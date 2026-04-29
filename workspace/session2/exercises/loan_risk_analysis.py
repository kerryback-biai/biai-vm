import pandas as pd
import numpy as np

# Load data
df = pd.read_excel('data/loan-risk-analysis/loan_tape.xlsx')
df['Origination Date'] = pd.to_datetime(df['Origination Date'])

# ========== RISK TIER CLASSIFICATION (from risk_policy.docx) ==========

def assign_tier(row):
    fico = row['FICO Score']
    ltv = row['LTV Ratio']
    dti = row['DTI Ratio']
    delin = row['Delinquency Status']
    purpose = row['Loan Purpose']

    # Tier 4 - High Risk (ANY)
    if (fico < 620 or
        ltv > 95 or
        dti > 50 or
        delin == '90+ Days Late' or
        (delin in ['60 Days Late', '90+ Days Late'] and fico < 660)):
        return 4

    # Tier 3 - Elevated Risk (ANY)
    if (620 <= fico <= 659 or
        85 < ltv <= 95 or
        43 < dti <= 50 or
        delin in ['30 Days Late', '60 Days Late'] or
        (purpose == 'Cash-Out Refi' and ltv > 75)):
        return 3

    # Tier 2 - Moderate Risk (ALL)
    if (660 <= fico <= 719 and
        ltv <= 85 and
        dti <= 43 and
        delin in ['Current', '30 Days Late']):
        return 2

    # Tier 1 - Low Risk (ALL)
    if (fico >= 720 and
        ltv <= 75 and
        dti <= 36 and
        delin == 'Current' and
        purpose in ['Purchase', 'Refinance']):
        return 1

    # Fallback: if passes Tier 4/3 checks but fails Tier 2/1 ALL criteria
    if fico >= 660 and ltv <= 85 and dti <= 43:
        return 2
    return 3

df['Risk Tier'] = df.apply(assign_tier, axis=1)

# ========== SPECIAL CONDITIONS ==========

total_value = df['Loan Amount'].sum()
state_concentration = df.groupby('Property State')['Loan Amount'].sum() / total_value * 100
concentrated_states = state_concentration[state_concentration > 25].index.tolist()

flags = []

# a) Concentration Risk
if concentrated_states:
    print(f"Concentration Risk: States > 25% of portfolio: {concentrated_states}")
    for st in concentrated_states:
        mask = df['Property State'] == st
        df.loc[mask, 'Risk Tier'] = df.loc[mask, 'Risk Tier'].apply(lambda x: min(x + 1, 4))
        for idx in df[mask].index:
            flags.append((idx, f'Concentration risk: {st} > 25% of portfolio'))
else:
    print("No single state exceeds 25% concentration.")

# b) Vintage Risk - originated before 2020
# Note: policy also requires "no payment history update in last 6 months"
# but the dataset lacks a last-update column, so we flag on origination date only.
vintage_mask = df['Origination Date'] < '2020-01-01'
for idx in df[vintage_mask].index:
    flags.append((idx, 'Vintage risk: originated before 2020'))

# c) Rate Risk - interest rate > 7.5% AND FICO < 680
rate_risk_mask = (df['Interest Rate'] > 7.5) & (df['FICO Score'] < 680)
for idx in df[rate_risk_mask].index:
    flags.append((idx, 'Rate risk: rate > 7.5% with FICO < 680 (potential predatory lending)'))

# d) Combined Stress - FICO < 640 AND LTV > 75% AND DTI > 40%
stress_mask = (df['FICO Score'] < 640) & (df['LTV Ratio'] > 75) & (df['DTI Ratio'] > 40)
for idx in df[stress_mask].index:
    flags.append((idx, 'Combined stress: FICO<640 AND LTV>75% AND DTI>40% => CRO escalation'))

# ========== STATE REGULATORY VIOLATIONS ==========

def check_state_violations(row):
    violations = []
    state = row['Property State']
    fico = row['FICO Score']
    ltv = row['LTV Ratio']
    dti = row['DTI Ratio']
    rate = row['Interest Rate']
    purpose = row['Loan Purpose']

    if state == 'CA':
        if rate > 10.0:
            violations.append('CA: rate exceeds 10% cap')
        if fico < 660 and ltv > 75:
            violations.append('CA: FICO<660 & LTV>75% - needs 2% additional reserves')
        if dti > 43:
            violations.append('CA: DTI>43% - needs enhanced documentation')
    elif state == 'TX':
        if purpose in ['Cash-Out Refi', 'Home Equity'] and ltv > 80:
            violations.append('TX: Home equity/cash-out LTV exceeds 80% constitutional cap')
        if rate > 8.5:
            violations.append('TX: rate>8.5% - additional disclosures required')
    elif state == 'NY':
        if fico < 680:
            violations.append('NY: subprime loan (FICO<680) - ability-to-repay verification needed')
        if ltv > 90:
            violations.append('NY: LTV>90% - mandatory escrow required')
    elif state == 'FL':
        if fico < 640:
            violations.append('FL: high-risk (FICO<640) - quarterly monitoring required')
    elif state == 'IL':
        if dti > 43:
            violations.append('IL: DTI>43% - cannot be classified as Qualified Mortgage')
        if fico < 620 and ltv > 85:
            violations.append('IL: FICO<620 & LTV>85% - director-level approval required')
    elif state == 'NV':
        if ltv > 90:
            violations.append('NV: CLTV>90% - enhanced monitoring required')
        if dti > 50:
            violations.append('NV: DTI>50% - documented compensating factors needed')
    return '; '.join(violations) if violations else ''

df['State Violations'] = df.apply(check_state_violations, axis=1)

# Build flags column
flag_dict = {}
for idx, reason in flags:
    if idx not in flag_dict:
        flag_dict[idx] = []
    flag_dict[idx].append(reason)
df['Special Flags'] = df.index.map(lambda i: '; '.join(flag_dict.get(i, [])) if i in flag_dict else '')

# ========== RESERVE CALCULATION ==========
reserve_rates = {1: 0.005, 2: 0.015, 3: 0.03, 4: 0.05}
df['Reserve Rate'] = df['Risk Tier'].map(reserve_rates)
df['Required Reserve'] = df['Loan Amount'] * df['Reserve Rate']

# Extra 2% reserves for CA loans with FICO<660 and LTV>75%
ca_extra = (df['Property State'] == 'CA') & (df['FICO Score'] < 660) & (df['LTV Ratio'] > 75)
df.loc[ca_extra, 'Required Reserve'] += df.loc[ca_extra, 'Loan Amount'] * 0.02

# ========== REPORTING ==========
tier_labels = {1: 'Tier 1 - Low Risk', 2: 'Tier 2 - Moderate Risk', 3: 'Tier 3 - Elevated Risk', 4: 'Tier 4 - High Risk'}
df['Tier Label'] = df['Risk Tier'].map(tier_labels)

print("\n" + "="*60)
print("LOAN PORTFOLIO RISK REPORT")
print("="*60)

print(f"\nTotal Loans: {len(df)}")
print(f"Total Portfolio Value: ${total_value:,.0f}")

print("\n--- Tier Distribution ---")
tier_summary = df.groupby('Risk Tier').agg(
    Count=('Borrower ID', 'count'),
    Total_Value=('Loan Amount', 'sum'),
    Total_Reserves=('Required Reserve', 'sum')
).reset_index()
for _, row in tier_summary.iterrows():
    label = tier_labels[row['Risk Tier']]
    print(f"  {label}: {row['Count']:.0f} loans, ${row['Total_Value']:,.0f} value, ${row['Total_Reserves']:,.0f} reserves")

print(f"\n  Total Required Reserves: ${df['Required Reserve'].sum():,.0f}")

print("\n--- State Distribution ---")
state_tier = df.groupby(['Property State', 'Risk Tier']).size().unstack(fill_value=0)
print(state_tier)

print("\n--- Concentration by State ---")
for st, pct in state_concentration.sort_values(ascending=False).head(6).items():
    marker = " ** CONCENTRATED **" if st in concentrated_states else ""
    print(f"  {st}: {pct:.1f}%{marker}")

# Flagged loans
flagged = df[(df['Special Flags'] != '') | (df['State Violations'] != '')]
print(f"\n--- Flagged Loans: {len(flagged)} of {len(df)} ---")

rate_risk_count = df['Special Flags'].str.contains('Rate risk').sum()
vintage_count = df['Special Flags'].str.contains('Vintage risk').sum()
stress_count = df['Special Flags'].str.contains('Combined stress').sum()
conc_count = df['Special Flags'].str.contains('Concentration').sum()
state_viol_count = (df['State Violations'] != '').sum()

print(f"  Rate risk flags: {rate_risk_count}")
print(f"  Vintage risk flags: {vintage_count}")
print(f"  Combined stress flags: {stress_count}")
print(f"  Concentration risk adjustments: {conc_count}")
print(f"  State regulatory violations: {state_viol_count}")

# Save to Excel
output_cols = ['Borrower ID', 'Loan Amount', 'Interest Rate', 'Term (Months)',
               'FICO Score', 'LTV Ratio', 'DTI Ratio', 'Delinquency Status',
               'Property State', 'Loan Purpose', 'Origination Date',
               'Tier Label', 'Risk Tier', 'Reserve Rate', 'Required Reserve',
               'State Violations', 'Special Flags']
df[output_cols].to_excel('exercises/loan_risk_report.xlsx', index=False, sheet_name='Risk Report')
print("\n-> Saved exercises/loan_risk_report.xlsx")
print("\nLoan risk analysis complete!")
