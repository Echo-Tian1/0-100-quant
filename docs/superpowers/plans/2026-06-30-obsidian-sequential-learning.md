# Obsidian Sequential Learning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing Obsidian notes for `0-100-quant` into a smooth 1-33 lesson sequence with reliable links, a clear route, and review checkpoints.

**Architecture:** Use the existing Obsidian vault under `notebooks/notes` as the source of truth. Generate deterministic navigation files from a fixed lesson map, then apply targeted link fixes and append lightweight navigation blocks to lesson notes without rewriting their bodies.

**Tech Stack:** Markdown, Obsidian wikilinks, Python standard library for validation, Git for change review.

---

## File Structure

- Create: `notebooks/notes/01-顺序通关路线.md`
  - Main study route grouped by stages, with one lesson row per Notebook.
- Create: `notebooks/notes/02-复习清单.md`
  - Checklist for explaining, reproducing, and modifying each lesson.
- Modify: `notebooks/notes/00-主页.md`
  - Replace outdated route links with a complete Chinese-file-name based 1-33 entry page.
- Modify: `notebooks/notes/**/*.md`
  - Fix known broken wikilinks and append a standard navigation block when missing.
- Modify: `README.md`
  - Update the outdated statement that the repository contains 30 notebooks.
- Create: `scripts/check_obsidian_links.py`
  - Validate wikilinks against Markdown files and report broken links, ignoring code fences and inline code.

## Lesson Map

Use this fixed map for all generated navigation:

| No. | Note | Notebook | Stage |
|---:|---|---|---|
| 01 | `01-Python核心语法` | `01_python_quickstart.ipynb` | Python 基础 |
| 02 | `02-NumPy数组运算` | `02_numpy_operations.ipynb` | Python 基础 |
| 03 | `03-随机数与蒙特卡洛` | `03_random_monte_carlo.ipynb` | Python 基础 |
| 04 | `04-Pandas时序处理` | `04_pandas_timeseries.ipynb` | 数据处理 |
| 05 | `05-AKShare均线波动率` | `05_akshare_ma_volatility.ipynb` | 数据处理 |
| 06 | `06-Pandas数据清洗` | `06_pandas_groupby_merge_pivot_missing.ipynb` | 数据处理 |
| 07 | `07-AKShare与SQLite` | `07_akshare_sqlite_etl.ipynb` | 数据处理 |
| 08 | `08-Matplotlib金融可视化` | `08_matplotlib_finance.ipynb` | 可视化与统计实战 |
| 09 | `09-K线布林带最大回撤` | `09_kline_volume_ma_bollinger_drawdown.ipynb` | 可视化与统计实战 |
| 10 | `10-SciPy统计分析` | `10_scipy_statistics.ipynb` | 可视化与统计实战 |
| 11 | `11-股票筛选器` | `11_stock_screener.ipynb` | 可视化与统计实战 |
| 12 | `12-CAPM贝塔系数` | `12_capm_beta.ipynb` | 金融理论与因子 |
| 13 | `13-Fama-French三因子模型` | `13_fama_french.ipynb` | 金融理论与因子 |
| 14 | `14-Fama-French五因子模型` | `14_fama_french_five_factor.ipynb` | 金融理论与因子 |
| 15 | `15-因子模型总结` | `15_factor_model_summary.ipynb` | 金融理论与因子 |
| 16 | `16-BS公式与Greeks` | `16_bs_greeks.ipynb` | 期权定价 |
| 17 | `17-蒙特卡洛期权定价` | `17_monte_carlo_option_pricing.ipynb` | 期权定价 |
| 18 | `18-亚式期权定价` | `18_asian_option.ipynb` | 期权定价 |
| 19 | `19-VaR-CVaR` | `19_VaR_CVaR.ipynb` | 风控与组合优化 |
| 20 | `20-Markowitz-均值方差优化` | `20_Markowitz_Portfolio_Optimization.ipynb` | 风控与组合优化 |
| 21 | `21-组合优化器` | `21_portfolio_optimizer.ipynb` | 风控与组合优化 |
| 22 | `22-均线策略与参数优化` | `22_moving_average_strategy.ipynb` | 策略开发与回测 |
| 23 | `23-动量与均值回归策略` | `23_momentum_mean_reversion.ipynb` | 策略开发与回测 |
| 24 | `24-backtrader事件驱动回测` | `24_backtrader_basics.ipynb` | 策略开发与回测 |
| 25 | `25-因子构建与检验` | `25_factor_construction.ipynb` | 策略开发与回测 |
| 26 | `26-回测陷阱专题` | `26_backtesting_pitfalls.ipynb` | 策略开发与回测 |
| 27 | `27-绩效归因分析` | `27_performance_attribution.ipynb` | 策略开发与回测 |
| 28 | `28-策略研究报告` | `28_strategy_research_report.ipynb` | 策略开发与回测 |
| 29 | `29-特征工程与数据准备` | `29_feature_engineering.ipynb` | ML 量化与系统化 |
| 30 | `30-机器学习量化入门` | `30_ml_quant_intro.ipynb` | ML 量化与系统化 |
| 31 | `31-QLib框架入门` | `31_qlib_intro.ipynb` | ML 量化与系统化 |
| 32 | `32-手写回测引擎` | `32_handwrite_backtest_engine.ipynb` | ML 量化与系统化 |
| 33 | `33-风控系统设计` | `33_risk_management.ipynb` | ML 量化与系统化 |

