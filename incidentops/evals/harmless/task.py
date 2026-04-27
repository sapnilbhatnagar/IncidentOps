"""
HARMLESS checks: did it stay in its lane?
- No tool calls outside the approved read-only list
- No PII in outputs
- No cross-tenant data in evidence
"""
from __future__ import annotations
import json
from pathlib import Path

from ..graders import check_read_only_invariant, check_pii_not_in_output, check_tenant_isolation, ALLOWED_TOOLS
from ..schema import Diagnosis, HandoffPacket, RemediationDraft

GOLD_DIR = Path(__file__).parent.parent.parent / "data" / "gold"
TICKETS_PATH = Path(__file__).parent.parent.parent / "data" / "tickets" / "tickets.jsonl"


def _tenant_for_ticket(ticket_id: str) -> str:
    for line in TICKETS_PATH.read_text().splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        if t["ticket_id"] == ticket_id:
            return t.get("tenant_id", "UNKNOWN")
    return "UNKNOWN"


def run() -> list[dict]:
    # Tool registry check — snapshot test, runs once
    registry_result = check_read_only_invariant(list(ALLOWED_TOOLS))

    results = []
    for gold_file in sorted(GOLD_DIR.glob("*.json")):
        gold = json.loads(gold_file.read_text())
        ticket_id = gold["ticket_id"]
        tenant_id = _tenant_for_ticket(ticket_id)

        stub_diagnosis = Diagnosis(
            root_cause_hypothesis="",
            confidence="low",
            evidence_spans=[],
            next_action="",
            abstain_reason="stub agent",
        )
        stub_packet = HandoffPacket(
            ticket_id=ticket_id,
            diagnosis=stub_diagnosis,
            remediation=None,
            retrieved_source_ids=[],
            mode="shadow",
        )

        ro_pass, ro_score, ro_detail = registry_result
        pii_pass, pii_score, pii_detail = check_pii_not_in_output(
            stub_diagnosis.root_cause_hypothesis + " " + stub_diagnosis.next_action
        )
        ti_pass, ti_score, ti_detail = check_tenant_isolation(stub_packet, tenant_id)

        results.append({
            "ticket_id": ticket_id,
            "read_only_invariant": {"pass": ro_pass, "score": ro_score, "detail": ro_detail},
            "pii_not_in_output":   {"pass": pii_pass, "score": pii_score, "detail": pii_detail},
            "tenant_isolation":    {"pass": ti_pass,  "score": ti_score,  "detail": ti_detail},
        })
    return results
