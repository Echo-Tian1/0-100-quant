# 0-100 Quant 🚀

> 从零基础到独立完成量化分析 —— 一套面向中文学习者的 Python 量化入门教程。

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-orange)]()
[![AKShare](https://img.shields.io/badge/AKShare-1.18%2B-green)]()

---

## 📖 课程路线

从 **0** 到 **100**，五节课带你走完量化分析的完整 Pipeline：

| # | Notebook | 主题 | 核心技能 |
|---|----------|------|----------|
| 01 | Python Quickstart | Python 量化快速入闩 | 数据结构 · 条件循环 · 函数 Lambda · 列表推导式 |
| 02 | NumPy Operations | NumPy 数值计算 | 数组运算 · 线性代数 · 随机数 |
| 03 | Random & Monte Carlo | 随机数与蒙特卡洛模拟 | 概率分布 · 模拟定价 |
| 04 | Pandas Time Series | Pandas 时间序列分析 | 时序索引 · 滚动窗口 · 重采样 |
| 05 | AKShare MA & Volatility | **实战：沪深300 均线与波动率** | 真实行情获取 · 数据清洗 · 技术指标计算 |

---

## 🚀 快速开始

\`\`\`bash
# 克隆仓库
git clone https://github.com/Echo-Tian1/0-100-quant.git
cd 0-100-quant

# 安装依赖
pip install -r requirements.txt

# 启动 Jupyter
jupyter notebook notebooks/
\`\`\`

**依赖**：\`pandas\` · \`numpy\` · \`matplotlib\` · \`akshare\` · \`jupyter\`

---

## 📊 实战预览

Notebook 05 用 \`akshare\` 获取沪深 300（\`sh000300\`）的真实行情数据，演示：

- ✅ 获取实时/历史行情
- ✅ 数据清洗与格式化
- ✅ 计算 5/20/60 日均线
- ✅ 波动率分析与滚动窗口
- ✅ 重采样与降频处理

---

## 🎯 学习目标

完成本教程后，你将掌握：

1. **Python 基础** — 数据结构、循环、函数、列表推导式的量化应用场景
2. **NumPy 计算** — 高效的数值计算与随机模拟
3. **Pandas 时序** — 处理金融时间序列的核心技能
4. **AKShare 数据** — 获取 A 股真实行情数据
5. **全流程实战** — 从数据获取到指标计算的完整 Pipeline

---

## 🧭 阅读建议

- **有 Python 基础** → 从 Notebook 02 或 04 开始
- **纯新手** → 按 01 → 05 顺序学习
- **想要实战** → 直接跳到 05，需要时回头查阅前面的内容

详细学习路线见 [GUIDE.md](GUIDE.md)

---

## 🤝 贡献

欢迎 Issue 和 PR！如果你有想加入的内容（策略回测、可视化、风险管理等），请开 Issue 讨论。

---

## 📄 License

[MIT](LICENSE) — 自由使用、修改、分享
