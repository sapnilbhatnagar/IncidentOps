# INC003 — Database Connection Pool Cascade

**Incident ID:** INC003  
**Date:** 2026-03-20  
**Severity:** P1  
**Duration:** 38 minutes (14:10–14:48)  
**Status:** Resolved. PIR complete.

---

## Summary

A single enterprise tenant running quarter-end reporting on the production database cluster held 340 of 350 available connections for 40 minutes, causing API latency to exceed 8s p95 across all tenants and triggering SLA breach risk for 6 enterprise accounts.

---

## Timeline

| Time | Event |
|---|---|
| 13:30 | Tenant TEN-IRONGATE-2023 scheduled quarter-end batch reporting job |
| 14:10 | VC-API-GATEWAY-LATENCY-HIGH alert fires — p95 at 2s |
| 14:15 | p95 now 5s. SRE opens incident bridge |
| 14:20 | p95 now 8s. Error rate starting to climb |
| 14:22 | SRE identifies connection pool saturation — 349/350 connections held |
| 14:25 | DBA paged. Long-running query identified: analytics aggregation, 55 minutes runtime |
| 14:28 | DBA terminates offending query set. Connection pool begins recovering |
| 14:40 | p95 back to 500ms |
| 14:48 | p95 back to baseline 300ms. Incident resolved |

---

## Five Whys

1. **Why did API latency spike?** DB connection pool was exhausted — API calls queuing for connections.
2. **Why was the connection pool exhausted?** A single query held 340 connections for 40 minutes.
3. **Why did the query hold so many connections?** The analytics aggregation spawned parallel workers, each holding a connection, with no timeout.
4. **Why was the query running on the production cluster?** The analytics replica was not configured for the tenant's reporting integration — only production cluster was accessible.
5. **Why was the analytics replica not configured?** Tenant onboarding checklist did not include routing analytics queries to the replica. Gap in runbook.

---

## Impact

- All tenants: API latency > 2s for 18 minutes, > 5s for 10 minutes
- 6 enterprise tenants: SLA 99.5% availability at risk (not breached — within 5-minute credit window)
- 0 data loss

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Route tenant analytics queries to read replica | Platform Engineering | 2026-03-21 ✓ |
| Add query timeout (300s) on production DB | DBA | 2026-03-22 ✓ |
| Add per-tenant connection limit (max 50) | Platform Engineering | 2026-03-28 |
| Update onboarding checklist for analytics replica routing | CS Ops | 2026-03-25 ✓ |
