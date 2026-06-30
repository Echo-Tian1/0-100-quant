from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS_DIR = REPO_ROOT / "notebooks"
NOTES_DIR = NOTEBOOKS_DIR / "notes"


class LearningMaterialsIntegrityTest(unittest.TestCase):
    def test_all_notebooks_are_valid_json(self) -> None:
        invalid: list[str] = []
        for path in sorted(NOTEBOOKS_DIR.glob("*.ipynb")):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                invalid.append(f"{path.name}: {exc}")

        self.assertEqual(invalid, [])

    def test_route_files_cover_all_34_lessons(self) -> None:
        route_files = [
            NOTES_DIR / "00-主页.md",
            NOTES_DIR / "01-顺序通关路线.md",
            NOTES_DIR / "02-复习清单.md",
        ]
        for path in route_files:
            text = path.read_text(encoding="utf-8")
            missing = [f"{idx:02d}" for idx in range(1, 35) if f"[[{idx:02d}-" not in text]
            with self.subTest(path=path.name):
                self.assertEqual(missing, [])

    def test_all_34_lesson_notes_have_navigation_blocks(self) -> None:
        lesson_notes = [
            "01-Python核心语法",
            "02-NumPy数组运算",
            "03-随机数与蒙特卡洛",
            "04-Pandas时序处理",
            "05-AKShare均线波动率",
            "06-Pandas数据清洗",
            "07-AKShare与SQLite",
            "08-Matplotlib金融可视化",
            "09-K线布林带最大回撤",
            "10-SciPy统计分析",
            "11-股票筛选器",
            "12-CAPM贝塔系数",
            "13-Fama-French三因子模型",
            "14-Fama-French五因子模型",
            "15-因子模型总结",
            "16-BS公式与Greeks",
            "17-蒙特卡洛期权定价",
            "18-亚式期权定价",
            "19-VaR-CVaR",
            "20-Markowitz-均值方差优化",
            "21-组合优化器",
            "22-均线策略与参数优化",
            "23-动量与均值回归策略",
            "24-backtrader事件驱动回测",
            "25-因子构建与检验",
            "26-回测陷阱专题",
            "27-绩效归因分析",
            "28-策略研究报告",
            "29-特征工程与数据准备",
            "30-机器学习量化入门",
            "31-QLib框架入门",
            "32-手写回测引擎",
            "33-风控系统设计",
            "34-量化策略全流程",
        ]
        missing_navigation: list[str] = []
        for note_name in lesson_notes:
            matches = list(NOTES_DIR.rglob(f"{note_name}.md"))
            if not matches:
                missing_navigation.append(f"{note_name}: missing note")
                continue
            text = matches[0].read_text(encoding="utf-8")
            if "## 顺序通关导航" not in text:
                missing_navigation.append(f"{note_name}: missing navigation")

        self.assertEqual(missing_navigation, [])

    def test_license_file_exists(self) -> None:
        self.assertTrue((REPO_ROOT / "LICENSE").exists())

    def test_requirements_include_key_course_dependencies(self) -> None:
        requirements = (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8")
        required_names = [
            "numpy",
            "pandas",
            "matplotlib",
            "scipy",
            "akshare",
            "scikit-learn",
            "backtrader",
            "vectorbt",
            "jupyter",
        ]

        missing = [name for name in required_names if name not in requirements]

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
