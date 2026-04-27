"""CLI runner. Exits non-zero if any hard gate fails."""
from __future__ import annotations
import json
import sys
from pathlib import Path

from .harmless.task import run as run_harmless
from .helpful.task import run as run_helpful
from .honest.task import run as run_honest

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())

# (category, check_key) → (config_section, config_key, hard_gate)
HARD_GATES: dict[tuple[str, str], bool] = {
    ("helpful",  "retrieval_recall"):    False,
    ("helpful",  "diagnosis_accuracy"):  False,
    ("helpful",  "schema_validity"):     True,
    ("honest",   "citation_coverage"):   True,
    ("honest",   "citation_precision"):  True,
    ("honest",   "hallucination_rate"):  True,
    ("honest",   "source_ids_valid"):    True,
    ("honest",   "abstention_quality"):  False,
    ("honest",   "calibration_brier"):   True,
    ("harmless", "read_only_invariant"): True,
    ("harmless", "pii_not_in_output"):   True,
    ("harmless", "tenant_isolation"):    True,
    ("harmless", "injection_refusal_rate"):    True,
    ("harmless", "out_of_scope_refusal_rate"): True,
}


def aggregate_per_ticket(per_ticket: list[dict], key: str) -> tuple[float, int, int]:
    scores = [r[key]["score"] for r in per_ticket if key in r]
    passes = [r[key]["pass"] for r in per_ticket if key in r]
    if not scores:
        return 0.0, 0, 0
    return sum(scores) / len(scores), sum(passes), len(passes)


def main() -> None:
    suites = {
        "helpful":  run_helpful(),
        "honest":   run_honest(),
        "harmless": run_harmless(),
    }

    print("\nEVAL RESULTS")
    print("=" * 72)

    hard_failures: list[str] = []
    advisory_failures: list[str] = []

    for category, suite in suites.items():
        print(f"\n{category.upper()}")
        per_ticket = suite.get("per_ticket", [])
        if per_ticket:
            check_keys = [k for k in per_ticket[0].keys() if k != "ticket_id"]
            for key in check_keys:
                mean, n_pass, n_total = aggregate_per_ticket(per_ticket, key)
                _emit(category, key, mean, n_pass, n_total, hard_failures, advisory_failures)

        for key, value in suite.get("aggregate", {}).items():
            label = f"{category}/{key}"
            is_hard = HARD_GATES.get((category, key), False)
            passed = value["pass"]
            status = "PASS" if passed else ("FAIL" if is_hard else "ADVISORY ↓")
            print(f"  {label:<44}  {value['score']:.3f}  [{status}]   {value['detail']}")
            if not passed:
                (hard_failures if is_hard else advisory_failures).append(label)

    print("\n" + "=" * 72)
    if hard_failures:
        print(f"GATE RESULT: FAIL — {len(hard_failures)} hard gate(s):")
        for f in hard_failures:
            print(f"  ✗ {f}")
        sys.exit(1)
    advisory_note = f" ({len(advisory_failures)} advisory below target)" if advisory_failures else ""
    print(f"GATE RESULT: PASS{advisory_note}")


def _emit(category, key, mean, n_pass, n_total, hard, advisory):
    label = f"{category}/{key}"
    is_hard = HARD_GATES.get((category, key), False)
    all_pass = n_pass == n_total
    status = "PASS" if all_pass else ("FAIL" if is_hard else "ADVISORY ↓")
    print(f"  {label:<44}  {mean:.2f}  {n_pass}/{n_total}   [{status}]")
    if not all_pass:
        (hard if is_hard else advisory).append(label)


if __name__ == "__main__":
    main()
