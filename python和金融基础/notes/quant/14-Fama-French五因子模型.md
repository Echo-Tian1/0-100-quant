# Fama-French 五因子模型

#量化理论 #因子模型 #资产定价 #五因子

## 核心概念

### 为什么需要五因子？

三因子模型（市场、规模、价值）无法解释两个重要异象：
- **盈利效应**：高盈利公司收益 > 低盈利公司收益
- **投资效应**：保守投资公司收益 > 激进投资公司收益

### 模型公式

$$R_i - R_f = \alpha + \beta(R_m - R_f) + s \cdot SMB + h \cdot HML + r \cdot RMW + c \cdot CMA + \epsilon$$

| 因子 | 全称 | 构建方式 | 经济学故事 |
|------|------|----------|------------|
| $R_m - R_f$ | 市场因子 | 市场收益 - 无风险利率 | 系统性风险补偿 |
| $SMB$ | Small Minus Big | 小市值 - 大市值 | 规模效应 |
| $HML$ | High Minus Low | 高B/M - 低B/M | 价值效应 |
| $RMW$ | Robust Minus Weak | 高盈利 - 低盈利 | 盈利质量溢价 |
| $CMA$ | Conservative Minus Aggressive | 低投资 - 高投资 | 保守投资溢价 |

### RMW 的经济学逻辑

- 高盈利公司有更强的现金流创造能力
- 经济下行时更抗跌（防御性）
- 类似「质量因子」（Quality Factor）

### CMA 的经济学逻辑

- 激进投资（大量资本支出、并购）→ 更大不确定性
- 保守投资 → 更稳定的现金流和更低的财务风险
- 投资者要求更高回报来补偿激进投资的风险

## 因子构建方法

### RMW（Robust Minus Weak）盈利因子

```python
def build_rmw(df):
    # 1. 按盈利能力 30%/70% 分位数分三组
    q30 = df['profitability'].quantile(0.3)
    q70 = df['profitability'].quantile(0.7)

    robust = df[df['profitability'] >= q70]   # 高盈利
    weak = df[df['profitability'] <= q30]      # 低盈利

    # 2. 市值加权收益
    def weighted_return(sub_df):
        weights = sub_df['market_cap'] / sub_df['market_cap'].sum()
        return (sub_df['return'] * weights).sum()

    # 3. RMW = 高盈利收益 - 低盈利收益
    return weighted_return(robust) - weighted_return(weak)
```

### CMA（Conservative Minus Aggressive）投资因子

```python
def build_cma(df):
    # 1. 按投资率 30%/70% 分位数分三组
    q30 = df['investment_rate'].quantile(0.3)
    q70 = df['investment_rate'].quantile(0.7)

    conservative = df[df['investment_rate'] <= q30]  # 保守投资
    aggressive = df[df['investment_rate'] >= q70]     # 激进投资

    # 2. 市值加权收益
    def weighted_return(sub_df):
        weights = sub_df['market_cap'] / sub_df['market_cap'].sum()
        return (sub_df['return'] * weights).sum()

    # 3. CMA = 保守投资收益 - 激进投资收益
    return weighted_return(conservative) - weighted_return(aggressive)
```

## 因子构建速查表

| 因子 | 分组变量 | 做多 | 做空 | 分位数 |
|------|----------|------|------|--------|
| SMB | 市值 | 小市值 | 大市值 | 中位数 |
| HML | B/M 比 | 高 B/M | 低 B/M | 30%/70% |
| RMW | 盈利能力 | 高盈利 | 低盈利 | 30%/70% |
| CMA | 投资率 | 低投资 | 高投资 | 30%/70% |

## 三因子 vs 五因子对比

| 对比维度 | 三因子 | 五因子 |
|----------|--------|--------|
| 因子数量 | 3个 | 5个 |
| 捕获异象 | 规模、价值 | + 盈利、投资 |
| 调整 R² | 较低 | 更高 |
| HML 显著性 | 通常显著 | 可能被削弱 |
| 模型复杂度 | 中等 | 较高 |

### 为什么加入 RMW/CMA 后 HML 可能变弱？

RMW 和 CMA 与 HML 有相关性，它们捕获了 HML 中部分信息。Fama 认为这不意味着 HML 无用，而是盈利和投资特征与价值特征有重叠。

