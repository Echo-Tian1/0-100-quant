# 06 | 数据清洗与合并（groupby / merge / pivot）

#python #pandas #数据清洗

## groupby 聚合

```python
# 单指标
df.groupby('行业')['PE'].mean()

# 多指标聚合
df.groupby('行业').agg(
    avg_pe=('PE', 'mean'),
    median_roe=('ROE', 'median'),
    count=('股票代码', 'count'),
    max_mv=('市值', 'max')
)

# 多级分组
df.groupby(['行业', '年份'])['PE'].mean().unstack()  # 行业×年份 透视
```

### agg 的两种写法

```python
# 命名聚合（推荐，清晰）
df.groupby('行业').agg(avg_pe=('PE', 'mean'))

# 字典聚合（简写）
df.groupby('行业').agg({'PE': 'mean', 'ROE': 'median'})
```

---

## merge 合并

```python
pd.merge(df_a, df_b, on='股票代码', how='inner')
```

| how | 保留什么 | 用途 |
|-----|---------|------|
| `inner` | 两边都有的 | 默认，最严格 |
| `left` | 左表全部 + 右表匹配 | 以左表为主 |
| `right` | 右表全部 + 左表匹配 | 少用 |
| `outer` | 所有都保留 | 找差异 |

### 多键合并

```python
pd.merge(df_a, df_b, on=['股票代码', '日期'], how='inner')
```

### 列名不同时

```python
pd.merge(df_a, df_b, left_on='code', right_on='股票代码', how='inner')
```

---

## pivot_table 透视表

```python
df.pivot_table(
    values='PE',          # 值
    index='行业',          # 行
    columns='年份',        # 列
    aggfunc='mean',        # 聚合函数
    fill_value=0           # 空值填充
)
```

### pivot_table vs groupby + unstack

```python
# 等价写法
df.pivot_table(values='PE', index='行业', columns='年份', aggfunc='mean')
df.groupby(['行业', '年份'])['PE'].mean().unstack()
```

---

## 缺失值处理策略

```python
df.isnull().sum()                    # 检查各列空值数
df.isnull().any(axis=1).sum()        # 有多少行含空值

# 删除
df.dropna()                          # 删除含空值的行
df.dropna(subset=['PE', 'ROE'])      # 只看这两列

# 填充
df.fillna(method='ffill')            # 前向填充（时序首选）
df.fillna(method='bfill')            # 后向填充
df.fillna(df.mean())                 # 均值填充
df.fillna({'PE': 0, 'ROE': df['ROE'].median()})  # 按列不同策略

# 插值
df.interpolate()                     # 线性插值
df.interpolate(method='time')        # 时间加权插值
```

### 量化场景的选择

| 场景 | 推荐方法 | 原因 |
|------|---------|------|
| 日线行情缺失 | `ffill` | 用前一天的价格 |
| 财务数据缺失 | `dropna` 或中位数 | 不同公司不可比 |
| 因子缺失 | `dropna` | 不应引入主观偏见 |

---

## 数据类型转换

```python
df['date'] = pd.to_datetime(df['date'])      # 字符串→日期
df['price'] = pd.to_numeric(df['price'], errors='coerce')  # 字符串→数字
df['code'] = df['code'].astype(str)          # 数字→字符串（股票代码！）
df['category'] = df['category'].astype('category')  # 节省内存
```

> ⚠️ 股票代码 `000001` 如果是 int 会变成 `1`，必须存为 str

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| `merge` 产生重复列 | 同名列会自动加 `_x` `_y`，用 `suffixes` 参数控制 |
| `groupby` 后索引变了 | 用 `.reset_index()` 恢复 |
| `pivot_table` 有空值 | 用 `fill_value=0` 填充 |
| `ffill` 的陷阱 | 如果第一天就是 NaN，`ffill` 也填不了，要先 `bfill` 再 `ffill` |
| `SettingWithCopyWarning` | 用 `df.loc[:, 'col'] = ...` 避免 |

---

📁 对应 Notebook: `06_pandas_groupby_merge_pivot_missing.ipynb`
⬅️ [[05-AKShare均线波动率]] ➡️ [[07-AKShare与SQLite]]

---

## 顺序通关导航

- 上一课：[[05-AKShare均线波动率]]
- 下一课：[[07-AKShare与SQLite]]
- 对应 Notebook：`06_pandas_groupby_merge_pivot_missing.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
