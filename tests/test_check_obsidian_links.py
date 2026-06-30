from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_obsidian_links import find_broken_links


class CheckObsidianLinksTest(unittest.TestCase):
    def test_reports_missing_wikilinks_and_ignores_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            notes = vault / "notes"
            notes.mkdir()
            (notes / "Existing.md").write_text("# Existing\n", encoding="utf-8")
            (notes / "Source.md").write_text(
                "\n".join(
                    [
                        "[[Existing]]",
                        "[[Missing]]",
                        "`[[IgnoredInline]]`",
                        "```python",
                        "df[[\"IgnoredFence\"]]",
                        "```",
                    ]
                ),
                encoding="utf-8",
            )

            broken = find_broken_links(vault)

        self.assertEqual(len(broken), 1)
        self.assertEqual(broken[0].target, "Missing")


if __name__ == "__main__":
    unittest.main()
