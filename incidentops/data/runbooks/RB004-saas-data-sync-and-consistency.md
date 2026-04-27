---
id: RB004
title: Data Sync and Consistency Issues (Lag, Missing Records, Dedup, Schema, Conflict)
last_updated: 2026-02-28
owner: data-platform
severity_levels: [P3, P2, P1]
related_runbooks: [RB003]
related_codes: [SYNC-LAG, SYNC-MISSING, SYNC-DEDUP-FAIL, SYNC-SCHEMA-MISMATCH, SYNC-CONFLICT]
---

## When to use

Use this runbook when one or more of the following is observed:

- Customer reports records missing or duplicated in target product or warehouse.
- VC-Sync emits elevated lag, missing-record, or dedup-fail events.
- Cross-product workflows break because data has not propagated.

## Symptoms

- Customer ticket: "the record exists in CRM but not in Analytics", "we are getting double rows in our warehouse", "the dashboard is 30 minutes stale".
- VC-Observability alert: `SYNC-LAG-HIGH` or `SYNC-MISSING-RATE`.

## Severity

- **P1**: data-integrity event affecting multiple tenants or breaching contractual data-freshness SLA.
- **P2**: single-tenant inconsistency on a critical integration.
- **P3**: single-record discrepancy.

## Initial triage (5 minutes)

1. Identify scope: one record, one record class, one tenant, or platform-wide?
2. Pull VC-Sync worker pool metrics and replication lag for the affected pipeline.
3. Check VC-DataPlatform for recent schema changes or migrations.
4. Confirm whether customer recently changed sync configuration, filter rules, or destination credentials.

## Investigation by code

### SYNC-LAG

Replication lag above threshold (default 5 min).

- Inspect worker pool saturation. Scale if backlog is real load.
- Look for downstream contention: target system slow, target schema lock, etc.
- Check for tenant skew: one tenant generating 10x normal volume can starve others.

### SYNC-MISSING

Record exists in source, not in target.

- Trace the sync event log for the record's identifier.
- Confirm whether filter rules, permissions, or schema validation excluded it.
- Check whether the record was created during a known sync outage window.

### SYNC-DEDUP-FAIL

Duplicate records in target.

- Inspect dedup-key derivation. Did the dedup-key shape change recently?
- A common cause: customer upgraded SDK and the new SDK regenerated identifiers on retry.
- Check for source-side replays that may have created divergent dedup-keys for the same logical record.

### SYNC-SCHEMA-MISMATCH

Source produced field target does not understand.

- Confirm schema version pinning.
- If schema migration in flight, coordinate with the migration owner.
- Most often follows a feature ship where the source side started populating a new optional field.

### SYNC-CONFLICT

Concurrent writes to the same record.

- Surface the conflict resolution policy (last-write-wins or CRDT) for the affected entity.
- Confirm with customer which version to retain.
- For systemic conflicts, escalate to data platform.

## Common causes (ranked by frequency)

1. Customer SDK upgrade changed dedup-key shape.
2. Schema migration in flight, source ahead of target.
3. Worker pool starvation due to a single noisy tenant.
4. Filter rules in customer config excluded records they expected to receive.
5. Platform-side data-platform incident (rare, P1).

## Remediation

- For dedup-key drift: identify affected records, hand off to Reconciliation team for de-duplication. The agent does not deduplicate.
- For lag: scale worker pool if appropriate; engage Data Platform on-call if platform-side.
- For missing records: confirm root cause, then hand off to Reconciliation team for backfill.
- Never modify customer data. Never deduplicate. Never delete. The agent investigates and proposes; humans execute.

## Escalation

- P1: page Data Platform on-call, open incident bridge, notify VP Customer Support and DPO if data-integrity event.
- P2: assign to Data Platform queue, target 4h.
- P3: standard support response.

## Post-resolution checklist

- Customer confirms data state matches expectation.
- Reconciliation actions logged.
- If data-integrity event, file with DPO for record-keeping.
- If pattern repeats, surface to engineering for product fix.