### Task 1: Add Obsidian Link Checker

**Files:**
- Create: `scripts/check_obsidian_links.py`

- [ ] **Step 1: Write the link checker script**

Create `scripts/check_obsidian_links.py` with:

```python
from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "notebooks"
NOTES_ROOT = VAULT_ROOT / "notes"


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def normalize_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    if target.endswith(".ipynb"):
        target = target[:-6]
    if "/" in target:
        target = Path(target).stem
    return target


def markdown_stems() -> set[str]:
    return {path.stem for path in NOTES_ROOT.rglob("*.md")} | {
        path.stem for path in VAULT_ROOT.glob("*.md")
    }


def broken_links() -> list[tuple[Path, str, str]]:
    existing = markdown_stems()
    broken: list[tuple[Path, str, str]] = []
    for path in sorted(list(NOTES_ROOT.rglob("*.md")) + list(VAULT_ROOT.glob("*.md"))):
        text = strip_code(path.read_text(encoding="utf-8"))
        for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
            raw = match.group(1)
            target = normalize_target(raw)
            if target and target not in existing:
                broken.append((path, target, raw))
    return broken


def main() -> int:
    broken = broken_links()
    if not broken:
        print("No broken Obsidian wikilinks found.")
        return 0

    print(f"Broken Obsidian wikilinks: {len(broken)}")
    for path, target, raw in broken:
        rel = path.relative_to(VAULT_ROOT)
        print(f"{rel}: [[{raw}]] -> missing target `{target}`")
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run checker and confirm baseline failure**

Run: `python3 scripts/check_obsidian_links.py`

Expected: exit code `1` with broken links including old names such as `python-quickstart`, `capm-beta`, and `portfolio-optimization`.

### Task 2: Generate Main Route Files

**Files:**
- Modify: `notebooks/notes/00-主页.md`
- Create: `notebooks/notes/01-顺序通关路线.md`
- Create: `notebooks/notes/02-复习清单.md`

- [ ] **Step 1: Replace `00-主页.md` with the sequential entry page**

Use the lesson map to write:

```markdown
# 量化学习笔记主页

## 今日入口

- 顺序学习：[[01-顺序通关路线]]
- 复习回看：[[02-复习清单]]
- 当前范围：01-33，共 33 个 Notebook

## 1-33 顺序路线

