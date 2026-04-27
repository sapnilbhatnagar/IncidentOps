"""HONEST: citation coverage, citation precision, hallucination, source validity, calibration, abstention."""
from __future__ import annotations
import json
from pathlib import Path

from ..graders import (
    check_abstention_when_evidence_thin,
    check_calibration_brier,
    check_citation_coverage,
    check_citation_precision,
    check_hallucination,
    check_source_ids_exist,
)
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
    calibration_pairs: list[tuple[Diagnosis, bool]] = []

    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        diagnosis = stub_diagnosis()
        retrieved_count = 0  # stub returns nothing

        cov  = check_citation_coverage(diagnosis)
        prec = check_citation_precision(diagnosis)
        hal  = check_hallucination(diagnosis)
        src  = check_source_ids_exist(diagnosis)
        abs_ = check_abstention_when_evidence_thin(diagnosis, retrieved_count)

        per_ticket.append({
            "ticket_id": gold["ticket_id"],
            "citation_coverage":  _pack(cov),
            "citation_precision": _pack(prec),
            "hallucination_rate": _pack(hal),
            "source_ids_valid":   _pack(src),
            "abstention_quality": _pack(abs_),
        })
        calibration_pairs.append((diagnosis, False))

    cal = check_calibration_brier(calibration_pairs)
    return {"per_ticket": per_ticket, "aggregate": {"calibration_brier": _pack(cal)}}


def _pack(t):
    return {"pass": t[0], "score": t[1], "detail": t[2]}
