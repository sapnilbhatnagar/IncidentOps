# INC004 — CDN Configuration Error: Stale Analytics Data

**Incident ID:** INC004  
**Date:** 2026-03-27  
**Severity:** P2  
**Duration:** 108 minutes (10:00–11:48)  
**Status:** Resolved. PIR complete.

---

## Summary

A CDN configuration change incorrectly set Cache-Control max-age to 3600s on Analytics API responses (correct value: 300s). Enterprise customers saw stale dashboard data for up to 40 minutes after record updates. Affected customers on the Analytics Cloud product.

---

## Timeline

| Time | Event |
|---|---|
| 10:00 | CDN configuration change deployed as part of performance initiative |
| 10:05 | Cache-Control max-age incorrectly set to 3600s on analytics endpoints |
| 10:45 | First customer report: stale data in Analytics dashboard 40 minutes after update |
| 11:00 | Second and third customer reports. Support escalates to Platform Engineering |
| 11:15 | Platform Engineering identifies incorrect Cache-Control header value |
| 11:30 | CDN config corrected to 300s. Targeted cache purge initiated |
| 11:48 | All cache entries for Analytics API purged. Data freshness confirmed |

---

## Five Whys

1. **Why did customers see stale data?** CDN was serving cached responses for up to 1 hour instead of 5 minutes.
2. **Why was the TTL set to 3600s?** A configuration template used in the CDN performance initiative had 3600s as default; the Analytics API override was not applied.
3. **Why was the override not applied?** The CDN change was made without a per-endpoint review — only top-level defaults were checked.
4. **Why was there no per-endpoint review?** CDN change process did not require a change manager sign-off for "minor" configuration changes.
5. **Why did it take 45 minutes to detect?** No synthetic monitoring checks data freshness — only error rate and latency are monitored.

---

## Impact

- All Analytics Cloud customers: data freshness degraded from < 5 minutes to up to 60 minutes
- 4 enterprise customers raised support tickets
- No data loss. No incorrect data — only stale data.

---

## Actions

| Action | Owner | Due |
|---|---|---|
| Add synthetic monitor for data freshness on Analytics API | Platform Engineering | 2026-04-03 |
| Require change manager review for all CDN config changes | Platform Engineering | 2026-04-01 ✓ |
| Document correct per-endpoint Cache-Control values in CDN runbook | Platform Engineering | 2026-04-05 |
| Proactive customer comms for future CDN changes affecting cache | CS Ops | 2026-04-10 |
