"""HELPFUL: retrieval recall, diagnosis accuracy, schema validity."""
from __future__ import annotations

import json
import os
from pathlib import Path

from ..graders import check_diagnosis_accuracy, check_retrieval_recall, check_schema_validity
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

    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        ticket_id = gold["ticket_id"]

        if live:
            ticket = _load_ticket(ticket_id) or {"ticket_id": ticket_id}
            query = ticket.get("description", ticket.get("title", ticket_id))
            chunks = retrieve(query, top_k=5)
            diagnosis = diagnose(ticket, chunks)
            retrieved_ids = [c.source_id for c in chunks]
        else:
            diagnosis = _stub_diagnosis()
            retrieved_ids = []

        per_ticket.append({
            "ticket_id": ticket_id,
            "retrieval_recall":   _pack(check_retrieval_recall(retrieved_ids, gold["gold_runbook"])),
            "diagnosis_accuracy": _pack(check_diagnosis_accuracy(diagnosis, gold["gold_root_cause"])),
            "schema_validity":    _pack(check_schema_validity(diagnosis.model_dump())),
        })

    return {"per_ticket": per_ticket}


def _pack(t):
    return {"pass": t[0], "score": t[1], "detail": t[2]}
