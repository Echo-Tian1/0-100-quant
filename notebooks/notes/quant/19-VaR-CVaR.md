# 19 VaR与CVaR：风险价值度量

> 模块 2.3 — 风控与优化 | [[00-主页]] | `19_VaR_CVaR.ipynb`

#quant #风控 #VaR #CVaR #蒙特卡洛

---

## 核心概念

### VaR（Value at Risk）

$$P(\text{损失} > \text{VaR}_\alpha) = 1 - \alpha$$

**一句话**：在置信水平 $\alpha$ 下，未来 T 天内最大可能损失。

| 置信度 | z值 | 含义 |
|--------|-----|------|
| 95% | -1.645 | 20天中有1天例外 |
| 99% | -2.326 | 100天中有1天例外 |

### CVaR（Expected Shortfall）

$$\text{CVaR}_\alpha = \mathbb{E}[\text{损失} \mid \text{损失} > \text{VaR}_\alpha]$$

**一句话**：超过 VaR 的那部分损失的平均值。

---

## 三种计算方法对比

| 方法 | 公式/思路 | 优点 | 缺点 | 适用场景 |
|------|----------|------|------|---------|
| 历史模拟法 | `-np.percentile(returns, 5)` | 不假设分布，直观 | 依赖历史 | 日常监控 |
| 参数法 | $-(μ + z_{0.05}·σ)$ | 极快，数学简洁 | 正态假设不成立 | 监管报告 |
| 蒙特卡洛法 | Cholesky + randn → 取分位数 | 灵活，可处理复杂组合 | 计算量大 | 非线性产品 |

---

## 完整代码模式

### 历史模拟法

```python
def var_historical(returns, confidence=0.95):
    return -np.percentile(returns, 100 * (1 - confidence))

def cvar_historical(returns, confidence=0.95):
    var = var_historical(returns, confidence)
    exceedances = returns[returns <= -var]
    return -exceedances.mean()
```

### 参数法（假设正态分布）

```python
from scipy import stats

def var_parametric(returns, confidence=0.95):
    mu, sigma = returns.mean(), returns.std()
    z = stats.norm.ppf(1 - confidence)
    return -(mu + z * sigma)

def cvar_parametric(returns, confidence=0.95):
    mu, sigma = returns.mean(), returns.std()
    z = stats.norm.ppf(1 - confidence)
    return -(mu - sigma * stats.norm.pdf(z) / (1 - confidence))
```

**手算验证**：$z_{95\%} = -1.645$，直接用 $\text{VaR} = -(μ - 1.645·σ)$ 计算。

### 蒙特卡洛法

```python
def var_monte_carlo(returns, weights, confidence=0.95, n_sim=10000, seed=42):
    np.random.seed(seed)
    mu = returns.mean().values
    cov = returns.cov().values
    L = np.linalg.cholesky(cov)
    sim = np.random.randn(n_sim, len(weights)) @ L.T + mu
    sim_pf = sim @ weights
    return -np.percentile(sim_pf, 100 * (1 - confidence))
```

**关键**：Cholesky 分解保证生成的随机数具有正确的相关性结构。

---

## Kupiec POF 回测检验

```python
def kupiec_test(returns, var_values, confidence=0.95):
    n = len(returns)
    exceptions = np.sum(returns < -var_values)
    er = exceptions / n                    # 实际例外率
    ee = 1 - confidence                    # 期望例外率
    
    lr_stat = -2 * (np.log((1-ee)**(n-exceptions) * ee**exceptions) 
                  - np.log((1-er)**(n-exceptions) * er**exceptions))
    p_value = 1 - stats.chi2.cdf(lr_stat, df=1)
    
    return {'例外天数': exceptions, 'p值': p_value,
            '结论': '✓ 模型可接受' if p_value > 0.05 else '⚠ 需调整'}
```

- **H₀**：模型准确，例外率 = $1-\alpha$
- **p > 0.05** → 不能拒绝 H₀ → 模型可接受

---

## VaR 的致命缺陷（为什么需要 CVaR）

| 特性 | VaR | CVaR |
|------|-----|------|
| 尾部信息 | ❌ 无（只看门槛） | ✅ 包含整个尾部 |
| 次可加性 | ❌ 不满足 | ✅ 满足 |
| 优化友好 | ❌ 非凸 | ✅ 凸优化 |
| Basel III 推荐 | 旧标准 | ✅ 新标准 |

**经典反例**：两笔独立贷款，每笔违约率 4%。单笔 95% VaR = 0，但两笔合并后 95% VaR > 0。VaR 不满足次可加性，意味着分散化反而"增加"风险——这违反金融常识。

---

## 踩坑记录

1. **正态性假设陷阱**：用参数法前一定做 Jarque-Bera 检验。金融收益率几乎都是肥尾（峰度 > 3），正态 VaR 会系统性低估风险。
2. **历史窗口选择**：窗口太短 → VaR 不稳定；太长 → 对近期风险不敏感。通常 250-500 天。
3. **蒙特卡洛收敛**：至少 10000 次模拟。检查收敛曲线再确定次数。
4. **VaR 不能直接相加**：组合 A 的 VaR + 组合 B 的 VaR ≠ (A+B) 的 VaR。必须重新计算组合收益率。
5. **Kupiec 检验的局限**：只检查例外频率，不检查例外是否聚集（Christoffersen 检验可弥补）。

---

## 相关笔记

- [[12-CAPM贝塔系数]] — Beta 也是风险度量，但衡量的是系统性风险
- 下节 [[20-Markowitz-均值方差优化]] — 用风险-收益框架优化组合权重（序号20）

---

📅 2026-06-14 | 📓 `19_VaR_CVaR.ipynb`

---

## 顺序通关导航

- 上一课：[[18-亚式期权定价]]
- 下一课：[[20-Markowitz-均值方差优化]]
- 对应 Notebook：`19_VaR_CVaR.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
