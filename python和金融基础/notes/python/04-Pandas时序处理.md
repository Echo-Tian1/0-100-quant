# 04 | DataFrame 基础与时间序列

#python #pandas #时序

## DataFrame 创建与索引

```python
df = pd.DataFrame({
    'date': pd.date_range('2026-01-01', periods=5),
    'close': [100, 102, 101, 105, 107],
    'volume': [1000, 1200, 800, 1500, 1100]
})
df.set_index('date', inplace=True)
```

### 三种索引方式

```python
df['close']              # 选列 → Series
df[['close', 'volume']]  # 选多列 → DataFrame
df.loc['2026-01-03']     # 按标签选行
df.iloc[2]               # 按位置选行（第3行）
df.loc['2026-01-02':'2026-01-04']  # 切片（两端都包含！）

# 条件筛选
df[df['close'] > 103]
df[(df['close'] > 100) & (df['volume'] > 1000)]  # 多条件用 & |
```

> ⚠️ `loc` 切片两端**都包含**，Python 切片只包含左端

---

## 时间序列处理

### 日期索引转换

```python
df.index = pd.to_datetime(df.index)    # 转为 DatetimeIndex
df = df.sort_index()                   # 按日期排序（很重要！）
```

### 时间范围筛选

```python
df.last('3M')          # 最近 3 个月
df.last('1Y')          # 最近 1 年
df['2026-01']          # 2026 年 1 月全部
df['2026-01':'2026-03']  # 1 月到 3 月
```

### resample 降频

```python
df.resample('W').last()     # 周频（取每周最后一天）
df.resample('M').mean()     # 月频（取月均值）
df.resample('Q').sum()      # 季度频（求和）
```

### rolling 滚动窗口

```python
df['MA5'] = df['close'].rolling(5).mean()     # 5 日均线
df['vol20'] = df['close'].pct_change().rolling(20).std() * np.sqrt(252)
df['max_high'] = df['high'].rolling(20).max()  # 20 日最高
```

### resample vs rolling

| | resample | rolling |
|---|---------|---------|
| 作用 | 降频（日→周/月） | 滚动窗口计算 |
| 结果行数 | 减少 | 不变 |
| 典型用途 | 月度收益统计 | 移动均线、波动率 |

---

## 常用统计函数

```python
df['close'].pct_change()         # 日收益率（百分比变化）
df['close'].pct_change().shift(1)  # 前一天的收益率
df['close'].diff()               # 日价差
df['close'].cummax()             # 累计最高（用于算回撤）
df['close'].rank(pct=True)       # 百分位排名
```

---

## 缺失值处理（量化关键）

```python
df.isnull().sum()                    # 各列空值数
df.dropna()                          # 删除含空值的行
df.fillna(method='ffill')            # 前向填充（时序首选）
df.fillna(method='bfill')            # 后向填充
df.interpolate()                     # 线性插值
df.fillna(df.mean())                 # 均值填充
```

> 时序数据用 `ffill`（用前一天的值填充），不要用均值

---

## 实战模式：从原始数据到指标

```python
# 完整流程
df = ak.stock_zh_a_hist(symbol='600519', period='daily', ...)
df['date'] = pd.to_datetime(df['日期'])
df.set_index('date', inplace=True)
df.sort_index(inplace=True)

df['return'] = df['收盘'].pct_change()
df['log_return'] = np.log(df['收盘'] / df['收盘'].shift(1))
df['MA20'] = df['收盘'].rolling(20).mean()
df['vol20'] = df['return'].rolling(20).std() * np.sqrt(252)
df['drawdown'] = df['收盘'] / df['收盘'].cummax() - 1
```

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| 日期列是字符串 | 必须 `pd.to_datetime()` 转换，否则切片不生效 |
| 索引未排序 | `.last()` 要求索引已排序，先 `sort_index()` |
| `SettingWithCopyWarning` | 用 `df.loc[:, 'col'] = values` 而非 `df['col'] = values` |
| `pct_change()` 第一行 | 是 `NaN`，记得 `dropna()` |
| `shift(1)` 方向 | `shift(1)` 是**往下**移（用前一天的值），不是往上 |

---

📁 对应 Notebook: `04_pandas_timeseries.ipynb`
⬅️ [[03-随机数与蒙特卡洛]] ➡️ [[05-AKShare均线波动率]]

---

## 顺序通关导航

- 上一课：[[03-随机数与蒙特卡洛]]
- 下一课：[[05-AKShare均线波动率]]
- 对应 Notebook：`04_pandas_timeseries.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
