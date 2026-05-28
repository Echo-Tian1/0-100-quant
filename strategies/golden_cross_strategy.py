import vectorbt as vbt
import numpy as np
import pandas as pd

# ============================================================
# 参数设置
# ============================================================
symbol = "AAPL"             # 股票代码（仅用于标题）
fast_ma = 50                # 快线（短期均线）
slow_ma = 200               # 慢线（长期均线）
initial_capital = 10000     # 初始资金
fees = 0.001                # 手续费率 0.1%

# ============================================================
# 获取数据 — 优先尝试真实数据，失败则用模拟数据
# ============================================================
close = None

# 尝试从 yfinance 下载
try:
    data = vbt.YFData.download(symbol, start="2020-01-01", end="2024-12-31")
    close = data.get("Close")
    if close is not None and len(close) > 0:
        print(f"Using real data for {symbol}: {len(close)} days")
except Exception as e:
    print(f"YFinance unavailable ({e.__class__.__name__}), using synthetic data instead.")

# 后备：生成模拟数据（几何布朗运动 + 趋势）
if close is None or len(close) == 0:
    print("Generating synthetic OHLC data...")
    np.random.seed(42)
    n_days = 1250  # ~5 年交易日
    dates = pd.date_range("2020-01-01", periods=n_days, freq="B")

    # 几何布朗运动，带趋势和波动
    returns = np.random.randn(n_days) * 0.015 + 0.0003
    price = 100 * np.exp(np.cumsum(returns))

    close = pd.Series(price, index=dates, name="Close")
    symbol = "SYNTH"
    print(f"Generated {len(close)} days of synthetic data")

# ============================================================
# 计算均线
# ============================================================
fast_ma_series = vbt.MA.run(close, window=fast_ma).ma
slow_ma_series = vbt.MA.run(close, window=slow_ma).ma

# ============================================================
# 生成信号
# 金叉（快线上穿慢线）→ 买入
# 死叉（快线下穿慢线）→ 卖出
# ============================================================
entries = fast_ma_series.vbt.crossed_above(slow_ma_series)
exits = fast_ma_series.vbt.crossed_below(slow_ma_series)

print(f"Buy signals: {entries.sum()} | Sell signals: {exits.sum()}")

# ============================================================
# 回测
# ============================================================
portfolio = vbt.Portfolio.from_signals(
    close,
    entries=entries,
    exits=exits,
    init_cash=initial_capital,
    fees=fees,
    freq="1D"
)

# ============================================================
# 输出统计
# ============================================================
print("\n" + "=" * 55)
print(f"  金叉死叉策略回测 — MA{fast_ma} / MA{slow_ma}")
print("=" * 55)
print(portfolio.stats())

# ============================================================
# 可视化
# ============================================================

# 图1：价格 + 均线 + 买卖信号
fig1 = close.vbt.plot(trace_kwargs=dict(name="Close"))
fig1.add_scatter(
    x=fast_ma_series.index, y=fast_ma_series,
    mode="lines", name=f"MA{fast_ma}", line=dict(color="orange", width=1)
)
fig1.add_scatter(
    x=slow_ma_series.index, y=slow_ma_series,
    mode="lines", name=f"MA{slow_ma}", line=dict(color="blue", width=1)
)

buy_mask = entries.values
sell_mask = exits.values
if buy_mask.any():
    fig1.add_scatter(
        x=close.index[buy_mask], y=close[buy_mask],
        mode="markers", name="Buy (Golden Cross)",
        marker=dict(color="green", size=10, symbol="triangle-up")
    )
if sell_mask.any():
    fig1.add_scatter(
        x=close.index[sell_mask], y=close[sell_mask],
        mode="markers", name="Sell (Death Cross)",
        marker=dict(color="red", size=10, symbol="triangle-down")
    )

fig1.update_layout(title=f"{symbol} — Golden Cross / Death Cross (MA{fast_ma} / MA{slow_ma})")
fig1.show()

# 图2：资金曲线
fig2 = portfolio.value().vbt.plot()
fig2.update_layout(title="Equity Curve")
fig2.show()

# 图3：回撤
fig3 = portfolio.plot_drawdowns()
fig3.update_layout(title="Drawdown")
fig3.show()

# ============================================================
# 交易明细
# ============================================================
trades_df = portfolio.trades.records_readable
if len(trades_df) > 0:
    print("\nRecent trades:")
    print(trades_df.head(20).to_string())
