# 10 | SciPy 统计分析

#quant #统计检验 #scipy #回归

## 假设检验核心逻辑

| 法庭 | 统计检验 | 含义 |
|------|---------|------|
| 无罪推定 | 原假设 H₀ | 默认「没有效果」 |
| 检察官举证 | 计算检验统计量 | 数据有多极端 |
| 证据强度 | P 值 | 假设 H₀ 为真，观测到当前结果的概率 |
| 判有罪 | P < α → 拒绝 H₀ | 证据充分 |
| 判无罪 | P ≥ α → 不拒绝 H₀ | 证据不足 |

> ⚠️ P 值**不是** H₀ 为真的概率！P = 0.03 不代表「有 97% 的把握」

---

## 正态性检验

```python
from scipy import stats

# JB 检验（看偏度 + 峰度）
jb_stat, jb_p = stats.jarque_bera(data)

# KS 检验（比较整体分布形状）
ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))

# Shapiro-Wilk（样本 < 5000 时最有力）
sw_stat, sw_p = stats.shapiro(data)
```

| 检验 | H₀ | 看什么 |
|------|-----|--------|
| JB | 正态分布 | 偏度=0 且峰度=0 |
| KS | 指定分布 | 经验分布 vs 理论分布的最大差距 |
| Shapiro | 正态分布 | 整体偏离程度 |

**解读**：P < 0.05 → 拒绝 H₀ → 数据**不服从**正态分布

### A 股收益率的现实

- 偏度 ≠ 0（左偏：大跌比大涨更频繁）
- 峰度 > 0（尖峰厚尾：极端事件比正态预测的多）
- → **不服从正态分布**，VaR 参数法会低估风险

---

## t 检验

```python
# 单样本：策略收益是否 ≠ 0？
t_stat, p = stats.ttest_1samp(strategy_returns, 0)

# 双样本：两个策略有差异？（先检验方差齐性）
lev_stat, lev_p = stats.levene(a, b)  # 方差是否相等
t_stat, p = stats.ttest_ind(a, b, equal_var=(lev_p > 0.05))

# 配对：优化前 vs 优化后
t_stat, p = stats.ttest_rel(after, before)
```

| 类型 | H₀ | 量化场景 |
|------|-----|---------|
| 单样本 | μ = 0 | 策略有超额收益？ |
| 双样本 | μ₁ = μ₂ | A 策略比 B 策略好？ |
| 配对 | μ_diff = 0 | 优化有效果？ |

> 双样本 t 检验前先用 `levene()` 检验方差齐性，方差不等时用 Welch t 检验

---

## 相关系数

```python
# Pearson（线性关系，假设正态）
r, p = stats.pearsonr(x, y)

# Spearman（单调关系，基于排名，抗离群值）
r, p = stats.spearmanr(x, y)

# Kendall（小样本，有序数据）
r, p = stats.kendalltau(x, y)
```

| 类型 | 衡量 | 抗离群值 | 适用 |
|------|------|---------|------|
| Pearson | 线性关系 | ❌ 敏感 | 连续、近似正态 |
| Spearman | 单调关系 | ✅ 稳健 | 非正态、有离群值 |
| Kendall | 排序一致性 | ✅ 稳健 | 小样本 |

**解读**：
- P < 0.05 → 相关性显著（不是偶然）
- |r| > 0.7 强相关，0.3-0.7 中等，< 0.3 弱
- **相关 ≠ 因果**！

### 相关系数矩阵 + 热力图

```python
corr = df.corr()

fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f'{corr.iloc[i,j]:.2f}', ha='center', va='center')
plt.colorbar(im)
```

---

## OLS 线性回归

```python
import statsmodels.api as sm

X = sm.add_constant(market_returns)  # 必须加截距项！
model = sm.OLS(stock_returns, X).fit()
print(model.summary())
```

### 关键输出解读

| 指标 | 含义 | 判断标准 |
|------|------|---------|
| `coef` | 系数（影响大小） | Beta > 1 波动大于市场 |
| `t值` | 系数 / 标准误 | |t| > 2 通常显著 |
| `P值` | 系数的显著性 | < 0.05 显著 |
| `R²` | 模型解释力 | 越接近 1 越好 |
| `adj. R²` | 调整 R² | 考虑变量个数，更公平 |
| `F 统计量` | 整体模型是否显著 | P < 0.05 显著 |

### CAPM 回归解读

```python
# stock_return = alpha + beta * market_return + epsilon
alpha = model.params[0]   # 截距 = 超额收益
beta = model.params[1]    # 斜率 = 市场敏感度
```

- Beta = 1.3 → 市场涨 1%，股票涨 1.3%
- Alpha > 0 且显著 → 有超额收益（真本事）
- Alpha 不显著 → 收益可能只是运气

---

## Q-Q 图解读

```python
stats.probplot(returns, dist='norm', plot=ax)
```

- 点在直线上 → 正态分布
- 两端偏离（S 形）→ 厚尾（极端事件多）
- 一端偏离 → 偏态（左偏或右偏）

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| `OLS` 忘加 `add_constant` | 没有截距项，结果全错 |
| 样本量太小 | t 检验需要足够样本（>30 通常安全） |
| 多重检验 | 测 100 个因子，5% 显著水平下平均有 5 个「假阳性」 |
| 相关 ≠ 因果 | 冰淇淋销量和溺水率正相关，都是因为夏天 |
| P 值误解 | P=0.03 不是「有 97% 把握」，是「如果 H₀ 为真，只有 3% 概率看到这个结果」 |

---

📁 对应 Notebook: `10_scipy_statistics.ipynb`
⬅️ [[09-K线布林带最大回撤]] ➡️ 股票筛选器（阶段项目1）

---

## 顺序通关导航

- 上一课：[[09-K线布林带最大回撤]]
- 下一课：[[11-股票筛选器]]
- 对应 Notebook：`10_scipy_statistics.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
