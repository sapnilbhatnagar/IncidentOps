"""AGENT-013: End-to-end pipeline — triage → retrieve → diagnose → tools → remediate → handoff."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from .chunker import Chunk
from .diagnose import diagnose
from .handoff import handoff
from .remediate import remediate
from .retrieve import retrieve
from ..evals.schema import HandoffPacket

_TICKETS_FILE = Path(__file__).parent.parent / "data" / "tickets" / "tickets.jsonl"


def _load_ticket(ticket_id: str) -> dict | None:
    for line in _TICKETS_FILE.read_text().splitlines():
        if not line.strip():
            continue
        t = json.loads(line)
        if t["ticket_id"] == ticket_id:
            return t
    return None


def run(
    ticket_id: str,
    top_k: int = 5,
    mode: Literal["shadow", "assist", "guided"] = "shadow",
    skip_remediation: bool = False,
) -> HandoffPacket:
    """
    Full pipeline for a single ticket.

    shadow  — diagnosis + draft are computed but not surfaced to customer.
    assist  — draft shown to engineer before they respond.
    guided  — engineer works through the draft step-by-step.
    """
    ticket = _load_ticket(ticket_id)
    if ticket is None:
        ticket = {"ticket_id": ticket_id}

    # Stage 1+2: triage query + retrieve
    query = ticket.get("description", ticket.get("title", ticket_id))
    chunks: list[Chunk] = retrieve(query, top_k=top_k)

    # Stage 3: diagnose
    diagnosis = diagnose(ticket, chunks)

    # Stage 4: tool calls happen inside diagnose() (the model calls tools via tool_use)
    # The five registered tools are available to the diagnosis stage via the prompt context.

    # Stage 5: remediate (skip if abstaining or explicitly skipped)
    remediation_draft = None
    if not diagnosis.abstain_reason and not skip_remediation:
        remediation_draft = remediate(diagnosis, ticket)

    # Stage 6: handoff
    return handoff(ticket_id, diagnosis, chunks, remediation_draft, mode)


def main() -> None:
    import sys
    ticket_id = sys.argv[1] if len(sys.argv) > 1 else "TKT-2026-03-04-001"
    print(f"Running pipeline for {ticket_id} …")
    packet = run(ticket_id, skip_remediation=True)
    print(f"\nDiagnosis: {packet.diagnosis.root_cause_hypothesis or '(abstained)'}")
    print(f"Confidence: {packet.diagnosis.confidence}")
    print(f"Retrieved: {packet.retrieved_source_ids}")
    if packet.diagnosis.abstain_reason:
        print(f"Abstain reason: {packet.diagnosis.abstain_reason}")


if __name__ == "__main__":
    main()
