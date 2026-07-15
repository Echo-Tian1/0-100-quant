# CAPM与Beta

> 现代金融学基石，理解风险与收益的核心框架

#金融理论 #因子模型 #CAPM #Beta

---

## 核心概念

### CAPM公式

$$E(R_i) = R_f + \beta_i \cdot [E(R_m) - R_f]$$

| 符号 | 含义 | 典型值 |
|------|------|--------|
| $R_f$ | 无风险利率 | 10年期国债收益率 ≈ 2.5% |
| $\beta_i$ | 系统性风险系数 | 0.5 ~ 1.5 |
| $E(R_m) - R_f$ | 市场风险溢价 | 5% ~ 8% |

### Beta的经济含义

$$\beta_i = \frac{Cov(R_i, R_m)}{Var(R_m)} = \rho_{i,m} \cdot \frac{\sigma_i}{\sigma_m}$$

**解读：**
- **β > 1**: 进攻型（科技、券商）—— 市场涨10%，它涨12%
- **β = 1**: 与市场同步（大盘蓝筹）
- **0 < β < 1**: 防御型（公用事业、消费）—— 市场跌10%，它跌6%
- **β < 0**: 与市场反向（极少见，黄金有时）

### Alpha的来源

$$\alpha_i = R_i - [R_f + \beta_i \cdot (R_m - R_f)]$$

**Alpha可能来源：**
1. **市场无效** — 信息不对称、投资者非理性
2. **隐藏因子暴露** — 规模、价值、动量等未被CAPM捕捉的风险
3. **技能或运气** — 选股能力或随机噪声

⚠️ **警告**: 长期持续正Alpha极其罕见，大多数「Alpha」其实是隐藏的Beta

---

## 完整代码模式

### 全样本Beta计算

```python
import statsmodels.api as sm

def calculate_beta_full_sample(returns_df, stock_code):
    """全样本Beta计算"""
    X = sm.add_constant(returns_df['market'])
    y = returns_df[stock_code]
    model = sm.OLS(y, X).fit()

    return {
        'alpha': model.params['const'] * 252,  # 年化Alpha
        'beta': model.params['market'],
        'r_squared': model.rsquared,
        'alpha_tvalue': model.tvalues['const'],
        'beta_tvalue': model.tvalues['market'],
        'alpha_pvalue': model.pvalues['const']
    }
```

### 滚动窗口Beta

```python
def calculate_rolling_beta(returns_df, stock_code, window=60):
    """滚动窗口Beta计算"""
    rolling_beta = []
    dates = []

    for i in range(window, len(returns_df)):
        window_data = returns_df.iloc[i-window:i]
        X = sm.add_constant(window_data['market'])
        y = window_data[stock_code]
        model = sm.OLS(y, X).fit()
        rolling_beta.append(model.params['market'])
        dates.append(returns_df.index[i])

    return pd.DataFrame({'date': dates, 'beta': rolling_beta}).set_index('date')
```

### 按Beta分组分析

```python
def categorize_by_beta(beta_results):
    """按Beta分三组"""
    betas = {code: result['beta'] for code, result in beta_results.items()}
    sorted_stocks = sorted(betas.items(), key=lambda x: x[1])

    n = len(sorted_stocks)
    low = [s[0] for s in sorted_stocks[:n//3]]
    mid = [s[0] for s in sorted_stocks[n//3:2*n//3]]
    high = [s[0] for s in sorted_stocks[2*n//3:]]

    return {'低Beta': low, '中Beta': mid, '高Beta': high}
```

---

## 对比表格

### 全样本 vs 滚动窗口

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 全样本 | 简单、统计显著 | 忽略时变性 | 长期分析 |
| 滚动窗口 | 捕捉时变性 | 噪声大、窗口选择敏感 | 短期交易、动态对冲 |

### 不同Beta水平的特征

| Beta范围 | 类型 | 典型行业 | 市场表现 |
|----------|------|----------|----------|
| β > 1.3 | 高进攻型 | 券商、科技 | 牛市超涨，熊市超跌 |
| 1.0 ~ 1.3 | 中进攻型 | 周期股 | 跟随放大 |
| 0.7 ~ 1.0 | 中防御型 | 消费、医药 | 波动较小 |
| β < 0.7 | 高防御型 | 公用事业、银行 | 熊市抗跌 |

---

## 踩坑记录

### 1. 数据对齐问题

**问题**: 市场指数和个股交易日不一致

```python
# ❌ 错误：直接拼接
all_returns = pd.concat([market_returns, stock_returns], axis=1)

# ✅ 正确：inner join确保日期对齐
all_returns = pd.DataFrame({'market': market_returns})
all_returns = all_returns.join(stock_returns, how='inner')
```

### 2. 收益率计算顺序

**问题**: 先dropna还是先pct_change

```python
# ❌ 错误：第一行是NaN但没处理
returns = prices.pct_change()

# ✅ 正确：dropna
returns = prices.pct_change().dropna()
```

### 3. Alpha年化处理

**问题**: 日度Alpha和年化Alpha搞混

```python
# 日度Alpha
alpha_daily = model.params['const']

# 年化Alpha（简单年化）
alpha_annual = alpha_daily * 252

# 年化Alpha（复利年化）
alpha_annual = (1 + alpha_daily) ** 252 - 1
```

### 4. Beta的统计显著性

**问题**: 只看Beta大小，忽略t值

```python
# 需要检查beta_tvalue
if abs(model.tvalues['market']) > 2:
    print('Beta统计显著')
else:
    print('Beta不显著，可能是噪声')
```

---

## 关键洞察

1. **Beta的时变性**: Beta不是固定的，会随市场环境变化。牛市中高Beta股更Beta，熊市中Beta可能收缩

2. **低Beta异象**: 全球市场普遍存在——低Beta股票往往有更高的风险调整收益

3. **Alpha的稀缺性**: 大部分Alpha统计不显著，即使显著也要考虑数据挖掘偏差

4. **CAPM的局限**: 单因子模型，忽略了规模、价值、动量等因子。现实用多因子模型更有效

---

## 相关笔记

- [[13-Fama-French三因子模型]] — Fama-French三因子模型
- 因子投资概述
- 风险调整收益指标

---

## 对应Notebook

`12_capm_beta.ipynb`

---

## 顺序通关导航

- 上一课：[[11-股票筛选器]]
- 下一课：[[13-Fama-French三因子模型]]
- 对应 Notebook：`12_capm_beta.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
