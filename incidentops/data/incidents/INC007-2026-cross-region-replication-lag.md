# INC007 — Cross-Region Replication Lag: Network Partition

**Incident ID:** INC007  
**Date:** 2026-03-28  
**Severity:** P1  
**Duration:** 70 minutes replication lag (08:00–09:10), customer impact until 09:40  
**Status:** Resolved. PIR complete.

---

## Summary

A 30-minute network partition between US-EAST-1 and EU-WEST-1 at 08:00 caused cross-region replication to pause. When the partition resolved, 45 minutes of accumulated lag required ~70 minutes to drain, during which EU enterprise customers saw data written in the US with up to 45-minute staleness.

---

## Timeline

| Time | Event |
|---|---|
| 08:00 | Network partition begins between US-EAST-1 and EU-WEST-1 |
| 08:00–08:30 | Replication paused. Lag accumulating at write-throughput rate |
| 08:30 | Partition resolves. Replication resumes. Accumulated lag: ~45 minutes |
| 08:35 | REPLICATION-LAG-HIGH alert fires (threshold: 30s) |
| 08:40 | SRE opens incident bridge. Lag at 45 minutes and beginning to drain |
| 08:45 | EU TAMs notified. 10 enterprise customers identified as affected |
| 09:10 | Lag drained to < 5s |
| 09:40 | All EU enterprise customers confirm data freshness restored |

---

## Five Whys

1. **Why did EU customers see stale data?** Cross-region replication paused for 30 minutes, then took 40 minutes to catch up.
2. **Why did replication pause?** Network partition prevented replication connection between regions.
3. **Why was the partition 30 minutes long?** Cloud provider BGP routing issue — outside VertexCloud's control.
4. **Why did lag take 40 minutes to drain after the partition?** Replication channel was not given priority bandwidth to catch up faster.
5. **Why was replication lag alert threshold 30s?** Alert threshold had not been reviewed since replication architecture changed — 30s is too aggressive for transient spikes.

---

## Impact

- 10 EU enterprise customers: data staleness up to 45 minutes
- No data loss — all writes replicated once partition resolved
- 0 SLA breaches (EU SLA allows up to 60 minutes replication lag for network partition events)

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Implement priority bandwidth lane for replication catch-up | Platform Engineering | 2026-04-15 |
| Review and update replication lag alert thresholds | Platform Engineering | 2026-04-03 ✓ |
| Add proactive customer comms playbook for replication lag events | CS Ops | 2026-04-05 ✓ |
| Add network partition to quarterly DR test scenarios | Platform Engineering | 2026-05-01 |
