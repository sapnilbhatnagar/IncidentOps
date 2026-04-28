"""HONEST: citation coverage, citation precision, hallucination, source validity, calibration, abstention."""
from __future__ import annotations

import json
import os
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
TICKETS_FILE = Path(__file__).parent.parent.parent / "data" / "tickets" / "tickets.jsonl"


def _load_ticket(ticket_id: str) -> dict | None:
    for line in TICKETS_FILE.read_text().splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        if t["ticket_id"] == ticket_id:
            return t
    return None


def _stub_diagnosis() -> Diagnosis:
    return Diagnosis(
        root_cause_hypothesis="",
        confidence="low",
        evidence_spans=[],
        next_action="",
        abstain_reason="agent not yet wired",
    )


def run() -> dict:
    live = os.environ.get("INCIDENTOPS_LIVE") == "1"

    if live:
        from incidentops.agent.retrieve import retrieve
        from incidentops.agent.diagnose import diagnose

    per_ticket: list[dict] = []
    calibration_pairs: list[tuple[Diagnosis, bool]] = []

    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        ticket_id = gold["ticket_id"]

        if live:
            ticket = _load_ticket(ticket_id) or {"ticket_id": ticket_id}
            query = ticket.get("description", ticket.get("title", ticket_id))
            chunks = retrieve(query, top_k=5)
            diagnosis = diagnose(ticket, chunks)
            retrieved_count = len(chunks)
        else:
            diagnosis = _stub_diagnosis()
            retrieved_count = 0

        is_correct = not diagnosis.abstain_reason  # proxy: non-abstaining counts as "attempted"
        calibration_pairs.append((diagnosis, is_correct))

        per_ticket.append({
            "ticket_id":          ticket_id,
            "citation_coverage":  _pack(check_citation_coverage(diagnosis)),
            "citation_precision": _pack(check_citation_precision(diagnosis)),
            "hallucination_rate": _pack(check_hallucination(diagnosis)),
            "source_ids_valid":   _pack(check_source_ids_exist(diagnosis)),
            "abstention_quality": _pack(check_abstention_when_evidence_thin(diagnosis, retrieved_count)),
        })

    cal = check_calibration_brier(calibration_pairs)
    return {"per_ticket": per_ticket, "aggregate": {"calibration_brier": _pack(cal)}}


def _pack(t):
    return {"pass": t[0], "score": t[1], "detail": t[2]}
