from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VAULT_ROOT = REPO_ROOT / "notebooks"


@dataclass(frozen=True)
class BrokenLink:
    source: Path
    target: str
    raw: str


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "", text)


def normalize_target(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    if target.endswith(".md"):
        target = target[:-3]
    if target.endswith(".ipynb"):
        target = target[:-6]
    if "/" in target:
        target = Path(target).stem
    return target


def markdown_stems(vault_root: Path) -> set[str]:
    notes_root = vault_root / "notes"
    stems = {path.stem for path in notes_root.rglob("*.md")}
    stems.update(path.stem for path in vault_root.glob("*.md"))
    return stems


def markdown_files(vault_root: Path) -> list[Path]:
    notes_root = vault_root / "notes"
    return sorted(list(notes_root.rglob("*.md")) + list(vault_root.glob("*.md")))


def find_broken_links(vault_root: Path = DEFAULT_VAULT_ROOT) -> list[BrokenLink]:
    existing = markdown_stems(vault_root)
    broken: list[BrokenLink] = []
    for path in markdown_files(vault_root):
        text = strip_code(path.read_text(encoding="utf-8"))
        for match in re.finditer(r"\[\[([^\]]+)\]\]", text):
            raw = match.group(1)
            target = normalize_target(raw)
            if target and target not in existing:
                broken.append(BrokenLink(source=path, target=target, raw=raw))
    return broken


def main() -> int:
    broken = find_broken_links()
    if not broken:
        print("No broken Obsidian wikilinks found.")
        return 0

    print(f"Broken Obsidian wikilinks: {len(broken)}")
    for link in broken:
        rel = link.source.relative_to(DEFAULT_VAULT_ROOT)
        print(f"{rel}: [[{link.raw}]] -> missing target `{link.target}`")
    return 1


if __name__ == "__main__":
    sys.exit(main())
