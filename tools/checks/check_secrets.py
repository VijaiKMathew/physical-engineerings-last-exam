"""Refuse credential material in tracked text files."""

from __future__ import annotations

import re
from pathlib import Path

PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|kaggle_key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}"),
)
SKIP = {".venv", "data", "scratch", "logs", ".git", "__pycache__", "artifacts"}
SUFFIXES = {".py", ".md", ".json", ".toml", ".txt", ".yml", ".yaml"}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    root = repo_root()
    hits = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in SUFFIXES:
            continue
        if SKIP.intersection(path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PATTERNS:
            if pattern.search(text):
                hits.append(f"{path.relative_to(root)} matches {pattern.pattern}")
    if hits:
        print("secrets scan failed:")
        print("\n".join(hits))
        return 1
    print("secrets scan OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