| 序号 | 阶段 | 主题 | Notebook | 状态 |
|---:|---|---|---|---|
| 01 | Python 基础 | [[01-Python核心语法]] | `01_python_quickstart.ipynb` | 已整理 |
| 02 | Python 基础 | [[02-NumPy数组运算]] | `02_numpy_operations.ipynb` | 已整理 |
| 03 | Python 基础 | [[03-随机数与蒙特卡洛]] | `03_random_monte_carlo.ipynb` | 已整理 |
| 04 | 数据处理 | [[04-Pandas时序处理]] | `04_pandas_timeseries.ipynb` | 已整理 |
| 05 | 数据处理 | [[05-AKShare均线波动率]] | `05_akshare_ma_volatility.ipynb` | 已整理 |
| 06 | 数据处理 | [[06-Pandas数据清洗]] | `06_pandas_groupby_merge_pivot_missing.ipynb` | 已整理 |
| 07 | 数据处理 | [[07-AKShare与SQLite]] | `07_akshare_sqlite_etl.ipynb` | 已整理 |
| 08 | 可视化与统计实战 | [[08-Matplotlib金融可视化]] | `08_matplotlib_finance.ipynb` | 已整理 |
| 09 | 可视化与统计实战 | [[09-K线布林带最大回撤]] | `09_kline_volume_ma_bollinger_drawdown.ipynb` | 已整理 |
| 10 | 可视化与统计实战 | [[10-SciPy统计分析]] | `10_scipy_statistics.ipynb` | 已整理 |
| 11 | 可视化与统计实战 | [[11-股票筛选器]] | `11_stock_screener.ipynb` | 已整理 |
| 12 | 金融理论与因子 | [[12-CAPM贝塔系数]] | `12_capm_beta.ipynb` | 已整理 |
| 13 | 金融理论与因子 | [[13-Fama-French三因子模型]] | `13_fama_french.ipynb` | 已整理 |
| 14 | 金融理论与因子 | [[14-Fama-French五因子模型]] | `14_fama_french_five_factor.ipynb` | 已整理 |
| 15 | 金融理论与因子 | [[15-因子模型总结]] | `15_factor_model_summary.ipynb` | 已整理 |
| 16 | 期权定价 | [[16-BS公式与Greeks]] | `16_bs_greeks.ipynb` | 已整理 |
| 17 | 期权定价 | [[17-蒙特卡洛期权定价]] | `17_monte_carlo_option_pricing.ipynb` | 已整理 |
| 18 | 期权定价 | [[18-亚式期权定价]] | `18_asian_option.ipynb` | 已整理 |
| 19 | 风控与组合优化 | [[19-VaR-CVaR]] | `19_VaR_CVaR.ipynb` | 已整理 |
| 20 | 风控与组合优化 | [[20-Markowitz-均值方差优化]] | `20_Markowitz_Portfolio_Optimization.ipynb` | 已整理 |
| 21 | 风控与组合优化 | [[21-组合优化器]] | `21_portfolio_optimizer.ipynb` | 已整理 |
| 22 | 策略开发与回测 | [[22-均线策略与参数优化]] | `22_moving_average_strategy.ipynb` | 已整理 |
| 23 | 策略开发与回测 | [[23-动量与均值回归策略]] | `23_momentum_mean_reversion.ipynb` | 已整理 |
| 24 | 策略开发与回测 | [[24-backtrader事件驱动回测]] | `24_backtrader_basics.ipynb` | 已整理 |
| 25 | 策略开发与回测 | [[25-因子构建与检验]] | `25_factor_construction.ipynb` | 已整理 |
| 26 | 策略开发与回测 | [[26-回测陷阱专题]] | `26_backtesting_pitfalls.ipynb` | 已整理 |
| 27 | 策略开发与回测 | [[27-绩效归因分析]] | `27_performance_attribution.ipynb` | 已整理 |
| 28 | 策略开发与回测 | [[28-策略研究报告]] | `28_strategy_research_report.ipynb` | 已整理 |
| 29 | ML 量化与系统化 | [[29-特征工程与数据准备]] | `29_feature_engineering.ipynb` | 已整理 |
| 30 | ML 量化与系统化 | [[30-机器学习量化入门]] | `30_ml_quant_intro.ipynb` | 已整理 |
| 31 | ML 量化与系统化 | [[31-QLib框架入门]] | `31_qlib_intro.ipynb` | 已整理 |
| 32 | ML 量化与系统化 | [[32-手写回测引擎]] | `32_handwrite_backtest_engine.ipynb` | 已整理 |
| 33 | ML 量化与系统化 | [[33-风控系统设计]] | `33_risk_management.ipynb` | 已整理 |

## 学习节奏

1. 先看本课 Obsidian 笔记，抓住概念和代码结构。
2. 再运行对应 Notebook，确认每段代码能复现。
3. 最后打开 [[02-复习清单]]，完成“能解释、能复现、能改造”三个检查。

## 阶段目标

- Python 基础：能写出量化代码所需的 Python / NumPy / 随机模拟基础。
- 数据处理：能获取、清洗、保存 A 股行情数据。
- 可视化与统计实战：能做指标图、统计检验和简单选股。
- 金融理论与因子：能解释 CAPM、Fama-French 和因子模型。
- 期权定价：能理解 BS、Greeks、蒙特卡洛和路径依赖期权。
- 风控与组合优化：能计算风险指标并做组合权重优化。
- 策略开发与回测：能完成策略构建、回测、归因和研究报告。
- ML 量化与系统化：能把特征、模型、框架、回测和风控连成闭环。

