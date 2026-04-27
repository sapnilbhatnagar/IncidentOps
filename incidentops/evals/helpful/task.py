"""
HELPFUL checks: did it actually help?
- Did it find the right runbook?
- Did the diagnosis match the gold answer?

Note: with a stub agent these will fail — that is correct and expected.
The point is to prove the graders are wired up before the agent exists.
"""
from __future__ import annotations
import json
from pathlib import Path

from ..graders import check_retrieval_recall, check_diagnosis_accuracy
from ..schema import Diagnosis

GOLD_DIR = Path(__file__).parent.parent.parent / "data" / "gold"


def run() -> list[dict]:
    results = []
    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        ticket_id = gold["ticket_id"]

        stub = Diagnosis(
            root_cause_hypothesis="",
            confidence="low",
            evidence_spans=[],
            next_action="",
            abstain_reason="stub agent — no model wired yet",
        )

        rr_pass, rr_score, rr_detail = check_retrieval_recall([], gold["gold_runbook"])
        da_pass, da_score, da_detail = check_diagnosis_accuracy(stub, gold["gold_root_cause"])

        results.append({
            "ticket_id": ticket_id,
            "retrieval_recall":   {"pass": rr_pass, "score": rr_score, "detail": rr_detail},
            "diagnosis_accuracy": {"pass": da_pass, "score": da_score, "detail": da_detail},
        })
    return results
