# 31-QLib框架入门

> 序号31 | 模块4.1 ML量化 | 第4阶段 进阶专题

---

## 本课核心问题

上两课 [[29-特征工程与数据准备]] 构造了因子 → [[30-机器学习量化入门]] 跑了第一个 ML 预测闭环。

这一课解决的是：**如何用工程化的框架管理整个 ML 量化流水线**。

QLib 是微软开源的 AI 量化平台，核心思想不是「某个模型有多强」，而是：

> 把研究流程拆成可替换的模块，每个模块有明确的输入/输出接口。

---

## QLib 四大模块

```text
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Data    │ → │  Model   │ → │ Strategy │ → │ Executor │
│ 数据准备  │   │ 模型训练  │   │ 策略信号  │   │ 回测评估  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘
     ↓               ↓              ↓              ↓
  因子构造      学习 f(X)→y     信号生成       绩效计算
  标签对齐      样本外预测       仓位管理       归因分析
```

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| **Data** | 数据加载、因子构造、标签计算、时间切分 | 原始行情 | 结构化数据集 (X, y, 时间索引) |
| **Model** | 模型训练与预测 | 特征 X, 标签 y | 预测值 pred |
| **Strategy** | 预测值 → 交易信号 | 预测值, 约束条件 | 信号 (buy/sell/hold) |
| **Executor** | 回测执行, 绩效计算 | 信号, 价格序列 | 净值、Sharpe、回撤 |

### 为什么要模块化

| 好处 | 说明 |
|------|------|
| 解耦 | 换模型不改数据，换策略不改模型 |
| 可复现 | 每步输出有明确接口，方便调试 |
| 可扩展 | 新增模型只需实现 Model 接口 |
| 公平对比 | 同一个 X 和 y 喂给不同模型，绩效在同一回测引擎中可比 |

---

## 1. Data 模块

最核心也最容易出错的模块。三件事：

### 因子构造

```python
class QLibData:
    def build_factors(self):
        df["ret_5d"]   = df["close"].pct_change(5)       # 动量
        df["vol_20d"]  = df["return"].rolling(20).std()   # 波动率
        df["ma_dev"]   = (close - ma_20) / ma_20          # 均线偏离
        df["turnover"] = abs(ret) / vol                   # 换手率代理
```

### 标签构造（防前视偏差）

```python
def build_labels(self, df):
    # ✅ 正确：标签是未来值，用 shift(-horizon)
    df["future_ret_5d"] = df["close"].shift(-5) / df["close"] - 1
    df["target"] = (df["future_ret_5d"] > 0).astype(int)
```

### 时间顺序切分

```python
def prepare(self, train_ratio=0.7):
    df = self.build_factors()
    df = self.build_labels(df)
    df = df.dropna()
    
    split = int(len(df) * train_ratio)
    train = df.iloc[:split]    # 早期数据训练
    test  = df.iloc[split:]    # 后期数据测试
```

---

## 2. Model 模块

核心接口：`fit(X, y)` → `predict(X)`

### 线性模型（传统因子方法）

```python
class QLibModel:
    def fit(self, X, y):
        if self.model_type == "linear":
            X_aug = np.column_stack([np.ones(len(X)), X])
            beta = np.linalg.lstsq(X_aug, y, rcond=None)[0]
            self.model = beta
    
    def predict(self, X):
        X_aug = np.column_stack([np.ones(len(X)), X])
        return X_aug @ self.model
```

### 树模型（ML 因子方法）

```python
def fit(self, X, y):
    if self.model_type == "tree":
        try:
            import lightgbm as lgb
            self.model = lgb.LGBMClassifier(n_estimators=100, max_depth=5)
        except ImportError:
            from sklearn.tree import DecisionTreeClassifier
            self.model = DecisionTreeClassifier(max_depth=5)
        self.model.fit(X, y)
```

---

## 3. Strategy 模块

将连续预测值转化为离散信号：

```python
class QLibStrategy:
    def generate_signals(self, predictions):
        top_thresh = np.quantile(preds, 0.7)      # Top 30% 做多
        bottom_thresh = np.quantile(preds, 0.3)    # Bottom 30% 做空
        
        signals = np.zeros_like(preds)
        signals[preds >= top_thresh] = 1
        signals[preds <= bottom_thresh] = -1
```

---

## 4. Executor 模块

回测 + 绩效指标：

```python
class QLibExecutor:
    def backtest(self):
        signal_diff = np.abs(np.diff(self.signals, prepend=0))
        strategy_returns = self.signals * self.returns - signal_diff * fee_rate
        strategy_nav = np.cumprod(1 + strategy_returns)
        return strategy_nav
    
    def evaluate(self):
        return {
            "Sharpe": annual_return / annual_vol,
            "最大回撤": (nav - peak).min() / peak,
            "胜率": (returns > 0).mean(),
        }
```

---

## 完整流水线

```python
def run_full_pipeline(price_df, model_type, horizon):
    data = QLibData(price_df, horizon)
    ds = data.prepare()
    model = QLibModel(model_type)
    model.fit(ds["X_train"], ds["y_train"])
    preds = model.predict(ds["X_test"])
    signals = QLibStrategy().generate_signals(preds)
    result = QLibExecutor(ds["returns"], signals).evaluate()
    return result
```

---

## 传统因子 vs ML 因子 对比表

| 维度 | 传统因子（线性） | ML 因子（树模型） |
|------|-----------------|-------------------|
| **假设** | 线性关系、同方差 | 不依赖线性假设，自动捕捉非线性 |
| **因子交互** | 需要手动构造交互项 | 自动学习交叉效应 |
| **可解释性** | 高（每个 β 明确） | 中低（特征重要性可用） |
| **过拟合风险** | 低（参数少） | 高（需严格控 max_depth） |
| **样本需求** | 小（几百条够） | 大（通常几千+） |
| **调参难度** | 低（几乎不调） | 高（超参数组合多） |
| **典型场景** | Fama-MacBeth 检验 | 高频预测、另类数据 |

---

## 踩坑记录

### 坑 1：Data 模块是前视偏差重灾区
- ❌ 用全样本均值填充缺失值（间接看了未来）
- ❌ 用全样本做标准化（测试集信息泄露到训练集）
- ✅ 填充和标准化参数只从训练集计算

### 坑 2：QLib 安装成本高
- QLib 依赖 torch、lightgbm 等重型库
- 可以先不装 QLib，而是手写核心组件理解架构
- 本课 notebook 提供了完整的 mini-QLib 实现

### 坑 3：树模型在小样本上极易过拟合
- 500 条数据用 `max_depth=None` 几乎 100% 过拟合
- 必须限制 `max_depth`（本课用 5）和 `n_estimators`

### 坑 4：QLib 的 yaml 配置容易出错
- 真实 QLib 用 yaml 定义流水线，字段名拼写错误不会报错
- 建议先用手写代码理解，再用 yaml 配置

---

## 标签

#ML量化 #QLib #量化框架 #模块化设计 #传统vsML

## 相关笔记

- [[29-特征工程与数据准备]] — 因子构造的前置步骤
- [[30-机器学习量化入门]] — ML 预测闭环
- [[27-绩效归因分析]] — Executor 输出的绩效指标详解
- [[26-回测陷阱专题]] — 前视偏差等陷阱的完整论述

## 对应 Notebook

`31_qlib_intro.ipynb`
