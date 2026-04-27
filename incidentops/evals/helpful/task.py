"""HELPFUL: retrieval recall, diagnosis accuracy, schema validity."""
from __future__ import annotations
import json
from pathlib import Path

from ..graders import check_diagnosis_accuracy, check_retrieval_recall, check_schema_validity
from ..schema import Diagnosis

GOLD_DIR = Path(__file__).parent.parent.parent / "data" / "gold"


def stub_diagnosis() -> Diagnosis:
    return Diagnosis(
        root_cause_hypothesis="",
        confidence="low",
        evidence_spans=[],
        next_action="",
        abstain_reason="agent not yet wired",
    )


def run() -> dict:
    per_ticket: list[dict] = []
    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        diagnosis = stub_diagnosis()

        per_ticket.append({
            "ticket_id": gold["ticket_id"],
            "retrieval_recall":   _pack(check_retrieval_recall([], gold["gold_runbook"])),
            "diagnosis_accuracy": _pack(check_diagnosis_accuracy(diagnosis, gold["gold_root_cause"])),
            "schema_validity":    _pack(check_schema_validity(diagnosis.model_dump())),
        })
    return {"per_ticket": per_ticket}


def _pack(t):
    return {"pass": t[0], "score": t[1], "detail": t[2]}