## 最近更新

- 2026-06-30：重建顺序通关入口，修复旧链接并补充复习路径。
```

- [ ] **Step 2: Create `01-顺序通关路线.md`**

Include stage sections, lesson rows, and a fixed action sequence for each stage:

```markdown
# 01-顺序通关路线

## 使用方法

每一课按同一个节奏走：

1. 读笔记：先看概念、表格和踩坑。
2. 跑代码：打开对应 Notebook，从上到下运行。
3. 做复盘：回到 [[02-复习清单]] 勾选本课检查点。

## 阶段 1：Python 基础（01-03）

目标：补齐后续量化代码需要的 Python、数组和随机模拟基础。

| 序号 | 主题 | 本课产出 |
|---:|---|---|
| 01 | [[01-Python核心语法]] | 能写函数、推导式、异常处理和文件读写 |
| 02 | [[02-NumPy数组运算]] | 能用数组表达批量计算和线性代数操作 |
| 03 | [[03-随机数与蒙特卡洛]] | 能模拟随机过程并理解蒙特卡洛估计 |
```

- [ ] **Step 3: Create `02-复习清单.md`**

Use one checklist row per lesson:

```markdown
# 02-复习清单

## 使用方法

每课结束后只问三件事：

- 我能不能用自己的话解释它？
- 我能不能重新运行对应 Notebook？
- 我能不能改一个参数或场景，并说出结果为什么变化？

## 01-33 检查表

| 序号 | 主题 | 能解释 | 能复现 | 能改造 |
|---:|---|---|---|---|
| 01 | [[01-Python核心语法]] | [ ] | [ ] | [ ] |
| 02 | [[02-NumPy数组运算]] | [ ] | [ ] | [ ] |
| 03 | [[03-随机数与蒙特卡洛]] | [ ] | [ ] | [ ] |
| 04 | [[04-Pandas时序处理]] | [ ] | [ ] | [ ] |
| 05 | [[05-AKShare均线波动率]] | [ ] | [ ] | [ ] |
| 06 | [[06-Pandas数据清洗]] | [ ] | [ ] | [ ] |
| 07 | [[07-AKShare与SQLite]] | [ ] | [ ] | [ ] |
| 08 | [[08-Matplotlib金融可视化]] | [ ] | [ ] | [ ] |
| 09 | [[09-K线布林带最大回撤]] | [ ] | [ ] | [ ] |
| 10 | [[10-SciPy统计分析]] | [ ] | [ ] | [ ] |
| 11 | [[11-股票筛选器]] | [ ] | [ ] | [ ] |
| 12 | [[12-CAPM贝塔系数]] | [ ] | [ ] | [ ] |
| 13 | [[13-Fama-French三因子模型]] | [ ] | [ ] | [ ] |
| 14 | [[14-Fama-French五因子模型]] | [ ] | [ ] | [ ] |
| 15 | [[15-因子模型总结]] | [ ] | [ ] | [ ] |
| 16 | [[16-BS公式与Greeks]] | [ ] | [ ] | [ ] |
| 17 | [[17-蒙特卡洛期权定价]] | [ ] | [ ] | [ ] |
| 18 | [[18-亚式期权定价]] | [ ] | [ ] | [ ] |
| 19 | [[19-VaR-CVaR]] | [ ] | [ ] | [ ] |
| 20 | [[20-Markowitz-均值方差优化]] | [ ] | [ ] | [ ] |
| 21 | [[21-组合优化器]] | [ ] | [ ] | [ ] |
| 22 | [[22-均线策略与参数优化]] | [ ] | [ ] | [ ] |
| 23 | [[23-动量与均值回归策略]] | [ ] | [ ] | [ ] |
| 24 | [[24-backtrader事件驱动回测]] | [ ] | [ ] | [ ] |
| 25 | [[25-因子构建与检验]] | [ ] | [ ] | [ ] |
| 26 | [[26-回测陷阱专题]] | [ ] | [ ] | [ ] |
| 27 | [[27-绩效归因分析]] | [ ] | [ ] | [ ] |
| 28 | [[28-策略研究报告]] | [ ] | [ ] | [ ] |
| 29 | [[29-特征工程与数据准备]] | [ ] | [ ] | [ ] |
| 30 | [[30-机器学习量化入门]] | [ ] | [ ] | [ ] |
| 31 | [[31-QLib框架入门]] | [ ] | [ ] | [ ] |
| 32 | [[32-手写回测引擎]] | [ ] | [ ] | [ ] |
| 33 | [[33-风控系统设计]] | [ ] | [ ] | [ ] |
```

### Task 3: Fix Broken Route Links

**Files:**
- Modify: `notebooks/notes/**/*.md`
- Modify: `notebooks/factor-investing.md`

- [ ] **Step 1: Apply known link replacements**

Replace only wikilink targets, preserving aliases when present:

```text
[[python-quickstart]] -> [[01-Python核心语法]]
[[numpy-operations]] -> [[02-NumPy数组运算]]
[[random-monte-carlo]] -> [[03-随机数与蒙特卡洛]]
[[pandas-timeseries]] -> [[04-Pandas时序处理]]
[[akshare-ma-volatility]] -> [[05-AKShare均线波动率]]
[[pandas-groupby-merge]] -> [[06-Pandas数据清洗]]
[[akshare-sqlite-etl]] -> [[07-AKShare与SQLite]]
[[matplotlib-finance]] -> [[08-Matplotlib金融可视化]]
[[kline-volume-ma-bollinger]] -> [[09-K线布林带最大回撤]]
[[scipy-statistics]] -> [[10-SciPy统计分析]]
[[stock-screener]] -> [[11-股票筛选器]]
[[capm-beta]] -> [[12-CAPM贝塔系数]]
[[Markowitz均值方差优化]] -> [[20-Markowitz-均值方差优化]]
[[20-Markowitz均值方差优化]] -> [[20-Markowitz-均值方差优化]]
[[portfolio-optimization]] -> [[20-Markowitz-均值方差优化]]
[[factor-investing]] -> [[factor-investing]]
[[15-蒙特卡洛期权定价]] -> [[17-蒙特卡洛期权定价]]
```

- [ ] **Step 2: Convert future-only links to plain text**

Replace:

```text
[[31-树模型与非线性因子]] -> 后续专题：树模型与非线性因子
[[XGBoost和LightGBM]] -> 后续专题：XGBoost 和 LightGBM
[[risk-adjusted-returns]] -> 风险调整收益指标
```

- [ ] **Step 3: Run link checker**

Run: `python3 scripts/check_obsidian_links.py`

Expected: remaining broken links, if any, are only caused by code-like text that should be converted or by files not yet created.

### Task 4: Append Lesson Navigation Blocks

**Files:**
- Modify: each existing 1-33 lesson note under `notebooks/notes`

- [ ] **Step 1: Append one standard block when missing**

For each lesson note, append this block if it does not already contain `## 顺序通关导航`:

