# BS公式与Greeks

#期权定价 #Greeks #Black-Scholes #风险管理

## 核心概念

### Black-Scholes 公式

欧式看涨/看跌期权的解析定价公式：

```
Call: C = S·N(d1) - K·e^(-rT)·N(d2)
Put:  P = K·e^(-rT)·N(-d2) - S·N(-d1)

其中：
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T
```

**参数说明：**
- S：标的资产当前价格
- K：行权价
- r：无风险利率（年化）
- σ：波动率（年化）
- T：到期时间（年）
- N(·)：标准正态分布 CDF

### BS 公式的假设

| 假设 | 现实中的违反 |
|------|--------------|
| 标的价格服从几何布朗运动 | 存在跳跃、波动率聚集 |
| 无风险利率恒定 | 利率随时间变化 |
| 无摩擦市场 | 有交易成本、买卖价差 |
| 不支付股息 | 很多股票有股息 |
| 欧式期权 | 美式期权更常见 |
| 波动率恒定 | 波动率微笑/偏斜 |

### Put-Call Parity（看涨看跌平价）

```
C + K·e^(-rT) = P + S
```

**这个关系不依赖任何模型假设**，只要无套利即可成立。

含义：看涨期权 + 现金 = 看跌期权 + 股票

---

## Greeks：期权风险敏感度

### Greeks 速查表

| Greek     | 符号  | 定义      | Call | Put  | 金融意义         |
| --------- | --- | ------- | ---- | ---- | ------------ |
| **Delta** | Δ   | ∂C/∂S   | 0~1  | -1~0 | 价格敏感度 / 行权概率 |
| **Gamma** | Γ   | ∂²C/∂S² | +    | +    | Delta 的变化率   |
| **Theta** | Θ   | ∂C/∂t   | -    | -    | 时间衰减（每日）     |
| **Vega**  | ν   | ∂C/∂σ   | +    | +    | 波动率敏感度       |
| **Rho**   | ρ   | ∂C/∂r   | +    | -    | 利率敏感度        |

### Greeks 的金融含义

#### Delta (Δ)
- Call Delta = 0.6：标的上涨 1 元，期权上涨 0.6 元
- 也可以理解为风险中性世界中到期为实值的概率
- **Delta 对冲**：卖 Call 需买入 Δ 份标的

#### Gamma (Γ)
- Delta 对标的价格的敏感度
- **平值期权 Gamma 最大**
- Gamma 大 → Delta 变化快 → 需频繁调仓

#### Theta (Θ)
- 通常为负值（时间流逝减少期权价值）
- **平值期权 Theta 最大**（时间价值衰减最快）
- 买期权 = 做多 Gamma + 做空 Theta

#### Vega (ν)
- 波动率上升 1%，期权价格上升 ν 个点
- **平值期权 Vega 最大**
- 市场恐慌 → 波动率上升 → 期权涨价

#### Rho (ρ)
- 利率上升 → Call 更值钱（行权支出现值下降）
- 通常 Rho 影响较小

### Greeks 的形状特征

| Greek | 形状 | 平值处 | 原因 |
|-------|------|--------|------|
| Delta | S 形 | ≈0.5 (Call) | 从 0（虚值）到 1（实值） |
| Gamma | 钟形 | 最大 | 平值 Delta 变化最敏感 |
| Theta | 倒钟形 | 最负 | 平值时间价值最大 |
| Vega | 钟形 | 最大 | 平值对波动率最敏感 |
| Rho | 单调递增 | 中等 | 标的价格越高影响越大 |

### 时间对 Greeks 的影响

| 到期时间 | Delta 曲线 | Gamma | Theta |
|----------|-----------|-------|-------|
| 短（临近到期） | 陡峭 | 平值处极大 | 平值处极负 |
| 长 | 平缓 | 较小 | 较小 |

**这就是为什么「末日轮」期权波动特别大（Gamma 大）。**

---

## 完整代码模式

### 手写 BS 公式

```python
import numpy as np
from scipy.stats import norm

def bs_d1(S, K, r, sigma, T):
    """计算 d1"""
    return (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))

def bs_d2(S, K, r, sigma, T):
    """计算 d2"""
    return bs_d1(S, K, r, sigma, T) - sigma * np.sqrt(T)

def bs_call(S, K, r, sigma, T):
    """计算欧式看涨期权价格"""
    d1 = bs_d1(S, K, r, sigma, T)
    d2 = bs_d2(S, K, r, sigma, T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def bs_put(S, K, r, sigma, T):
    """计算欧式看跌期权价格"""
    d1 = bs_d1(S, K, r, sigma, T)
    d2 = bs_d2(S, K, r, sigma, T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
```

### 计算 Greeks

```python
def bs_greeks(S, K, r, sigma, T, option_type='call'):
    """计算所有 Greeks"""
    d1 = bs_d1(S, K, r, sigma, T)
    d2 = bs_d2(S, K, r, sigma, T)
    nd1 = norm.pdf(d1)
    
    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (-S * nd1 * sigma / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:  # put
        delta = norm.cdf(d1) - 1
        theta = (-S * nd1 * sigma / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
    
    gamma = nd1 / (S * sigma * np.sqrt(T))
    vega = S * nd1 * np.sqrt(T) / 100
    
    return {
        'Delta': delta, 'Gamma': gamma, 'Theta': theta,
        'Vega': vega, 'Rho': rho
    }
```

