"""Shared output types. The agent produces a Diagnosis; graders inspect it."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel


class EvidenceSpan(BaseModel):
    source_id: str      # e.g. "RB001", "TKT-2026-03-04-001", "INC003"
    text: str           # the quoted passage
    span_start: int
    span_end: int


class Diagnosis(BaseModel):
    root_cause_hypothesis: str
    confidence: Literal["high", "medium", "low"]
    evidence_spans: list[EvidenceSpan]
    next_action: str
    abstain_reason: str | None = None   # set when agent declines to diagnose


class RemediationDraft(BaseModel):
    steps: list[str]
    expected_effect: str
    rollback_note: str | None
    required_human_approver: str | None


class HandoffPacket(BaseModel):
    ticket_id: str
    diagnosis: Diagnosis
    remediation: RemediationDraft | None
    retrieved_source_ids: list[str]
    mode: Literal["shadow", "assist", "guided"]
