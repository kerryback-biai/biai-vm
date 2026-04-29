import pandas as pd
import openpyxl
from datetime import datetime

# ==============================
# Load portfolio lots
# ==============================
lots = pd.read_excel('data/portfolio/portfolio_lots.xlsx')
print(f"Portfolio lots: {len(lots)} rows")
print(f"Columns: {list(lots.columns)}")
print(f"Unique tickers: {lots['Ticker'].nunique()}")
print()

# ==============================
# Try MotherDuck connection
# ==============================
MOTHERDUCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhLWMxMThlYzUzLTZkNDItNGYwNC1hNjg2LTI3Y2IzMTYyZDFjYkBzYS5tb3RoZXJkdWNrLmNvbSIsInNlc3Npb24iOiJzYS1jMTE4ZWM1My02ZDQyLTRmMDQtYTY4Ni0yN2NiMzE2MmQxY2Iuc2EubW90aGVyZHVjay5jb20iLCJwYXQiOiJtWUZTX0FYMk5MV2pnWC1DT0p2a2VIQnJ5ek5RaGVSQllvWVlZUndOdU9zIiwidXNlcklkIjoiMjk0NDE0NmYtOWYwMy00NjUyLThlMzUtZTgzZjgwOTY5N2VlIiwiaXNzIjoibWRfcGF0IiwicmVhZE9ubHkiOmZhbHNlLCJ0b2tlblR5cGUiOiJyZWFkX3dyaXRlIiwiaWF0IjoxNzUzMDIzNzgzfQ.iYjIvy_FSJirhaFIxYka-J-6JHa9IEWxP8eVV05FaGI"

motherduck_ok = False
prices_df = None
recs_df = None

try:
    import duckdb
    conn = duckdb.connect(f"md:student_stocks?motherduck_token={MOTHERDUCK_TOKEN}")

    # Get current prices for our tickers
    tickers = lots['Ticker'].unique().tolist()
    ticker_str = ",".join([f"'{t}'" for t in tickers])

    prices_df = conn.execute(f"""
        SELECT p.ticker, p.close, p.marketcap, p.pb,
               r.recommendation
        FROM prices p
        JOIN recommendations r ON p.ticker = r.ticker
        WHERE p.ticker IN ({ticker_str})
    """).fetchdf()

    print("MotherDuck connection: SUCCESS")
    print(f"Retrieved prices for {len(prices_df)} of {len(tickers)} tickers")
    motherduck_ok = True

    # Check which tickers are missing
    found = set(prices_df['ticker'].values)
    missing = [t for t in tickers if t not in found]
    if missing:
        print(f"Missing tickers: {missing}")

    conn.close()
except Exception as e:
    print(f"MotherDuck connection FAILED: {e}")
    print("Will proceed with cost-basis-only analysis.")

