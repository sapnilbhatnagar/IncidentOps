"""CI-002: Format eval-results.json as a GitHub PR markdown comment.

Usage: python ops/pr_comment.py [eval-results.json]
Prints the comment body to stdout; pipe to gh pr comment or write to $GITHUB_STEP_SUMMARY.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def _status(row: dict) -> str:
    hard = row.get("hard_gate", False)
    ok = row.get("passed", True)
    if ok:
        return "PASS"
    return "FAIL" if hard else "ADVISORY"


def _icon(status: str) -> str:
    return {"PASS": "✅", "FAIL": "❌", "ADVISORY": "⚠️"}.get(status, "")


def format_comment(results: dict) -> str:
    gate = results.get("gate", "unknown").upper()
    gate_icon = "✅" if gate == "PASS" else "❌"

    lines = [
        f"## {gate_icon} HHH Eval — {gate}",
        "",
        "| Check | Score | Status |",
        "|---|---|---|",
    ]

    for row in results.get("checks", []):
        status = _status(row)
        icon = _icon(status)
        score = row.get("score", 0)
        n_pass = row.get("n_pass")
        n_total = row.get("n_total")
        score_str = f"{n_pass}/{n_total}" if n_pass is not None else f"{score:.3f}"
        lines.append(f"| `{row['check']}` | {score_str} | {icon} {status} |")

    hard_failures = results.get("hard_failures", [])
    advisory_failures = results.get("advisory_failures", [])

    if hard_failures:
        lines += ["", "**Blocking failures:**"]
        for f in hard_failures:
            lines.append(f"- `{f}`")

    if advisory_failures:
        lines += ["", "**Advisory (non-blocking):**"]
        for f in advisory_failures:
            lines.append(f"- `{f}`")

    lines += ["", "*Honest + Harmless failures block merge. Helpful is advisory.*"]
    return "\n".join(lines)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("eval-results.json")
    if not path.exists():
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    results = json.loads(path.read_text())
    print(format_comment(results))


if __name__ == "__main__":
    main()
