# 01 | Python 核心语法速通

#python #基础

## 核心数据结构

```python
# 列表 —— 有序、可变、可重复
prices = [10.5, 11.2, 10.8, 11.5]
prices.append(12.0)
prices[-1]        # 最后一个元素
prices[1:3]       # 切片 [11.2, 10.8]

# 元组 —— 有序、不可变（函数返回多值）
point = (100, 200)
x, y = point      # 解包

# 集合 —— 无序、不重复（去重）
sectors = {"银行", "科技", "消费", "银行"}  # → {"银行", "科技", "消费"}

# 字典 —— 键值对（量化无处不在）
stock = {"name": "茅台", "price": 1680.5, "pe": 35.2}
stock.get("pe", "无数据")  # 安全取值
```

---

## 列表推导式 —— Python 的加速器

```python
# 基础：变换
returns = [(b - a) / a for a, b in zip(prices[:-1], prices[1:])]

# 带条件：筛选 + 变换
big_moves = [r for r in returns if abs(r) > 0.03]

# 嵌套：笛卡尔积
pairs = [(s, d) for s in stocks for d in dates]

# 字典推导式
price_dict = {name: price for name, price in zip(names, prices)}
```

> 列表推导式是 [[02-NumPy数组运算]] 向量化思想的铺垫

---

## 函数与 Lambda

```python
# 默认参数
def calc_return(start, end, cost=0.001):
    """计算扣费后的收益率"""
    return (end - start) / start - cost

# *args 和 **kwargs
def portfolio(*stocks, **kwargs):
    print(f"持仓: {stocks}")
    print(f"参数: {kwargs}")

portfolio("茅台", "宁德", weight=0.5)

# Lambda —— 一次性小函数
stocks.sort(key=lambda s: s["pe"])           # 排序
list(map(lambda p: p * 1.1, prices))         # 批量变换
list(filter(lambda s: s["pe"] < 20, stocks)) # 筛选
```

---

## 文件读写

```python
# 写入
with open("data.csv", "w", encoding="utf-8") as f:
    f.write("date,price\n2026-01-01,100\n")

# 读取
with open("data.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

> 始终用 `with open`，自动关闭文件，即使中途报错也不会泄漏资源

---

## 异常处理

```python
# 捕获特定异常
try:
    result = a / b
except ZeroDivisionError:
    return float('nan')
except TypeError as e:
    print(f"类型错误: {e}")
    return None
except Exception as e:
    print(f"未知错误: {e}")
    raise  # 重新抛出

# 实用：安全读取
def safe_read(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
```

---

## 实用内置函数

```python
# enumerate —— 同时拿索引和值
for i, name in enumerate(["茅台", "宁德"], start=1):
    print(f"#{i}: {name}")

# zip —— 并行遍历
for date, price in zip(dates, prices):
    print(f"{date}: {price}")

# sorted —— 排序（不改变原列表）
sorted(stocks, key=lambda s: s["pe"], reverse=True)

# any / all
any(r > 0.05 for r in returns)   # 有没有大涨的
all(r > 0 for r in returns)      # 是不是全涨

# min / max 的 key 参数
max(stocks, key=lambda s: s["pe"])  # PE 最高的
```

---

## 字符串格式化

```python
name, price, pct = "茅台", 1680.5, 0.0625

# f-string（推荐）
print(f"{name}: ¥{price:,.2f}, 涨幅 {pct:+.2%}")
# → 茅台: ¥1,680.50, 涨幅 +6.25%

# 格式化符号
# :,.2f  千分位 + 2位小数
# :+.2%  百分比 + 正负号
# :>10   右对齐占10字符
# :<10   左对齐
```

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| `list` 是可变对象 | `a = b` 后改 `a` 也改了 `b`，用 `a = b.copy()` |
| `dict.get()` vs `dict[]` | `.get()` 找不到返回 `None`，`[]` 会报 `KeyError` |
| `range` 不包含右端 | `range(1, 5)` → `[1, 2, 3, 4]` |
| 浮点比较 | `0.1 + 0.2 != 0.3`，用 `abs(a - b) < 1e-9` |
| 可变默认参数 | `def f(a=[])` 有坑，用 `def f(a=None)` |

---

📁 对应 Notebook: `01_python_quickstart.ipynb`
⬅️ - ➡️ [[02-NumPy数组运算]]

---

## 顺序通关导航

- 上一课：无
- 下一课：[[02-NumPy数组运算]]
- 对应 Notebook：`01_python_quickstart.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