# ==============================
# Portfolio analysis
# ==============================
if motherduck_ok and prices_df is not None:
    # Merge current prices into lots
    lots = lots.merge(prices_df[['ticker','close','recommendation']],
                      left_on='Ticker', right_on='ticker', how='left')

    # Current value per lot
    lots['Current Value'] = lots['Shares'] * lots['close']
    lots['Unrealized Gain'] = lots['Current Value'] - lots['Cost']
    lots['Holding Period'] = (datetime(2026, 4, 28) - lots['Date']).dt.days
    lots['Long Term'] = lots['Holding Period'] > 365

    total_value = lots['Current Value'].sum()
    total_cost = lots['Cost'].sum()
    total_unrealized = lots['Unrealized Gain'].sum()

    print(f"\n{'='*60}")
    print(f"PORTFOLIO SUMMARY")
    print(f"{'='*60}")
    print(f"Total current value: ${total_value:,.2f}")
    print(f"Total cost basis:    ${total_cost:,.2f}")
    print(f"Total unrealized G/L: ${total_unrealized:,.2f}")
    print(f"Number of lots:      {len(lots)}")
    print(f"Number of stocks:    {lots['Ticker'].nunique()}")

    # Sector weights
    sector_value = lots.groupby('Sector')['Current Value'].sum()
    sector_weights = (sector_value / total_value * 100).sort_values(ascending=False)

    targets = {
        'Technology': 25.38, 'Financial Services': 13.19, 'Healthcare': 9.66,
        'Consumer Cyclical': 9.33, 'Communication Services': 8.40, 'Industrials': 7.91,
        'Consumer Defensive': 5.48, 'Energy': 3.74, 'Real Estate': 2.40,
        'Basic Materials': 2.32, 'Utilities': 2.19
    }
    # Money market target is 10%, but we have no money market in the portfolio

    print(f"\n{'='*60}")
    print(f"SECTOR WEIGHTS vs TARGETS")
    print(f"{'='*60}")
    print(f"{'Sector':<25} {'Current':>8} {'Target':>8} {'Diff':>8} {'Flag':>6}")
    print(f"{'-'*55}")

    all_sectors = set(list(sector_weights.index) + list(targets.keys()))
    for sector in sorted(all_sectors):
        current = sector_weights.get(sector, 0)
        target = targets.get(sector, 0)
        diff = current - target
        flag = " ***" if abs(diff) > 3 else ""
        print(f"{sector:<25} {current:>7.2f}% {target:>7.2f}% {diff:>+7.2f}%{flag}")

    # Money market
    print(f"{'Money Market':<25} {'0.00':>7}% {'10.00':>7}% {'-10.00':>7}%{'  ***':>6}")

    # Sell-rated stocks
    print(f"\n{'='*60}")
    print(f"SELL-RATED STOCKS")
    print(f"{'='*60}")

    sell_lots = lots[lots['recommendation'] == 'Sell'].copy()
    sell_by_ticker = sell_lots.groupby('Ticker').agg({
        'Current Value': 'sum',
        'Cost': 'sum',
        'Unrealized Gain': 'sum',
        'Shares': 'sum',
        'Sector': 'first',
        'close': 'first'
    }).sort_values('Current Value', ascending=False)

    sell_pct = sell_by_ticker['Current Value'].sum() / total_value * 100
    print(f"Sell-rated stocks: {len(sell_by_ticker)} stocks, {len(sell_lots)} lots")
    print(f"Value in Sell-rated: ${sell_by_ticker['Current Value'].sum():,.2f} ({sell_pct:.1f}% of portfolio)")
    print()

    print(f"{'Ticker':<8} {'Sector':<25} {'Value':>12} {'Cost':>12} {'Gain':>12} {'% Port':>8}")
    print(f"{'-'*77}")
    for ticker, row in sell_by_ticker.iterrows():
        pct = row['Current Value'] / total_value * 100
        print(f"{ticker:<8} {row['Sector']:<25} ${row['Current Value']:>10,.2f} ${row['Cost']:>10,.2f} ${row['Unrealized Gain']:>10,.2f} {pct:>7.2f}%")

    # Tax cost if selling all Sell-rated
    # Top federal rates per exercise prompt: 20% long-term, 37% short-term
    lt_gains = sell_lots[sell_lots['Long Term'] & (sell_lots['Unrealized Gain'] > 0)]['Unrealized Gain'].sum()
    st_gains = sell_lots[~sell_lots['Long Term'] & (sell_lots['Unrealized Gain'] > 0)]['Unrealized Gain'].sum()
    lt_losses = sell_lots[sell_lots['Long Term'] & (sell_lots['Unrealized Gain'] < 0)]['Unrealized Gain'].sum()
    st_losses = sell_lots[~sell_lots['Long Term'] & (sell_lots['Unrealized Gain'] < 0)]['Unrealized Gain'].sum()

    lt_tax = lt_gains * 0.20
    st_tax = st_gains * 0.37
    lt_loss_benefit = lt_losses * 0.20  # losses offset gains at same rate
    st_loss_benefit = st_losses * 0.37
    losses = lt_losses + st_losses
    loss_benefit = lt_loss_benefit + st_loss_benefit
    total_tax = lt_tax + st_tax + loss_benefit  # loss_benefit is negative

    print(f"\nTAX COST IF ALL SELL-RATED SOLD:")
    print(f"  Long-term gains:  ${lt_gains:>10,.2f} (tax @ 20%: ${lt_tax:>10,.2f})")
    print(f"  Short-term gains: ${st_gains:>10,.2f} (tax @ 37%: ${st_tax:>10,.2f})")
    print(f"  Losses:           ${losses:>10,.2f} (benefit:   ${loss_benefit:>10,.2f})")
    print(f"  Total estimated tax: ${total_tax:>10,.2f}")

    # Single stock concentration
    stock_values = lots.groupby('Ticker')['Current Value'].sum()
    stock_pcts = (stock_values / total_value * 100).sort_values(ascending=False)
    over_5 = stock_pcts[stock_pcts > 5]

    print(f"\n{'='*60}")
    print(f"CONCENTRATION CHECK (>5% single stock)")
    print(f"{'='*60}")
    if len(over_5) > 0:
        for ticker, pct in over_5.items():
            print(f"  {ticker}: {pct:.2f}%  *** OVER LIMIT")
    else:
        print("  No stocks over 5% -- all within limit")

    # Top 10 positions
    print(f"\nTop 10 positions:")
    for ticker, pct in stock_pcts.head(10).items():
        print(f"  {ticker}: {pct:.2f}%")

else:
    # Fallback: cost-basis-only analysis
    print("\nProceeding with cost-basis analysis only (no current prices)...")
    total_cost = lots['Cost'].sum()
    print(f"Total cost basis: ${total_cost:,.2f}")

    sector_cost = lots.groupby('Sector')['Cost'].sum()
    sector_pcts = (sector_cost / total_cost * 100).sort_values(ascending=False)
    print("\nSector weights (by cost basis):")
    for sector, pct in sector_pcts.items():
        print(f"  {sector}: {pct:.2f}%")
