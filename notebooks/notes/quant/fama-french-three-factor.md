# Fama-French 三因子模型

#量化理论 #因子模型 #资产定价

## 核心概念

### 模型公式

$$R_i - R_f = \alpha_i + \beta_i(R_m - R_f) + s_i \cdot SMB + h_i \cdot HML + \epsilon_i$$

| 符号 | 含义 | 计算方法 |
|------|------|----------|
| $R_i - R_f$ | 资产超额收益 | 资产收益 - 无风险利率 |
| $R_m - R_f$ | 市场超额收益 | 市场指数收益 - 无风险利率 |
| $SMB$ | 规模因子 | 小市值组合收益 - 大市值组合收益 |
| $HML$ | 价值因子 | 高B/M组合收益 - 低B/M组合收益 |
| $\alpha$ | 超额收益 | 回归截距，应接近0 |
| $\beta, s, h$ | 因子暴露 | 回归系数 |

## 因子构建方法

### SMB（Small Minus Big）

```python
def build_smb(df):
    # 1. 按市值中位数分组
    median_cap = df['market_cap'].median()
    small = df[df['market_cap'] <= median_cap]
    big = df[df['market_cap'] > median_cap]

    # 2. 计算市值加权收益
    def weighted_return(sub_df):
        weights = sub_df['market_cap'] / sub_df['market_cap'].sum()
        return (sub_df['return'] * weights).sum()

    # 3. SMB = 小市值收益 - 大市值收益
    return weighted_return(small) - weighted_return(big)
```

### HML（High Minus Low）

```python
def build_hml(df):
    # 1. 按 B/M 比分三组
    q30 = df['bm_ratio'].quantile(0.3)
    q70 = df['bm_ratio'].quantile(0.7)
    high_bm = df[df['bm_ratio'] >= q70]  # 价值股
    low_bm = df[df['bm_ratio'] <= q30]   # 成长股

    # 2. 市值加权收益
    def weighted_return(sub_df):
        weights = sub_df['market_cap'] / sub_df['market_cap'].sum()
        return (sub_df['return'] * weights).sum()

    # 3. HML = 高B/M收益 - 低B/M收益
    return weighted_return(high_bm) - weighted_return(low_bm)
```

## 回归分析代码模式

```python
import statsmodels.api as sm

# 准备数据
X = factors_df[['Rm_Rf', 'SMB', 'HML']]
X = sm.add_constant(X)  # 添加截距
y = portfolio_returns - rf

# OLS 回归
model = sm.OLS(y, X).fit()

# 关键指标
print(f"Alpha: {model.params['const']:.6f}")
print(f"Beta:  {model.params['Rm_Rf']:.4f}")
print(f"s:     {model.params['SMB']:.4f}")
print(f"h:     {model.params['HML']:.4f}")
print(f"R²:    {model.rsquared:.4f}")

# 显著性检验
for factor in ['const', 'Rm_Rf', 'SMB', 'HML']:
    t_stat = model.tvalues[factor]
    p_value = model.pvalues[factor]
    significant = "✓ 显著" if p_value < 0.05 else "✗ 不显著"
    print(f"{factor}: t={t_stat:.3f}, p={p_value:.4f} {significant}")
```

## 结果解读指南

### t 值和 p 值

| t值 | p值 | 含义 |
|-----|-----|------|
| \|t\| > 2.58 | p < 0.01 | 高度显著 *** |
| \|t\| > 1.96 | p < 0.05 | 显著 ** |
| \|t\| > 1.65 | p < 0.10 | 边际显著 * |
| \|t\| < 1.65 | p > 0.10 | 不显著 |

### R² 解释

- **R² > 0.8**：模型解释力很强
- **0.5 < R² < 0.8**：模型解释力较好
- **R² < 0.5**：模型解释力较弱，可能遗漏重要因子

### 因子暴露含义

| 因子 | 系数符号 | 含义 |
|------|----------|------|
| SMB | s > 0 | 偏向小市值股票 |
| SMB | s < 0 | 偏向大市值股票 |
| HML | h > 0 | 偏向价值股（高B/M） |
| HML | h < 0 | 偏向成长股（低B/M） |

## 对比：CAPM vs Fama-French

| 特性 | CAPM | Fama-French |
|------|------|-------------|
| 因子数量 | 1个（市场） | 3个（市场+规模+价值） |
| 公式 | $R_i-R_f=\beta(R_m-R_f)$ | + SMB + HML |
| 解释力 | 较弱 | 较强 |
| 异象处理 | 无法解释 | 解释规模/价值效应 |
| 复杂度 | 简单 | 中等 |

## 踩坑记录

### 1. 市值加权 vs 等权重
- **错误**：直接用算术平均
- **正确**：用市值加权，大公司权重更高
```python
weights = market_cap / market_cap.sum()
portfolio_return = (returns * weights).sum()
```

### 2. 分组时间点
- **错误**：每月重新分组
- **正确**：每年6月底分组，持有至次年6月（避免频繁换手）

### 3. B/M 比计算
- **错误**：用当前市值
- **正确**：用上一年末的账面价值 / 当前市值

### 4. 回归前数据对齐
- **错误**：因子和收益数据时间不对齐
- **正确**：确保所有序列日期一致

## 相关笔记

- [[capm-beta]] - CAPM 模型和 Beta 计算
- [[portfolio-optimization]] - 投资组合优化
- [[factor-investing]] - 因子投资概述

## 对应 Notebook

- `14_fama_french.ipynb`

## 参考资料

- Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds.
- [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