### 绘制 Greeks 曲线

```python
import matplotlib.pyplot as plt

S_range = np.linspace(70, 130, 200)
K, r, sigma, T = 100, 0.05, 0.2, 0.5

greeks_list = [bs_greeks(S, K, r, sigma, T, 'call') for S in S_range]

fig, axes = plt.subplots(2, 3, figsize=(14, 9))
for ax, greek in zip(axes.flat, ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']):
    values = [g[greek] for g in greeks_list]
    ax.plot(S_range, values, linewidth=2)
    ax.axvline(x=K, color='gray', linestyle=':', alpha=0.5)
    ax.set_title(greek)
    ax.grid(True, alpha=0.3)
```

### 数值方法验证

```python
def numerical_greeks(S, K, r, sigma, T, option_type='call'):
    """用有限差分法计算 Greeks"""
    price_func = bs_call if option_type == 'call' else bs_put
    dS, dsigma, dr, dT = 0.01, 0.0001, 0.0001, 1/365
    
    delta = (price_func(S+dS, K, r, sigma, T) - price_func(S-dS, K, r, sigma, T)) / (2 * dS)
    gamma = (price_func(S+dS, K, r, sigma, T) - 2*price_func(S, K, r, sigma, T) + price_func(S-dS, K, r, sigma, T)) / (dS**2)
    theta = (price_func(S, K, r, sigma, T-dT) - price_func(S, K, r, sigma, T)) / dT / 365
    vega = (price_func(S, K, r, sigma+dsigma, T) - price_func(S, K, r, sigma-dsigma, T)) / (2 * dsigma) / 100
    rho = (price_func(S, K, r+dr, sigma, T) - price_func(S, K, r-dr, sigma, T)) / (2 * dr) / 100
    
    return {'Delta': delta, 'Gamma': gamma, 'Theta': theta, 'Vega': vega, 'Rho': rho}
```

---

## 常见策略 Greeks 特征

| 策略 | Delta | Gamma | Theta | Vega | 适用场景 |
|------|-------|-------|-------|------|----------|
| 买入 Call | + | + | - | + | 看涨 |
| 买入 Put | - | + | - | + | 看跌 |
| 卖出 Call | - | - | + | - | 看不涨 |
| 卖出 Put | + | - | + | - | 看不跌 |
| 买入跨式 | 0 | + | - | + | 预期大幅波动 |
| 卖出跨式 | 0 | - | + | - | 预期横盘整理 |

**核心规律：Gamma 和 Theta 是对价关系**
- 做多 Gamma = 做空 Theta（买期权）
- 做空 Gamma = 做多 Theta（卖期权）

---

## 踩坑记录

### 1. Theta 的单位问题
- **问题**：Theta 通常表示「每日」时间价值衰减，但公式计算的是「每年」
- **解决**：计算结果要除以 365

### 2. Vega 和 Rho 的单位问题
- **问题**：Vega 通常表示「波动率变化 1%」的影响，Rho 表示「利率变化 1%」的影响
- **解决**：计算结果要除以 100

### 3. Put-Call Parity 验证失败
- **问题**：自己实现时验证 Put-Call Parity 不成立
- **原因**：通常是 Put 公式写错了（符号错误）
- **解决**：检查 `N(-d2)` 和 `N(-d1)` 的符号

### 4. Greeks 数值不稳定
- **问题**：Gamma 在深度实值/虚值时数值很小但不稳定
- **原因**：正态分布 PDF 在尾部接近 0
- **解决**：这是正常现象，实际交易中这些区域的 Greeks 本身就不重要

### 5. 美式期权不能用 BS 公式
- **问题**：用 BS 公式给美式期权定价
- **原因**：BS 公式假设欧式期权（只能到期行权）
- **解决**：美式期权需要使用二叉树、有限差分等方法

---

## 对比：不同定价方法

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **BS 公式** | 解析解、计算快 | 假设严格 | 欧式期权 |
| **二叉树** | 直观、可处理美式 | 计算慢 | 美式期权 |
| **蒙特卡洛** | 灵活、可处理路径依赖 | 慢、有噪声 | 奇异期权 |
| **有限差分** | 稳定、可处理边界 | 实现复杂 | 连续定价 |

---

## 相关笔记

- [[12-CAPM贝塔系数]] - Beta 与期权 Delta 的关系
- [[14-Fama-French五因子模型]] - 因子模型与期权定价的区别
- [[17-蒙特卡洛期权定价]] - 下一步：用 MC 定价期权

---

## 对应 Notebook

`16_bs_greeks.ipynb`

---

## 顺序通关导航

- 上一课：[[15-因子模型总结]]
- 下一课：[[17-蒙特卡洛期权定价]]
- 对应 Notebook：`16_bs_greeks.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
