# 20 Markowitz 均值方差优化

> 模块 2.3 — 风控与优化 | [[00-主页]] | `20_Markowitz_Portfolio_Optimization.ipynb`

#quant #组合优化 #Markowitz #有效前沿 #PyPortfolioOpt

---

## 核心概念

### Markowitz 框架（1952）

**问题**：给定 $n$ 个资产，如何分配权重以在给定风险下最大化收益？

**数学表述**：

- 组合收益：$\mu_p = \mathbf{w}^T\boldsymbol{\mu}$
- 组合方差：$\sigma_p^2 = \mathbf{w}^T\Sigma\mathbf{w}$
- 夏普比：$S_p = (\mu_p - r_f)/\sigma_p$

### 三个关键组合

| 组合 | 优化目标 | 特点 |
|------|---------|------|
| **最小方差 (MVP)** | $\min \mathbf{w}^T\Sigma\mathbf{w}$ | 纯风险最小化，有闭式解 |
| **最大夏普比 (MSR)** | $\max (\mu_p-r_f)/\sigma_p$ | 风险调整收益最优，需数值优化 |
| **等权 (1/n)** | $w_i=1/n$ | 基准对照，无优化 |

---

## 完整代码模式

### 1. 最小方差组合 — 拉格朗日解析解

$$\mathbf{w}_{MVP} = \frac{\Sigma^{-1}\mathbf{1}}{\mathbf{1}^T\Sigma^{-1}\mathbf{1}}$$

```python
Sigma_inv = np.linalg.inv(Sigma)
ones = np.ones(n)
w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)
```

### 2. 最大夏普比 — scipy 数值优化

```python
from scipy.optimize import minimize

def neg_sharpe(w, mu, Sigma, rf=0.02):
    ret = w @ mu
    vol = np.sqrt(w @ Sigma @ w)
    return -(ret - rf) / vol

# 约束：权重和为1，不做空
constraints = ({'type': 'eq', 'fun': lambda w: w.sum() - 1})
bounds = tuple((0, 1) for _ in range(n))

result = minimize(neg_sharpe, np.ones(n)/n, args=(mu, Sigma),
                  method='SLSQP', bounds=bounds, constraints=constraints)
w_msr = result.x
```

### 3. 构建有效前沿

对每个目标收益 $\mu_{target}$，求最小方差：

```python
def min_variance_for_target(target_return, mu, Sigma):
    constraints = [
        {'type': 'eq', 'fun': lambda w: w.sum() - 1},
        {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
    ]
    bounds = tuple((0, 1) for _ in range(n))
    result = minimize(lambda w: w @ Sigma @ w, w0,
                      method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x, np.sqrt(result.fun)
```

### 4. PyPortfolioOpt 一行搞定

```python
from pypfopt import EfficientFrontier, expected_returns, risk_models

mu = expected_returns.mean_historical_return(returns)
S = risk_models.sample_cov(returns)

ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
weights = ef.max_sharpe(risk_free_rate=0.02)
perf = ef.portfolio_performance(risk_free_rate=0.02)
# → (收益, 波动, 夏普比)
```

---

## 分散化的数学原理

两个资产的组合方差：

$$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\sigma_2$$

当 $\rho < 1$：$\sigma_p < w_1\sigma_1 + w_2\sigma_2$ — **风险小于加权平均**。

当 $\rho \to -1$：可构造零风险组合。

---

## 两基金分离定理

> 有效前沿上的**任意组合**都可以由两个有效基金（如 MVP 和 MSR）线性组合而成。

这意味着投资者只需要选择风险偏好（在 MVP 和 MSR 之间），不需要关心具体股票。

---

## 约束条件的影响

| 约束 | 效果 |
|------|------|
| 无约束 | 最优解可能包含极端负权重（做空） |
| $w_i \geq 0$ | 不允许做空，前沿缩短 |
| $w_i \leq 0.4$ | 限制集中度，夏普比略降 |
| $0.05 \leq w_i \leq 0.35$ | 最严格，夏普比进一步下降 |

**核心洞察**：约束越紧 → 可行域越小 → 最优夏普比越低（无免费午餐）。

---

## 踩坑记录

1. **输入敏感性问题**：期望收益的微小变化会导致权重剧烈波动。解决方案：使用 Black-Litterman 或收缩估计。
2. **样本协方差的噪声**：用历史协方差直接优化 → 权重极端。建议：Ledoit-Wolf 收缩、因子模型降维。
3. **事后优化偏差**：用全样本做优化再回测 → 严重高估表现。必须滚动窗口优化。
4. **优化器收敛问题**：SLSQP 可能卡在局部最优。尝试不同初始值、或用全局优化器（differential_evolution）。
5. **PyPortfolioOpt 的 `save_weights_to_file`**：保存结果便于后续复现。

---

## 对比：三种优化方法

| 方法 | 优点 | 缺点 |
|------|------|------|
| 拉格朗日解析解 | 精确、快速 | 仅适用简单约束（MVP） |
| scipy 数值优化 | 灵活、自定义约束 | 需要调初始值和算法 |
| PyPortfolioOpt | 专业、功能全、内置可视化 | 额外依赖 |

---

## 相关笔记

- [[19-VaR-CVaR]] — VaR/CVaR 是风险度量，Markowitz 是风险管理（优化）
- [[capm-beta]] — CAPM 的切线组合就是 Markowitz 的 MSR
- 下节 [[21-组合优化器]] — 整合 CAPM + 因子 + 优化的阶段项目（序号21）

---

📅 2026-06-15 | 📓 `20_Markowitz_Portfolio_Optimization.ipynb`
