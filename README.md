# algorithmic-trading-strategy
I built a trading algorithm with lookback and trailing SL which trades based on simple breakouts. This simple strategy was backtested on historical data which provided 94% returns in 6 years!
Strategy Overview:
 - Platform: QuantConnect (LEAN Engine)
- Asset Class: US Equities – Primary focus on SPY (S&P 500 ETF)
- Approach: Systematic trading with low turnover and position management logic
- Backtest Period: September 2017 – September 2023 (6 years)
- Starting Capital: $100,000
- Final Equity: $194,263.44
- Net Profit: $94,263.44 (+94.26%)
- Compounding Annual Return (CAR): 11.69%
- Sharpe Ratio: 0.591 (moderate risk-adjusted returns)
- Sortino Ratio: 0.555 (penalized for downside volatility)
- Max Drawdown: 16.5% (risk exposure is acceptable, not defensive)
