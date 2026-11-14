"""Validate CHAMPION.json ledger configuration and existence."""

from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    root = repo_root()
    champ_path = root / "CHAMPION.json"
    if not champ_path.exists():
        print(f"Warning: {champ_path.name} not initialized yet.")
        return 0

    try:
        data = json.loads(champ_path.read_text(encoding="utf-8"))
        required_keys = ["label", "model_api", "dev_score", "date"]
        missing = [k for k in required_keys if k not in data]
        if missing:
            print(f"check_champion FAILED: Missing required keys: {missing}")
            return 1
        print(f"check_champion OK: {data['label']} ({data.get('model_api')}, dev_score={data.get('dev_score')})")
        return 0
    except Exception as e:
        print(f"check_champion ERROR: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
