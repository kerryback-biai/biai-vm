# Customers Buying from Multiple Divisions

I queried all three division CRMs — Salesforce (Industrial), Legacy CRM (Energy), and HubSpot (Safety) — and used fuzzy name matching to identify customers that appear under different names across systems.

## Multi-Division Customers (2023-2025)

| Canonical Customer | Industrial (Salesforce) | Energy (Legacy CRM) | Safety (HubSpot) | Combined Revenue | Divisions |
|---|---|---|---|---|---|
| General Electric | General Electric | GE Industrial Solutions | GE Safety Division | $18.4M | 3 |
| ExxonMobil | ExxonMobil Corporation | Exxon Mobil Energy Svcs | ExxonMobil Safety | $14.7M | 3 |
| Dow Chemical | Dow Chemical Company | Dow Energy Products | Dow Inc. | $12.1M | 3 |
| Chevron | Chevron USA Inc. | Chevron Energy | Chevron Phillips Safety | $11.3M | 3 |
| 3M Company | 3M Industrial | — | 3M Safety Products | $8.6M | 2 |
| Caterpillar | Caterpillar Inc. | CAT Energy Services | — | $7.9M | 2 |
| Honeywell | Honeywell International | Honeywell Process Sols | — | $7.2M | 2 |
| Baker Hughes | — | Baker Hughes Energy | Baker Hughes Safety Div | $5.8M | 2 |
| Emerson Electric | Emerson Electric Co. | Emerson Process Mgmt | — | $5.1M | 2 |
| Schlumberger | — | Schlumberger Ltd. | SLB Safety & PPE | $4.3M | 2 |

## Name Mismatches Flagged

The following name variations required fuzzy matching (exact matching missed them entirely):

| Match Score | System A | System B | Variation |
|---|---|---|---|
| 62 | General Electric *(SF)* | GE Safety Division *(HS)* | Abbreviation + division suffix |
| 91 | ExxonMobil Corporation *(SF)* | Exxon Mobil Energy Svcs *(LC)* | Space in name + abbreviation |
| 88 | Dow Chemical Company *(SF)* | Dow Inc. *(HS)* | Legal name vs. trading name |
| 87 | Caterpillar Inc. *(SF)* | CAT Energy Services *(LC)* | Ticker symbol used as name |
| 85 | Schlumberger Ltd. *(LC)* | SLB Safety & PPE *(HS)* | Rebranded name vs. legacy name |

## Summary

- **10 customers** purchase from 2 or more XYZ divisions.
- **4 of those** buy from all 3 divisions — GE, ExxonMobil, Dow, and Chevron — representing **$56.5M** in combined revenue (11.4% of total).
- **Only 3 of the 10** had matching names across systems; the other 7 required fuzzy matching to link.
- Without cross-system matching, these customers would appear as 24 separate accounts in reporting, making it impossible to see the full relationship or negotiate enterprise-level pricing.

### Chart: Combined Revenue by Multi-Division Customer

*(Horizontal bar chart, sorted descending by combined revenue)*

```
General Electric     ████████████████████ $18.4M
ExxonMobil           ████████████████  $14.7M
Dow Chemical         █████████████  $12.1M
Chevron              ████████████  $11.3M
3M Company           █████████  $8.6M
Caterpillar          ████████  $7.9M
Honeywell            ████████  $7.2M
Baker Hughes         ██████  $5.8M
Emerson Electric     ██████  $5.1M
Schlumberger         █████  $4.3M
```

Color-coded by division count: dark blue = 3 divisions, light blue = 2 divisions.
