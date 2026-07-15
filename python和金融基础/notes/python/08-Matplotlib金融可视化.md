# 08 | Matplotlib 金融可视化

#python #matplotlib #可视化 #mplfinance

## 中文字体配置（macOS）

```python
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'SimHei', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False  # 负号用 ASCII '-'
```

> 如果中文还是方块，检查字体名是否拼对，或用 `FontProperties` 局部指定

---

## 手绘 K 线（理解底层）

```python
import matplotlib.patches as mpatches
import matplotlib.dates as mdates

def draw_candlestick(ax, df, width=0.6, colorup='#DC143C', colordown='#228B22'):
    dates = mdates.date2num(df.index.to_pydatetime())
    for date, row in zip(dates, df.itertuples()):
        if row.Close >= row.Open:
            color, bot, h = colorup, row.Open, row.Close - row.Open
        else:
            color, bot, h = colordown, row.Close, row.Open - row.Close
        ax.plot([date, date], [row.Low, row.High], color=color, lw=0.8)
        ax.add_patch(mpatches.Rectangle(
            (date - width/2, bot), width, max(h, 0.01),
            facecolor=color if h > 0 else 'none', edgecolor=color))
```

---

## mplfinance 快速出图

```python
import mplfinance as mpf

# 基础 K 线 + 成交量
mpf.plot(df, type='candle', style='charles', mav=(5, 20), volume=True)

# 叠加自定义指标
apds = [
    mpf.make_addplot(df['MA5'], color='red', width=1.2),
    mpf.make_addplot(df['BB_UP'], color='purple', width=0.8, linestyle='--'),
    mpf.make_addplot(df['BB_DN'], color='purple', width=0.8, linestyle='--'),
]
mpf.plot(df, type='candle', addplot=apds, volume=True, figsize=(16, 9))
```

> ⚠️ `make_addplot` 用 `width` 控制线宽，**不是** `linewidth`（踩过的坑）

### 自定义风格

```python
mc = mpf.make_marketcolors(up='red', down='green', edge='inherit',
                            volume={'up': '#EF5350', 'down': '#26A69A'})
s = mpf.make_mpf_style(marketcolors=mc, gridcolor='#E0E0E0', facecolor='white')
mpf.plot(df, style=s, ...)
```

---

## 收益率分布诊断

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 左：直方图 + KDE + 正态叠加
ax1.hist(returns, bins=40, density=True, alpha=0.5, color='steelblue')
sns.kdeplot(returns, ax=ax1, color='darkblue', lw=2.5)
x = np.linspace(returns.min(), returns.max(), 500)
ax1.plot(x, stats.norm.pdf(x, returns.mean(), returns.std()), 'r--', lw=2)

# 右：Q-Q 图（偏离直线 = 偏离正态）
stats.probplot(returns, dist='norm', plot=ax2)
```

---

## 多子图布局

### subplots 等分

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
# axes[0,0] axes[0,1] axes[1,0] axes[1,1]
```

### GridSpec 不等分

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(18, 9))
gs = GridSpec(4, 6, figure=fig, hspace=0.35, wspace=0.4)

ax1 = fig.add_subplot(gs[0:3, 0:4])   # 大图：3行4列
ax2 = fig.add_subplot(gs[3, 0:4])     # 底部：1行4列（成交量）
ax3 = fig.add_subplot(gs[0:2, 4:6])   # 右上：2行2列（分布）
ax4 = fig.add_subplot(gs[2:4, 4:6])   # 右下：2行2列（统计表）
```

### 双 Y 轴

```python
ax5 = fig.add_subplot(gs[2, 2])
ax5.plot(dates, volatility, color='steelblue')
ax5.set_ylabel('波动率', color='steelblue')

ax5b = ax5.twinx()
ax5b.plot(dates, cum_return, color='red')
ax5b.set_ylabel('累计收益', color='red')
```

---

## 格式化器

```python
# 日期格式
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 数字格式（成交量用 M 为单位）
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.0f}M'))

# 百分比格式
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.1%}'))
```

---

## 标注与箭头

```python
ax.annotate(
    '最大回撤 -15%',
    xy=(mdd_date, mdd_price),           # 箭头指向
    xytext=(mdd_date, mdd_price * 1.05), # 文字位置
    fontsize=11, fontweight='bold', color='red',
    ha='center',
    bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='red', alpha=0.85),
    arrowprops=dict(arrowstyle='->', color='red', lw=1.5)
)

# 区域标注
ax.axvspan(start_date, end_date, alpha=0.15, color='red')
```

---

## 保存高清图片

```python
fig.savefig('output.png', dpi=200, bbox_inches='tight', facecolor='white')
```

| 参数 | 说明 |
|------|------|
| `dpi=200` | 高清（屏幕用 100，打印用 300） |
| `bbox_inches='tight'` | 裁掉多余白边 |
| `facecolor='white'` | 背景白色（默认透明） |

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| 中文方块 | 字体名拼错或不在系统中，用 `fm.fontManager.ttflist` 查看可用字体 |
| 负号变方块 | `axes.unicode_minus = False` |
| `make_addplot` 参数 | `width` 不是 `linewidth` |
| 图例不显示 | `mpf.plot` 的图例需要在 `addplot` 里加 `label` |
| 子图重叠 | `plt.tight_layout()` 或手动调 `hspace/wspace` |

---

📁 对应 Notebook: `08_matplotlib_finance.ipynb`
⬅️ [[07-AKShare与SQLite]] ➡️ [[09-K线布林带最大回撤]]

---

## 顺序通关导航

- 上一课：[[07-AKShare与SQLite]]
- 下一课：[[09-K线布林带最大回撤]]
- 对应 Notebook：`08_matplotlib_finance.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
