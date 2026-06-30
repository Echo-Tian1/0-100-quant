# 05 | AKShare 数据源 + 均线 + 滚动波动率

#python #pandas #akshare #均线 #波动率

## AKShare 获取数据

```python
import akshare as ak

# 个股日线（最常用）
df = ak.stock_zh_a_hist(
    symbol='600519',       # 股票代码
    period='daily',        # 日线
    start_date='20240101', # 开始日期
    end_date='20260101',   # 结束日期
    adjust='qfq'           # 前复权（推荐）
)
```

### 复权方式对比

| 类型 | 说明 | 用途 |
|------|------|------|
| `qfq` 前复权 | 以最新价格为基准，往前调整 | 技术分析（推荐） |
| `hfq` 后复权 | 以发行价为基准，往后调整 | 计算真实收益率 |
| `''` 不复权 | 原始价格 | 查看真实成交价 |

> 不复权的价格在除权日会跳空，均线会断，技术分析**必须**用复权

### 其他数据源

```python
# 指数日线
df = ak.stock_zh_index_daily_em(symbol='sh000300')  # 沪深300

# 行业板块
df = ak.stock_board_industry_hist_em(symbol='半导体', period='daily',
                                      start_date='20260101', end_date='20260531')
```

---

## 移动均线（MA）

```python
df['MA5']  = df['收盘'].rolling(5).mean()
df['MA20'] = df['收盘'].rolling(20).mean()
df['MA60'] = df['收盘'].rolling(60).mean()
```

### 金叉/死叉检测

```python
df['MA5_above'] = df['MA5'] > df['MA20']
df['MA5_above_prev'] = df['MA5_above'].shift(1)

# 金叉：昨天 MA5 ≤ MA20，今天 MA5 > MA20
df['golden_cross'] = (~df['MA5_above_prev'].fillna(False)) & df['MA5_above']
# 死叉：反过来
df['death_cross'] = df['MA5_above_prev'].fillna(False) & (~df['MA5_above'])
```

### 均线斜率（趋势强度）

```python
df['MA20_slope'] = df['MA20'].pct_change(5)  # 5日变化率
# > 0 向上趋势，< 0 向下趋势，绝对值越大趋势越强
```

---

## 滚动波动率

```python
returns = df['收盘'].pct_change()

# 20 日滚动波动率（年化）
df['vol20'] = returns.rolling(20).std() * np.sqrt(252)

# 滚动偏度和峰度
df['skew20'] = returns.rolling(20).skew()
df['kurt20'] = returns.rolling(20).kurt()
```

> 252 = A 股一年交易日。年化 = 日标准差 × √252

### 波动率的含义

| vol20 值 | 含义 |
|----------|------|
| < 15% | 低波动（蓝筹、银行） |
| 15-30% | 中等波动（消费、医药） |
| 30-50% | 高波动（科技、新能源） |
| > 50% | 极高波动（概念股、ST） |

---

## IQR 异常值检测

```python
Q1 = df['收盘'].quantile(0.25)
Q3 = df['收盘'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 3 * IQR
upper = Q3 + 3 * IQR
outliers = (df['收盘'] < lower) | (df['收盘'] > upper)
print(f"异常值数量: {outliers.sum()}")
```

---

## 数据清洗 Checklist

```python
# 1. 列名统一（中→英或英→中）
df = df.rename(columns={'日期': 'date', '收盘': 'close', ...})

# 2. 日期索引
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.sort_index(inplace=True)

# 3. 数值类型
for col in ['open', 'high', 'low', 'close', 'volume']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 4. 缺失值
print(df.isnull().sum())
df = df.dropna()  # 或 ffill

# 5. 异常值检查
# ... IQR 法 ...
```

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| 不复权做均线 | 除权日跳空，均线断崖式变化 |
| `rolling(20)` 前 19 行 | 是 `NaN`，记得处理 |
| 年化因子 | 日线用 √252，周线用 √52，月线用 √12 |
| `pct_change()` 第一行 | `NaN`，与 `rolling` 的 `NaN` 叠加要注意顺序 |

---

📁 对应 Notebook: `05_akshare_ma_volatility.ipynb`
⬅️ [[04-Pandas时序处理]] ➡️ [[06-Pandas数据清洗]]

---

## 顺序通关导航

- 上一课：[[04-Pandas时序处理]]
- 下一课：[[06-Pandas数据清洗]]
- 对应 Notebook：`05_akshare_ma_volatility.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
