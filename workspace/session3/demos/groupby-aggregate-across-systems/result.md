# Revenue per Employee by Division (2025)

I pulled 2025 revenue from each division's CRM and headcount from Workday HR, then merged the results.

## Results

| Division | 2025 Revenue | Headcount | Revenue / Employee |
|---|---|---|---|
| Energy | $52.1M | 134 | **$388,800** |
| Industrial | $87.3M | 218 | **$400,500** |
| Safety | $34.8M | 87 | **$400,000** |
| **Company-wide** | **$174.2M** | **482** | **$361,400** |

*Note: Company-wide headcount includes 43 Corporate/HQ employees (HR, Finance, IT, Executive) who are not assigned to a division. Division-level figures count only employees assigned to that division in Workday.*

### Chart: Revenue per Employee by Division

*(Grouped bar chart — blue bars = revenue per employee, gray dashed line = company-wide average)*

```
              Revenue / Employee ($K)
              0    100   200   300   400   500
              |     |     |     |     |     |
Industrial    ████████████████████████████░  $400.5K
Safety        ████████████████████████████   $400.0K
Energy        ███████████████████████████    $388.8K
Company-wide  ·····························  $361.4K (avg)
```

## Key Observations

1. **Surprisingly close:** All three divisions cluster tightly around $390K-$401K per employee, suggesting headcount has been scaled roughly in proportion to revenue across the business.

2. **Industrial is largest but not most efficient:** Industrial generates the highest absolute revenue ($87.3M) but its per-employee figure ($400.5K) is only marginally above Safety ($400.0K). Scale alone is not driving outsized productivity.

3. **Corporate overhead drags the average down:** The company-wide figure ($361.4K) is ~10% below divisional averages because 43 Corporate employees generate no direct revenue. This is typical for a company of this size — corporate overhead represents 8.9% of total headcount.

4. **Energy lags slightly:** Energy's $388.8K per employee is the lowest among divisions. This could reflect the heavier field-service component of the Energy business, which requires more personnel per dollar of revenue than Industrial distribution or Safety product sales.

## Data Sources

| Metric | System | Table |
|---|---|---|
| Industrial revenue | Salesforce CRM | `sf_opportunities` |
| Energy revenue | Legacy CRM | `orders` |
| Safety revenue | HubSpot CRM | `hs_deals` |
| Headcount | Workday HR | `wd_employees` |