```markdown
---

## 顺序通关导航

- 上一课：[[PREVIOUS_NOTE]]
- 下一课：[[NEXT_NOTE]]
- 对应 Notebook：`NOTEBOOK_FILE`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
```

For lesson 01 use `无` as previous; for lesson 33 use `无` as next.

- [ ] **Step 2: Run link checker**

Run: `python3 scripts/check_obsidian_links.py`

Expected: no broken links from the new navigation blocks.

### Task 5: Update README Count

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update outdated count**

Replace:

```text
这个仓库包含 30 个 Jupyter Notebook
```

with:

```text
这个仓库目前包含 33 个 Jupyter Notebook
```

- [ ] **Step 2: Confirm no other stale count remains**

Run: `rg -n "30 个|33 个|Notebook" README.md notebooks/notes/00-主页.md`

Expected: README and homepage both describe 33 lessons or 33 notebooks consistently.

### Task 6: Final Verification

**Files:**
- No new files beyond previous tasks

- [ ] **Step 1: Run Obsidian link check**

Run: `python3 scripts/check_obsidian_links.py`

Expected: `No broken Obsidian wikilinks found.`

- [ ] **Step 2: Check route files mention all lessons**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
root = Path('notebooks/notes')
files = [
    root / '00-主页.md',
    root / '01-顺序通关路线.md',
    root / '02-复习清单.md',
]
for path in files:
    text = path.read_text(encoding='utf-8')
    missing = [f'{i:02d}' for i in range(1, 34) if f'[[{i:02d}-' not in text]
    print(f'{path}: missing lesson links {missing}')
    if missing:
        raise SystemExit(1)
PY
```

Expected: each file reports `missing lesson links []`.

- [ ] **Step 3: Review git diff**

Run: `git status --short` and `git diff --stat`

Expected: changes are limited to route files, note link/navigation updates, README, checker script, and plan/design docs.
