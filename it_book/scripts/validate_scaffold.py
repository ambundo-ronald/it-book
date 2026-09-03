from __future__ import annotations

import json
import py_compile
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = APP_ROOT.parent


def main() -> int:
    validate_json()
    validate_python()
    validate_required_files()
    print("IT Book scaffold validation passed.")
    return 0


def validate_json():
    for path in REPO_ROOT.rglob("*.json"):
        with path.open(encoding="utf-8") as handle:
            json.load(handle)


def validate_python():
    for path in APP_ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        py_compile.compile(str(path), doraise=True)


def validate_required_files():
    required = [
        "it_book/pyproject.toml",
        "it_book/it_book/hooks.py",
        "it_book/it_book/reporting/api.py",
        "it_book/it_book/reporting/summary.py",
        "it_book/it_book/page/it_book_dashboard/it_book_dashboard.js",
        "it_book/it_book/page/it_book_dashboard/it_book_dashboard.json",
        "it_book/it_book/doctype/it_project/it_project.json",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).exists()]
    if missing:
        raise FileNotFoundError(f"Missing required scaffold files: {', '.join(missing)}")


if __name__ == "__main__":
    raise SystemExit(main())
