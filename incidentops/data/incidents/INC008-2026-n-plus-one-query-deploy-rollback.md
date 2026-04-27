# INC008 — N+1 Query Regression: Deploy Rollback

**Incident ID:** INC008  
**Date:** 2026-03-22  
**Severity:** P1  
**Duration:** 27 minutes (10:55–11:22)  
**Status:** Resolved. PIR complete.

---

## Summary

Deploy v2.14.1 of VC-API-Gateway introduced an N+1 query pattern in the request authorization middleware. Every API call began making one DB query per OAuth scope instead of a batched lookup. High-scope enterprise tokens triggered 12+ DB calls per request, pushing p95 latency to 4.2s. Rollback resolved the issue in 22 minutes.

---

## Timeline

| Time | Event |
|---|---|
| 10:55 | v2.14.1 deployed to VC-API-Gateway via rolling update |
| 11:00 | VC-API-GATEWAY-LATENCY-HIGH alert fires — p95 at 2.1s |
| 11:03 | Latency still rising — p95 at 3.8s. SRE opens incident bridge |
| 11:05 | Correlation with deploy at 10:55 identified immediately |
| 11:08 | Trace analysis confirms N+1 pattern in authorization middleware |
| 11:10 | Rollback to v2.13.9 initiated |
| 11:14 | Rolling rollback progressing — latency begins to drop |
| 11:22 | Rollback complete. p95 back to 310ms baseline |

---

## Five Whys

1. **Why did API latency spike?** Every API call was making 12+ sequential DB queries in the authorization path.
2. **Why was there an N+1 query?** The authorization middleware was refactored to check permissions one scope at a time instead of with a single batched query.
3. **Why did this pass code review?** The refactor looked logically correct; the reviewer did not recognise the N+1 pattern without seeing the SQL it generated.
4. **Why did pre-deploy testing not catch it?** Performance testing used tokens with 1-2 scopes; enterprise tokens with 8-15 scopes were not in the test matrix.
5. **Why was the test matrix limited to 1-2 scopes?** No standardized load test corpus including high-scope enterprise tokens existed.

---

## Impact

- All tenants: API p95 latency 2-4.2s for 22 minutes
- 0 errors (latency only — no timeouts)
- 0 SLA breaches (P99 stayed under the 10s SLA threshold)
- Rollback: total time to resolution 27 minutes

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Add high-scope enterprise token to load test matrix | Platform Engineering | 2026-03-29 ✓ |
| Add N+1 query detection to CI (via query count assertion in integration tests) | Platform Engineering | 2026-04-10 |
| Fix the batched authorization lookup and re-deploy as v2.14.2 | Platform Engineering | 2026-03-23 ✓ |
| Add latency regression gate to deploy pipeline (p95 < 500ms for 5 min post-deploy) | Platform Engineering | 2026-04-15 |
