"""
CLI runner. Produces human-readable output and exits non-zero if any hard gate fails.
Usage: python -m incidentops.evals.run_evals
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

from .helpful.task import run as run_helpful
from .honest.task import run as run_honest
from .harmless.task import run as run_harmless

CONFIG = json.loads((Path(__file__).parent / "config.json").read_text())

# Which per-ticket checks map to which config keys, and whether they're hard gates
CHECK_MAP = {
    # category         check_key                config_section   config_key                 hard_gate
    ("helpful",  "retrieval_recall"):    ("helpful",   "retrieval_recall_at_3",    False),
    ("helpful",  "diagnosis_accuracy"):  ("helpful",   "diagnosis_accuracy",       False),
    ("honest",   "citation_coverage"):   ("honest",    "citation_coverage",        True),
    ("honest",   "hallucination_rate"):  ("honest",    "hallucination_rate",       True),
    ("honest",   "source_ids_valid"):    ("honest",    "citation_coverage",        True),
    ("harmless", "read_only_invariant"): ("harmless",  "read_only_violations",     True),
    ("harmless", "pii_not_in_output"):   ("harmless",  "pii_leakages",             True),
    ("harmless", "tenant_isolation"):    ("harmless",  "cross_tenant_leakages",    True),
}


def agg(results: list[dict], key: str) -> tuple[float, int, int]:
    """Return (mean_score, n_pass, n_total) for a check across all tickets."""
    scores = [r[key]["score"] for r in results if key in r]
    passes = [r[key]["pass"] for r in results if key in r]
    if not scores:
        return 0.0, 0, 0
    return sum(scores) / len(scores), sum(passes), len(passes)


def main() -> None:
    helpful_results  = run_helpful()
    honest_results   = run_honest()
    harmless_results = run_harmless()

    all_results = {
        "helpful":  helpful_results,
        "honest":   honest_results,
        "harmless": harmless_results,
    }

    check_keys = {
        "helpful":  ["retrieval_recall", "diagnosis_accuracy"],
        "honest":   ["citation_coverage", "hallucination_rate", "source_ids_valid"],
        "harmless": ["read_only_invariant", "pii_not_in_output", "tenant_isolation"],
    }

    hard_gate_failures: list[str] = []
    advisory_failures:  list[str] = []

    print("\nEVAL RESULTS")
    print("=" * 60)

    for category, keys in check_keys.items():
        print(f"\n{category.upper()}")
        for key in keys:
            mean_score, n_pass, n_total = agg(all_results[category], key)
            map_entry = CHECK_MAP.get((category, key))
            is_hard = map_entry[2] if map_entry else False
            gate_label = "HARD GATE" if is_hard else "advisory"

            all_pass = n_pass == n_total
            status = "PASS" if all_pass else ("FAIL" if is_hard else "ADVISORY ↓")
            label = f"{category}/{key}"

            print(f"  {label:<40}  {mean_score:.2f}  {n_pass}/{n_total} tickets  [{status}]")

            if not all_pass:
                if is_hard:
                    hard_gate_failures.append(label)
                else:
                    advisory_failures.append(label)

    print("\n" + "=" * 60)
    if hard_gate_failures:
        print(f"GATE RESULT: FAIL — {len(hard_gate_failures)} hard gate(s) failed:")
        for f in hard_gate_failures:
            print(f"  ✗ {f}")
        sys.exit(1)
    else:
        if advisory_failures:
            print(f"GATE RESULT: PASS (with {len(advisory_failures)} advisory check(s) below target)")
        else:
            print("GATE RESULT: PASS")


if __name__ == "__main__":
    main()
