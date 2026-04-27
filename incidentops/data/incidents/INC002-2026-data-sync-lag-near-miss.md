---
id: INC002
title: Cross-Product Data Sync Lag Near-Miss
date: 2026-02-04
duration_minutes: 36
severity: P1
products_affected: [CRM Cloud, Analytics Cloud]
tenants_affected: 47
sla_breach: false
related_runbooks: [RB004]
related_tickets: [TKT-2026-02-04-001]
status: Resolved-PIR-Complete
---

## Executive summary

On 4 February 2026, between 17:30 and 18:06 UTC, VC-Sync (the cross-product data sync service) experienced replication lag that climbed from a baseline of 35 seconds to a peak of 28 minutes between CRM Cloud and Analytics Cloud. 47 enterprise tenants were affected. The contracted real-time data freshness SLA on Enterprise tier is "under 5 minutes for 99% of records". Lag breached this for 36 minutes.

A formal SLA breach would have triggered credits totalling approximately $185,000. The breach was avoided by a near-miss: contractual lag is measured on a per-tenant rolling 24h average, and the spike was short enough that 24h average remained within bound for all but one tenant. That tenant accepted goodwill comms in lieu of a credit.

## Timeline

| Time (UTC) | Event |
|---|---|
| 17:30 | VC-Observability fires `VC-DATAPLATFORM-LATENCY-HIGH`. NS-CoreBank ledger lookup p95 climbs from 35ms to 284ms. |
| 17:54 | VC-Sync emits `SYNC-LAG-HIGH`. Lag at 8 minutes and climbing. |
| 18:00 | Tier 3 SRE on-call paged. Hypothesis: downstream contention on VC-DataPlatform. |
| 18:03 | Worker pool scaled from 8 to 24. Lag plateaus. |
| 18:09 | Lag begins decreasing. |
| 18:34 | Lag back under 60s. |
| 18:42 | Root cause confirmed: a Q1 reporting batch was running on the live production cluster contrary to ringfencing policy. |
| 18:48 | Reporting batch killed. |
| 19:15 | Lag at baseline. |

## Customer impact

- 47 tenants saw real-time analytics dashboards stale by up to 28 minutes.
- One Tier 1 customer running a customer-facing dashboard at near-real-time noticed the lag and raised a complaint. They received goodwill credit and a written apology from the VP Customer Support.
- No data was lost. All records eventually synced.

## SLA exposure

Contracted SLA: data freshness under 5 minutes for 99% of records on Enterprise tier, measured as a per-tenant rolling 24h average.

Spike was 36 minutes wide. 24h average bound was breached on 1 tenant, not breached on 46. Total contractual exposure: ~$1,800 (the one tenant). Total goodwill: $4,000.

If the spike had lasted 75 minutes instead of 36, the average bound would have been breached on all 47 tenants, with credits of ~$185,000. The agent should be able to recognise this trajectory and surface it as an escalation trigger.

## Root cause analysis (5 whys)

**The Q1 reporting batch was running on the live production cluster.**

- Why? It was scheduled there by the data engineering team's batch orchestrator.
- Why did the orchestrator schedule it on production? The ringfencing config was set to "non-production preferred, production permitted" rather than "non-production only".
- Why was the config that permissive? It had been temporarily relaxed during a 2025 capacity issue and never tightened back.
- Why was it not tightened back? No automation tracked the temporary relaxation. The ticket was closed when the immediate issue resolved.
- Why was there no automation? Historical assumption that ringfencing config changes are infrequent enough to track manually.

## Lessons

1. Ringfencing config changes must be auditable, time-bounded, and automatically reverted unless renewed. (Action: Data Platform, in progress.)
2. The on-call playbook for `VC-DATAPLATFORM-LATENCY-HIGH` did not include "check the batch orchestrator schedule". This was the fastest path to root cause. (Action: Data Platform, completed 2026-02-12.)
3. SLA trajectory monitoring (not just current state) would have flagged the 24h-average risk earlier. (Action: Customer Success Ops, in progress.)

## Why this matters for IncidentOps

The agent should have been able to:

- At 17:30, on the latency alert, surface the relationship between VC-DataPlatform latency and downstream sync lag (RB004).
- At 17:54 on the lag alert, surface the most recent ringfencing config changes from the data engineering team's audit log.
- Throughout, project the SLA breach trajectory based on current lag and 24h average, and escalate when the trajectory crossed a threshold.

This is the kind of multi-source reasoning that costs senior engineers ~30 minutes of context-gathering even when they know exactly what to look for. The agent compresses that to seconds.
