# backtrader 事件驱动回测

#backtrader #事件驱动 #回测框架 #交易成本

## 核心概念

### 事件驱动 vs 向量化回测

| 特性 | 向量化回测 | 事件驱动回测 |
|------|------------|--------------|
| **原理** | 一次性计算所有信号 | 逐根 K 线模拟 |
| **速度** | 快 | 慢 |
| **真实性** | 较低（可能有未来数据） | 高（严格时序） |
| **灵活性** | 低 | 高 |
| **适用场景** | 快速验证想法 | 详细回测、实盘对接 |
| **代表工具** | pandas + numpy | backtrader、vnpy |

### 为什么需要事件驱动？

向量化回测的问题：

1. **未来数据泄露**：容易不小心用到未来数据
2. **撮合逻辑简化**：无法精确模拟订单撮合
3. **交易成本粗糙**：难以精确计算手续费和滑点
4. **无法对接实盘**：回测和实盘逻辑不一致

事件驱动回测的优势：

1. **严格时序**：每根 K 线只用到之前的数据
2. **精确撮合**：模拟真实的订单撮合过程
3. **灵活成本**：可以精确设置手续费和滑点
4. **实盘对接**：回测逻辑可以直接用于实盘

---

## backtrader 架构

```
Cerebro（大脑）
├── DataFeed（数据源）
│   └── PandasData / YahooFinanceData
├── Strategy（策略）
│   └── next() / buy() / sell()
├── Broker（经纪人）
│   └── 手续费 / 滑点 / 资金
├── Analyzer（分析器）
│   └── SharpeRatio / DrawDown / Returns
└── Observer（观察者）
    └── Cash / Value / Trades
```

---

## 订单类型

| 订单类型 | 说明 | 适用场景 |
|----------|------|----------|
| **市价单** | 以当前市场价格立即成交 | 快速入场/出场 |
| **限价单** | 指定价格，达到后成交 | 精确控制成本 |
| **止损单** | 价格达到阈值后触发 | 风险控制 |

### 撮合逻辑

backtrader 的撮合逻辑：

1. **市价单**：以当天的开盘价成交
2. **限价单**：如果当天的价格触及限价，则成交
3. **止损单**：如果当天的价格触及止损价，则触发

**注意**：backtrader 默认使用**当天的开盘价**撮合，这可能与实际交易有差异。

---

## 交易成本

### 手续费设置

backtrader 支持多种手续费模式：

| 模式 | 说明 | 示例 |
|------|------|------|
| **百分比** | 按交易金额的百分比 | 0.1% |
| **固定金额** | 每笔交易固定费用 | 5 元 |
| **混合模式** | 百分比 + 固定金额 | 0.1% + 5 元 |

### 滑点设置

**滑点**是指实际成交价格与预期价格的差异。

- **产生原因**：市场波动、流动性不足
- **设置方式**：固定滑点或百分比滑点
- **影响**：降低策略收益

---

## 完整代码模式

### 创建 Cerebro

```python
import backtrader as bt

# 创建 Cerebro
cerebro = bt.Cerebro()

# 设置初始资金
cerebro.broker.setcash(100000)

# 设置手续费：0.1%
cerebro.broker.setcommission(commission=0.001)

# 设置滑点：0.05%
cerebro.broker.set_slippage_perc(0.0005)
```

### 定义策略

```python
class DualMovingAverage(bt.Strategy):
    """
    双均线策略
    """
    params = (
        ('fast_period', 10),   # 短期均线
        ('slow_period', 30),   # 长期均线
    )
    
    def __init__(self):
        # 计算均线
        self.fast_ma = bt.indicators.SMA(
            self.data.close, period=self.params.fast_period
        )
        self.slow_ma = bt.indicators.SMA(
            self.data.close, period=self.params.slow_period
        )
        
        # 金叉死叉信号
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
    
    def next(self):
        # 当前没有持仓
        if not self.position:
            # 金叉：买入
            if self.crossover > 0:
                self.buy()
        # 当前有持仓
        else:
            # 死叉：卖出
            if self.crossover < 0:
                self.sell()
```

### 运行回测

```python
# 添加数据
data = PandasData(dataname=data_df)
cerebro.adddata(data)

# 添加策略
cerebro.addstrategy(DualMovingAverage)

# 运行回测
results = cerebro.run()
strategy = results[0]

# 获取结果
final_value = cerebro.broker.getvalue()
```

### 限价单示例

```python
class LimitOrderStrategy(bt.Strategy):
    """
    限价单策略示例
    """
    def next(self):
        if not self.position:
            if self.crossover > 0:
                # 限价单：在当前价格下方 2% 买入
                limit_price = self.data.close[0] * (1 - 0.02)
                self.buy(price=limit_price, exectype=bt.Order.Limit)
        else:
            if self.crossover < 0:
                # 限价单：在当前价格上方 2% 卖出
                limit_price = self.data.close[0] * (1 + 0.02)
                self.sell(price=limit_price, exectype=bt.Order.Limit)
```

---

## 踩坑记录

### 1. 数据格式问题
- **问题**：backtrader 无法识别 pandas DataFrame
- **原因**：列名不匹配
- **解决**：确保列名为 'open', 'high', 'low', 'close', 'volume'

### 2. 撮合逻辑差异
- **问题**：回测结果与预期不符
- **原因**：backtrader 用开盘价撮合，向量化用收盘价
- **解决**：理解两种方法的差异，选择合适的框架

### 3. 手续费设置
- **问题**：手续费没有生效
- **原因**：没有正确设置 commission
- **解决**：使用 `cerebro.broker.setcommission(commission=0.001)`

### 4. 交易记录
- **问题**：无法获取交易记录
- **原因**：没有实现 notify_trade 方法
- **解决**：在策略中实现 notify_trade 方法

---

## 对比：向量化 vs 事件驱动

| 方面 | 向量化 | 事件驱动 |
|------|--------|----------|
| **速度** | 快 | 慢 |
| **真实性** | 较低 | 高 |
| **灵活性** | 低 | 高 |
| **学习曲线** | 低 | 高 |
| **适用场景** | 快速验证 | 详细回测、实盘 |

**建议**：
- 快速验证想法：使用向量化
- 详细回测和实盘：使用事件驱动

---

## 相关笔记

- [[22-均线策略与参数优化]] - 均线策略详细讲解
- [[23-动量与均值回归策略]] - 动量和均值回归策略
- [[21-组合优化器]] - 组合优化

---

## 对应 Notebook

`24_backtrader_basics.ipynb`

---

## 顺序通关导航

- 上一课：[[23-动量与均值回归策略]]
- 下一课：[[25-因子构建与检验]]
- 对应 Notebook：`24_backtrader_basics.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
