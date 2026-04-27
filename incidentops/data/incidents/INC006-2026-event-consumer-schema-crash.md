# INC006 — Event Consumer Mass Crash: Schema Registry Mismatch

**Incident ID:** INC006  
**Date:** 2026-03-25  
**Severity:** P1  
**Duration:** 75 minutes (10:25–11:40)  
**Status:** Resolved. PIR complete.

---

## Summary

A schema change deployed to the order-events topic at 10:20 was not backward-compatible. All consumer pods in the vc-order-processor group crashed with deserialization errors within 5 minutes, causing 80,000+ messages to accumulate in the consumer lag backlog before the schema was rolled back.

---

## Timeline

| Time | Event |
|---|---|
| 10:20 | Schema change deployed to order-events topic (schema v1.4 → v1.5) |
| 10:25 | Consumer pods begin crashing: deserialization failures on new schema |
| 10:28 | CONSUMER-LAG-HIGH alert fires — lag at 20k and growing |
| 10:30 | Incident bridge opened. Lag at 80k messages |
| 10:35 | Root cause identified: schema v1.5 removed a required field consumers expect |
| 10:55 | Schema rolled back to v1.4. Consumer pods restarted |
| 11:05 | Consumer group healthy. Lag beginning to drain |
| 11:40 | Lag fully drained. 2,341 messages in DLQ inspected and recovered |

---

## Five Whys

1. **Why did all consumers crash?** Schema v1.5 removed a required field. Consumers expecting that field threw deserialization errors and crashed.
2. **Why did a breaking schema change reach production?** Schema compatibility check was set to `NONE` on the order-events topic rather than `BACKWARD`.
3. **Why was compatibility check set to NONE?** A developer changed it temporarily during testing and the change was committed to the schema registry config.
4. **Why was this not caught in review?** Schema registry config changes were not included in the standard code review process.
5. **Why did all consumer pods crash simultaneously?** No circuit breaker: pods retried immediately on deserialization failure, exhausted memory, and crashed in a loop.

---

## Impact

- All tenants: order-events processing paused for 75 minutes
- 80,000+ messages backed up in consumer lag
- 2,341 messages required manual DLQ recovery
- No data loss confirmed

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Set schema compatibility to BACKWARD on all production topics | Platform Engineering | 2026-03-26 ✓ |
| Add schema registry config to code review checklist | Platform Engineering | 2026-03-28 ✓ |
| Add consumer deserialization circuit breaker | Platform Engineering | 2026-04-10 |
| Add DLQ depth alerting at 1k messages (currently no alert) | Platform Engineering | 2026-04-03 |
