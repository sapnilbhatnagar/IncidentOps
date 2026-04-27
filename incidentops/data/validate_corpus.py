"""CORPUS-007: Validate corpus counts and emit JSON manifest."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

TARGETS = {
    "runbooks": 15,
    "tickets": 40,
    "incidents": 8,
    "gold": 30,
}


def count_files(directory: Path, suffix: str) -> list[Path]:
    return sorted(directory.glob(f"*{suffix}")) if directory.exists() else []


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text().splitlines() if line.strip())


def validate_gold(gold_dir: Path) -> tuple[int, list[str]]:
    files = count_files(gold_dir, ".json")
    errors = []
    required = {"ticket_id", "gold_runbook", "gold_root_cause", "gold_remediation", "difficulty"}
    for f in files:
        try:
            record = json.loads(f.read_text())
            missing = required - record.keys()
            if missing:
                errors.append(f"{f.name}: missing fields {missing}")
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}: invalid JSON — {e}")
    return len(files), errors


def main() -> None:
    runbooks = count_files(ROOT / "runbooks", ".md")
    incidents = count_files(ROOT / "incidents", ".md")
    tickets = count_jsonl(ROOT / "tickets" / "tickets.jsonl")
    gold_count, gold_errors = validate_gold(ROOT / "gold")

    counts = {
        "runbooks": len(runbooks),
        "tickets": tickets,
        "incidents": len(incidents),
        "gold": gold_count,
    }

    passed = True
    results = {}
    for key, target in TARGETS.items():
        actual = counts[key]
        ok = actual >= target
        results[key] = {"actual": actual, "target": target, "pass": ok}
        if not ok:
            passed = False

    manifest = {"counts": results, "gold_errors": gold_errors, "overall": "PASS" if passed and not gold_errors else "FAIL"}
    print(json.dumps(manifest, indent=2))

    if not passed or gold_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
