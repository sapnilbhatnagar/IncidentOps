---
id: INC001
title: Webhook Delivery Cascading Failure
date: 2025-09-11
duration_minutes: 52
severity: P1
products_affected: [Service Cloud, Integration Cloud]
tenants_affected: 184
events_delayed: 12438
related_runbooks: [RB003]
related_tickets: [TKT-2025-09-11-001, TKT-2025-09-11-002, TKT-2025-09-11-003]
status: Resolved-PIR-Complete
---

## Executive summary

On 11 September 2025, between 14:08 and 15:00 UTC, VertexCloud's webhook delivery service (VC-Webhooks) suffered a cascading failure that delayed delivery of 12,438 webhook events across 184 enterprise tenants. The trigger was a degraded primary delivery worker pool. Failover to standby was authorised at 14:14 but was blocked by an expired TLS certificate on the standby pool, extending the impact by 17 minutes. Standby came online at 14:31 and the backlog drained by 15:00.

Three Tier 1 enterprise customers reported missed events that broke real-time downstream workflows. No data was lost. No customer compensation paid as no SLA breach was contractually triggered, but two customers requested goodwill credits which were issued.

## Timeline

| Time (UTC) | Event |
|---|---|
| 14:08 | VC-Observability fires `WHK-WORKER-LATENCY-HIGH` on primary pool. |
| 14:09 | Worker NACK rate climbs past 1.8% in 60-second window. |
| 14:11 | LinkHealth check reports primary pool DEGRADED, standby pool HEALTHY. |
| 14:14 | Tier 3 SRE on-call authorises failover to standby. |
| 14:16 | Failover **fails**: TLS handshake to standby pool returns `certificate expired 2025-09-09`. |
| 14:17 | Incident bridge opened. Page to Integration Platform on-call and Identity Platform on-call. |
| 14:22 | Decision: emergency cert rotation on standby (per RB-SEC-12) rather than attempt to recover primary. |
| 14:31 | Standby pool online with rotated cert. Failover succeeds. |
| 14:38 | Backlog drain commences. Peak queue depth: 12,438 events. |
| 15:00 | Backlog drained. All tenants caught up. |
| 15:02 | Status page updated to resolved. |
| 15:30 | First customer comms drafted by Customer Success. |

## Customer impact

- 184 tenants experienced webhook delays of 6 to 52 minutes.
- 12,438 events delivered late but not lost.
- Three Tier 1 enterprise customers reported downstream workflow breakage:
  - Customer A: real-time fraud-screening pipeline missed events; manual replay required.
  - Customer B: real-time inventory-sync pipeline backlogged; resolved by replay.
  - Customer C: customer-facing notification pipeline delayed; minor user-facing impact.
- 11 tenants chose to use replay-by-time after recovery; replay completed within 4 hours.

## SLA exposure

VertexCloud's contracted webhook delivery SLA is 99.9% within 60 seconds for Enterprise tier. The 52-minute outage triggered SLA credit calculation on 184 tenants. After review, 138 tenants did not meet the credit threshold (impact below tenant-specific event volume floor). 46 tenants received automated SLA credits totalling $42,300. Two additional goodwill credits issued.

## Root cause analysis (5 whys)

**The certificate on the standby webhook delivery pool was expired.**

- Why? It was last rotated on 2024-09-09 with a 1-year validity, and the rotation calendar item slipped.
- Why did the calendar slip? The cert rotation calendar lived in the Identity Platform team's old wiki, which was archived during a Confluence consolidation in March 2025. The reminder was lost in archive.
- Why was there no automated detection? VC-Identity only monitors certs on production-active surfaces. Standby pool was treated as cold and excluded.
- Why was standby treated as cold? Historical assumption from when standby was a quarterly-tested DR plan, not an active-active part of the webhook delivery posture.
- Why did the assumption persist? No incident had forced a re-examination since the standby pool architecture changed in 2023.

## Lessons

1. Certificate rotation monitoring must cover all surfaces, including standby. (Action: Identity Platform, completed 2025-10-04.)
2. Rotation calendars must live in a single source of truth, not team-owned wikis. (Action: InfoSec, completed 2025-09-25.)
3. Failover playbooks must include a TLS pre-flight check. (Action: Integration Platform, completed 2025-09-30.)
4. Status page communication was 22 minutes late from incident start. Comms threshold should be tightened. (Action: Customer Success, in progress.)

## Why this matters for IncidentOps

The agent should have been able to:

- At 14:09, retrieve RB003 (webhook delivery failures) and RB-SEC-12 (cert rotation).
- At 14:14, recognise the failover-to-standby pattern and pre-fetch the standby's cert status.
- At 14:16, when failover failed with TLS error, immediately surface RB-SEC-12 and the prior cert rotation history.
- Throughout, draft customer comms language for Customer Success approval.

If the agent had compressed retrieval and reasoning time at each step by 60%, the impact window would have been ~30 minutes shorter. This is not a hypothetical: the runbooks already existed, the certs already had public expiry, and the prior similar incident in 2023 was already documented.
