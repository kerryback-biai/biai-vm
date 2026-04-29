# Stock Database Access

Use this to query the stock database on MotherDuck. The database name is `student_stocks` and it contains three tables: `stocks`, `prices`, and `recommendations`.

## Setup

Install duckdb if it isn't already installed:

```python
import subprocess, sys
try:
    import duckdb
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb"])
    import duckdb
```

## Query Function

```python
import duckdb

MOTHERDUCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhLWMxMThlYzUzLTZkNDItNGYwNC1hNjg2LTI3Y2IzMTYyZDFjYkBzYS5tb3RoZXJkdWNrLmNvbSIsInNlc3Npb24iOiJzYS1jMTE4ZWM1My02ZDQyLTRmMDQtYTY4Ni0yN2NiMzE2MmQxY2Iuc2EubW90aGVyZHVjay5jb20iLCJwYXQiOiJtWUZTX0FYMk5MV2pnWC1DT0p2a2VIQnJ5ek5RaGVSQllvWVlZUndOdU9zIiwidXNlcklkIjoiMjk0NDE0NmYtOWYwMy00NjUyLThlMzUtZTgzZjgwOTY5N2VlIiwiaXNzIjoibWRfcGF0IiwicmVhZE9ubHkiOmZhbHNlLCJ0b2tlblR5cGUiOiJyZWFkX3dyaXRlIiwiaWF0IjoxNzUzMDIzNzgzfQ.iYjIvy_FSJirhaFIxYka-J-6JHa9IEWxP8eVV05FaGI"

def run_sql(query):
    """Run a SQL query against the MotherDuck student_stocks database and return a pandas DataFrame."""
    conn = duckdb.connect(f"md:student_stocks?motherduck_token={MOTHERDUCK_TOKEN}")
    result = conn.execute(query).fetchdf()
    conn.close()
    return result
```

## Tables

### stocks

Stock reference data for ~4,300 non-delisted U.S. equities.

| Column | Description |
|--------|-------------|
| ticker | Ticker symbol (e.g., AAPL) |
| name | Company name |
| sector | Sector (e.g., Technology, Healthcare, Energy) |
| industry | Industry (e.g., Consumer Electronics, Banks - Diversified) |
| exchange | Exchange (NYSE, NASDAQ) |
| scalemarketcap | Market cap size category (6 - Mega, 5 - Large, 4 - Mid, 3 - Small, 2 - Micro) |
| scalerevenue | Revenue size category |
| location | Company headquarters |
| siccode | SIC industry code |
| sicindustry | SIC industry description |
| sicsector | SIC sector description |
| famaindustry | Fama-French industry classification |
| currency | Trading currency (USD) |
| isdelisted | Delisting status (all N in this table) |

Sample rows:

| ticker | name | sector | industry | scalemarketcap | exchange |
|--------|------|--------|----------|----------------|----------|
| AAPL | APPLE INC | Technology | Consumer Electronics | 6 - Mega | NASDAQ |
| JPM | JPMORGAN CHASE & CO | Financial Services | Banks - Diversified | 6 - Mega | NYSE |
| XOM | EXXON MOBIL CORP | Energy | Oil & Gas Integrated | 6 - Mega | NYSE |
| JNJ | JOHNSON & JOHNSON | Healthcare | Drug Manufacturers - General | 6 - Mega | NYSE |
| MSFT | MICROSOFT CORP | Technology | Software - Infrastructure | 6 - Mega | NASDAQ |

### prices

Most recent closing price, market cap, and price-to-book ratio for each stock.

| Column | Description |
|--------|-------------|
| ticker | Ticker symbol |
| close | Most recent closing price in dollars |
| marketcap | Market capitalization in thousands of dollars |
| pb | Price-to-book ratio |

Sample rows:

| ticker | close | marketcap | pb |
|--------|-------|-----------|-----|
| AAPL | 270.23 | 3,967,284.5 | 45.0 |
| JPM | 310.29 | 836,862.2 | 2.3 |
| XOM | 146.44 | 610,180.8 | 2.4 |
| JNJ | 234.18 | 564,350.1 | 6.9 |
| MSFT | 422.79 | 3,139,481.7 | 8.0 |

### recommendations

Analyst recommendation for each stock, based on price-to-book percentile ranking.

| Column | Description |
|--------|-------------|
| ticker | Ticker symbol |
| recommendation | One of: Strong Buy, Buy, Hold, Sell |

The recommendations are assigned by P/B percentile: bottom 10% = Strong Buy, 10-30% = Buy, 30-70% = Hold, above 70% = Sell.

Sample rows:

| ticker | recommendation |
|--------|---------------|
| AAPL | Sell |
| JPM | Hold |
| XOM | Hold |
| JNJ | Sell |
| MSFT | Sell |

## Example Queries

```sql
-- Get all Technology stocks with a Buy recommendation
SELECT s.ticker, s.name, p.close, p.marketcap, r.recommendation
FROM stocks s
JOIN prices p ON s.ticker = p.ticker
JOIN recommendations r ON s.ticker = r.ticker
WHERE s.sector = 'Technology' AND r.recommendation = 'Buy'

-- Get sector summary
SELECT s.sector, COUNT(*) as n_stocks, AVG(p.pb) as avg_pb
FROM stocks s
JOIN prices p ON s.ticker = p.ticker
GROUP BY s.sector
ORDER BY n_stocks DESC
```
