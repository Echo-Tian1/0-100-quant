# 0-100 Quant 🚀

> 从零基础到独立完成量化分析 —— 一套面向中文学习者的 Python 量化入门教程。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange)]()
[![AKShare](https://img.shields.io/badge/AKShare-1.18%2B-green)]()
[![mplfinance](https://img.shields.io/badge/mplfinance-0.12%2B-lightgrey)]()

---

## 📖 课程路线

从 **0** 到 **100**，九个 Notebook 覆盖量化分析从数据到可视化的完整链路：

### 第一阶段：基础工具

| # | Notebook | 主题 | 核心技能 |
|---|----------|------|----------|
| 01 | Python Quickstart | Python 量化快速入门 | 数据结构 · 条件循环 · 函数 Lambda · 列表推导式 |
| 02 | NumPy Operations | NumPy 数值计算 | 数组运算 · 线性代数 · 随机数 |
| 03 | Random & Monte Carlo | 随机数与蒙特卡洛模拟 | 概率分布 · 随机游走 · 模拟定价 |

### 第二阶段：数据处理

| # | Notebook | 主题 | 核心技能 |
|---|----------|------|----------|
| 04 | Pandas Time Series | Pandas 时间序列分析 | 时序索引 · 滚动窗口 · 重采样 |
| 05 | AKShare MA & Volatility | **实战：沪深300 均线与波动率** | 真实行情获取 · 数据清洗 · 技术指标计算 |
| 06 | Pandas GroupBy / Merge / Pivot | Pandas 高级数据处理 | GroupBy 聚合 · Merge 连接 · Pivot Table · 缺失值处理 |
| 07 | AKShare + SQLite ETL | 数据获取与本地持久化 | 多标的批量下载 · SQLite 存储 · ETL 管道 |

### 第三阶段：可视化与实战

| # | Notebook | 主题 | 核心技能 |
|---|----------|------|----------|
| 08 | Matplotlib 金融可视化 | K线图 · 收益率分布 · 多子图仪表盘 | 中文配置 · 手绘K线 · mplfinance · QQ图 · GridSpec 布局 |
| 09 | K线 + 成交量 + 布林带 + 回撤 | **综合实战仪表盘** | mplfinance 高级面板 · 布林带叠加 · 最大回撤标注 |
| 10 | SciPy 统计分析 | 正态性检验 · t检验 · 线性回归 | JB检验 · KS检验 · 相关系数显著性 |
| 11 | 股票筛选器 | **阶段项目：多条件量化选股** | AKShare · Pandas 筛选 · 行业分析 · 可视化导出 |

### 第四阶段：金融理论与模型

| # | Notebook | 主题 | 核心技能 |
|---|----------|------|----------|
| 12 | CAPM与Beta | **资本资产定价模型实战** | Beta估计 · 滚动窗口 · Alpha分析 · 分组对比 |

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/Echo-Tian1/0-100-quant.git
cd 0-100-quant

# 安装依赖
pip install -r requirements.txt

# 启动 Jupyter
jupyter notebook notebooks/
```

**核心依赖**：`numpy` · `pandas` · `matplotlib` · `mplfinance` · `akshare` · `jupyter`

**辅助库**：`scipy` · `seaborn` · `yfinance` · `vectorbt` · `ipykernel`

---

## 📊 实战预览

- **Notebook 05** — 用 `akshare` 获取沪深 300 真实行情，计算 5/20/60 日均线，波动率分析与滚动窗口
- **Notebook 07** — 批量下载多只 A 股数据，构建本地 SQLite 数据库，实现可复现的 ETL 管道
- **Notebook 08** — 从零手绘 K 线图到 mplfinance 专业出图，收益率分布诊断（histogram / 密度曲线 / Q-Q 图）
- **Notebook 09** — 一站式仪表盘：K线 + 成交量柱状图 + MA 均线 + 布林带 + 最大回撤区间标注

---

## 🎯 学习目标

完成全部课程后，你将掌握：

1. **Python 基础** — 数据结构、循环、函数、列表推导式的量化应用场景
2. **NumPy 计算** — 高效的数值计算与随机模拟
3. **Pandas 全栈** — 时间序列、GroupBy、Merge、Pivot、缺失值处理
4. **数据获取** — AKShare 获取 A 股行情，SQLite 本地持久化
5. **金融可视化** — matplotlib 手绘 + mplfinance 专业 K 线图，多子图仪表盘布局
6. **综合实战** — 均线系统 · 布林带 · 最大回撤 · 完整的量化分析 Pipeline
7. **量化选股** — 多条件股票筛选器 · 行业分析 · PE/PB 估值分析

---

## 🧭 阅读建议

- **有 Python 基础** → 从 02（NumPy）或 04（Pandas 时序）切入
- **纯新手** → 按 01 → 09 顺序学习，每节 1-2 小时
- **只要可视化** → 直接看 08、09，K线图和仪表盘即学即用
- **关注数据管道** → 05 → 07 → 09，走通「获取→存储→分析→出图」全流程

详细学习路线见 [GUIDE.md](GUIDE.md)

---

## 🤝 贡献

欢迎 Issue 和 PR！如果你有想加入的内容（策略回测、因子分析、风险管理等），请开 Issue 讨论。

---

## 📄 License

[MIT](LICENSE) — 自由使用、修改、分享
