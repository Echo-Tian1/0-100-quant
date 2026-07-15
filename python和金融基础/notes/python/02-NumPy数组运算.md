# 02 | NumPy 数组运算与向量化

#python #numpy #向量化

## 核心思想：向量化 = 干掉 for 循环

```python
# ❌ 慢（500ms）
returns = []
for i in range(1, len(prices)):
    returns.append((prices[i] - prices[i-1]) / prices[i-1])

# ✅ 快（5ms）—— 100 倍差距
returns = np.diff(prices) / prices[:-1]
```

> NumPy 底层用 C 实现，避免了 Python 解释器的循环开销

---

## ndarray 基础

```python
a = np.array([1, 2, 3, 4, 5])
a.shape       # (5,)
a.dtype       # dtype('int64')
a.ndim        # 1

# 常用创建
np.zeros(10)                    # 全 0
np.ones((3, 4))                 # 全 1
np.arange(0, 10, 2)             # [0, 2, 4, 6, 8]
np.linspace(0, 1, 100)          # 0 到 1 均匀 100 个点
np.random.default_rng(42).normal(0, 1, 1000)  # 正态随机
```

---

## 广播机制（Broadcasting）

NumPy 的「魔法」：形状不同的数组自动对齐运算

### 三条规则（从后往前比维度）
1. 维度相等 → 可以运算
2. 其中一个是 1 → 自动扩展
3. 都不满足 → 报错

```python
# (3,4) 与 (4,) → (4,) 自动变成 (1,4) 再扩展到 (3,4)
data = np.ones((3, 4))
weights = np.array([0.1, 0.2, 0.3, 0.4])
result = data * weights  # ✅ 成功

# (3,4) 与 (3,) → 报错！从后往前比：4≠3 且都不是 1
try:
    data * np.array([1, 2, 3])
except ValueError as e:
    print(f"广播失败: {e}")
```

### 实战：行归一化

```python
data = np.random.randn(5, 3)  # 5 只股票 × 3 个因子
row_means = data.mean(axis=1, keepdims=True)  # (5,1) keepdims 保留维度！
centered = data - row_means  # 广播：(5,3) - (5,1) → (5,3)
```

> ⚠️ 不加 `keepdims` 会变成 `(5,)`，广播就出错了

---

## 布尔索引 & 条件筛选

```python
returns = np.array([0.01, -0.03, 0.02, -0.01, 0.05])

# 布尔数组
mask = returns > 0  # [True, False, True, False, True]
returns[mask]       # [0.01, 0.02, 0.05]

# np.where —— 条件赋值
signal = np.where(returns > 0, '涨', '跌')

# np.clip —— 截断极端值（量化常用）
clipped = np.clip(returns, -0.02, 0.02)  # 超过 ±2% 的截断
```

---

## 聚合与轴操作

```python
data = np.random.randn(100, 5)  # 100 天 × 5 只股票

data.mean()          # 全局均值
data.mean(axis=0)    # 每只股票的均值（沿行压缩 → 1×5）
data.mean(axis=1)    # 每天的均值（沿列压缩 → 100×1）

# keepdims 保持维度，方便后续广播
normalized = (data - data.mean(axis=0, keepdims=True)) / data.std(axis=0, keepdims=True)
```

| axis | 含义 | 结果形状 |
|------|------|---------|
| `axis=0` | 沿行方向压缩（跨天） | `(5,)` |
| `axis=1` | 沿列方向压缩（跨股票） | `(100,)` |

---

## 量化常用函数速查

```python
# 排序
np.sort(returns)                # 升序
np.argsort(returns)             # 返回索引（排名）

# 集合
np.unique(sectors)              # 去重
np.intersect1d(a, b)            # 交集

# 数学
np.cumsum(returns)              # 累计收益
np.cumprod(1 + returns)         # 累计净值
np.percentile(returns, 95)      # 95% 分位数（VaR）
np.corrcoef(a, b)               # 相关系数矩阵

# 拼接
np.concatenate([a, b])          # 首尾相接
np.vstack([a, b])               # 垂直拼接
np.hstack([a, b])               # 水平拼接
```

---

## 性能对比

```python
import time
n = 1_000_000
prices = np.random.randn(n).cumsum() + 100

# Python for
start = time.time()
r1 = [(prices[i]-prices[i-1])/prices[i-1] for i in range(1, n)]
print(f"Python: {time.time()-start:.3f}s")

# NumPy
start = time.time()
r2 = np.diff(prices) / prices[:-1]
print(f"NumPy:  {time.time()-start:.3f}s")

# Python: ~0.5s  NumPy: ~0.005s  → 100x
```

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| `a = b` 不复制 | `a` 和 `b` 指向同一数组，改 `a` 也改了 `b`。用 `a = b.copy()` |
| 整数除法 | `3 / 2 = 1.5`（Python3），但 `np.array([3]) / np.array([2])` 看 dtype |
| 浮点精度 | `np.float32` 精度不够，量化用 `float64` |
| 空数组运算 | `np.array([]).mean()` → `nan`，先检查长度 |

---

📁 对应 Notebook: `02_numpy_operations.ipynb`
⬅️ [[01-Python核心语法]] ➡️ [[03-随机数与蒙特卡洛]]

---

## 顺序通关导航

- 上一课：[[01-Python核心语法]]
- 下一课：[[03-随机数与蒙特卡洛]]
- 对应 Notebook：`02_numpy_operations.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
