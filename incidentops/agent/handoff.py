"""AGENT-012: Handoff packet assembly."""
from __future__ import annotations

from typing import Literal

from .chunker import Chunk
from ..evals.schema import Diagnosis, HandoffPacket, RemediationDraft


def handoff(
    ticket_id: str,
    diagnosis: Diagnosis,
    chunks: list[Chunk],
    remediation: RemediationDraft | None,
    mode: Literal["shadow", "assist", "guided"] = "shadow",
) -> HandoffPacket:
    """Package diagnosis + retrieval provenance + remediation into a HandoffPacket."""
    return HandoffPacket(
        ticket_id=ticket_id,
        diagnosis=diagnosis,
        remediation=remediation,
        retrieved_source_ids=[c.source_id for c in chunks],
        mode=mode,
    )
