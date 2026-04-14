import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV file
df = pd.read_csv('trades.csv')

# Filter for exit trades (where the trade is closed)
exit_trades = df[df['Type'].str.startswith('Exit')]

# Select relevant columns
trades = exit_trades[['Date and time', 'Net P&L USD']].copy()

# Convert date column to datetime
trades['Date and time'] = pd.to_datetime(trades['Date and time'])

# Sort by date
trades = trades.sort_values('Date and time')

# Rename columns for ease
trades.columns = ['Date', 'PnL']

# Calculate metrics
total_trades = len(trades)
winning_trades = (trades['PnL'] > 0).sum()
win_rate = winning_trades / total_trades if total_trades > 0 else 0

total_profit = trades[trades['PnL'] > 0]['PnL'].sum()
total_loss = abs(trades[trades['PnL'] < 0]['PnL'].sum())
profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')

# Equity curve
trades['Cumulative PnL'] = trades['PnL'].cumsum()

# Max Drawdown
trades['Peak'] = trades['Cumulative PnL'].cummax()
trades['Drawdown'] = trades['Peak'] - trades['Cumulative PnL']
max_drawdown = trades['Drawdown'].max()

# Sharpe Ratio (assuming daily returns, risk-free rate = 0)
# Group by date (day) for daily PnL
daily_pnl = trades.groupby(trades['Date'].dt.date)['PnL'].sum()
daily_equity = daily_pnl.cumsum()
daily_returns = daily_equity.pct_change().dropna()
sharpe_ratio = daily_returns.mean() / daily_returns.std() if daily_returns.std() > 0 else 0

# Print metrics
print(f"Total Trades: {total_trades}")
print(f"Win Rate: {win_rate:.2%}")
print(f"Profit Factor: {profit_factor:.2f}")
print(f"Max Drawdown: ${max_drawdown:.2f}")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Plot Equity Curve
plt.figure(figsize=(10, 6))
plt.plot(trades['Date'], trades['Cumulative PnL'], label='Equity Curve')
plt.title('Trading Performance - Equity Curve')
plt.xlabel('Date')
plt.ylabel('Cumulative P&L ($)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('performance.png')