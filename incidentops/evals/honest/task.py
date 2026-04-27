"""
HONEST checks: can you trust what the agent said?
- Did it cite its sources?
- Did it make anything up?
- Are the sources it cited real?
"""
from __future__ import annotations
import json
from pathlib import Path

from ..graders import check_citation_coverage, check_hallucination, check_source_ids_exist
from ..schema import Diagnosis

GOLD_DIR = Path(__file__).parent.parent.parent / "data" / "gold"


def run() -> list[dict]:
    results = []
    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        ticket_id = gold["ticket_id"]

        # Stub agent: always abstains — no real agent yet
        stub = Diagnosis(
            root_cause_hypothesis="",
            confidence="low",
            evidence_spans=[],
            next_action="",
            abstain_reason="stub agent — no model wired yet",
        )

        c_pass, c_score, c_detail = check_citation_coverage(stub)
        h_pass, h_score, h_detail = check_hallucination(stub)
        s_pass, s_score, s_detail = check_source_ids_exist(stub)

        results.append({
            "ticket_id": ticket_id,
            "citation_coverage":  {"pass": c_pass, "score": c_score, "detail": c_detail},
            "hallucination_rate": {"pass": h_pass, "score": h_score, "detail": h_detail},
            "source_ids_valid":   {"pass": s_pass, "score": s_score, "detail": s_detail},
        })
    return results