## 五因子回归代码模式

```python
import statsmodels.api as sm

# 五因子回归
X_5f = factors_df[['Rm_Rf', 'SMB', 'HML', 'RMW', 'CMA']]
X_5f = sm.add_constant(X_5f)
y = portfolio_returns - rf

model_5f = sm.OLS(y, X_5f).fit()

# 关键指标
print(f"Alpha: {model_5f.params['const']:.6f}")
print(f"Beta:  {model_5f.params['Rm_Rf']:.4f}")
print(f"s:     {model_5f.params['SMB']:.4f}")
print(f"h:     {model_5f.params['HML']:.4f}")
print(f"r:     {model_5f.params['RMW']:.4f}")   # 新增
print(f"c:     {model_5f.params['CMA']:.4f}")   # 新增
print(f"R²:    {model_5f.rsquared:.4f}")
print(f"调整R²: {model_5f.rsquared_adj:.4f}")
```

## 结果解读指南

### 因子暴露含义

| 系数 | 含义 | 举例 |
|------|------|------|
| $\beta > 1$ | 比市场波动更大 | 激进型基金 |
| $s > 0$ | 偏向小市值 | 小盘股基金 |
| $h > 0$ | 偏向价值股 | 价值投资策略 |
| $r > 0$ | 偏向高盈利 | 质量投资策略 |
| $c > 0$ | 偏向保守投资 | 低资本支出公司 |
| $\alpha > 0$ | 存在超额收益 | 选股能力（需检验显著性） |

### 嵌套模型 F 检验

检验 RMW 和 CMA 是否联合显著：

```python
from scipy import stats

rss_3f = np.sum(model_3f.resid ** 2)
rss_5f = np.sum(model_5f.resid ** 2)
n = len(y)

f_stat = ((rss_3f - rss_5f) / 2) / (rss_5f / (n - 6))
p_value = 1 - stats.f.cdf(f_stat, 2, n - 6)

# p < 0.05 → 新因子联合显著
```

## 踩坑记录

### 1. 盈利能力的代理变量
- **常见选择**：ROE、ROA、毛利率、营业利润率
- **建议**：ROE 最常用，但要注意金融行业杠杆率高，ROE 天然偏高

### 2. 投资率的代理变量
- **常见选择**：总资产增长率、资本支出/总资产、权益增长
- **Fama-French 原文**：用总资产增长率 (Asset Growth)
- **注意**：投资率为负（资产缩水）的公司要单独考虑

### 3. 因子方向搞反
- **RMW**：Robust - Weak，系数 r > 0 = 偏向高盈利 ✓
- **CMA**：Conservative - Aggressive，系数 c > 0 = 偏向低投资 ✓
- **常见错误**：把 CMA 搞反了，以为 c > 0 是偏向高投资 ✗

### 4. 多重共线性
- 五个因子之间可能有相关性
- 解决方案：检查 VIF（方差膨胀因子），或用正交化处理

### 5. 数据频率匹配
- 因子数据通常是月度/年度
- 收益率数据要和因子数据频率一致
- 财务数据有滞后性（如用上一年末的数据）

## 对比表格：三因子 vs 五因子 vs 其他模型

| 模型 | 因子 | 优势 | 局限 |
|------|------|------|------|
| CAPM | 1个 | 简单 | 无法解释异象 |
| FF三因子 | 3个 | 解释规模/价值效应 | 无法解释盈利/投资效应 |
| FF五因子 | 5个 | 更全面的异象解释 | HML 可能被削弱 |
| Carhart四因子 | 4个 | 加入动量 | 缺少盈利/投资 |

## 相关笔记

- [[12-CAPM贝塔系数]] - CAPM 模型和 Beta 计算
- [[13-Fama-French三因子模型]] - 三因子模型基础
- [[20-Markowitz-均值方差优化]] - 投资组合优化
- 因子投资概述

## 对应 Notebook

- `14_fama_french_five_factor.ipynb`

## 参考资料

- Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model.
- Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds.
- [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)

---

## 顺序通关导航

- 上一课：[[13-Fama-French三因子模型]]
- 下一课：[[15-因子模型总结]]
- 对应 Notebook：`14_fama_french_five_factor.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
