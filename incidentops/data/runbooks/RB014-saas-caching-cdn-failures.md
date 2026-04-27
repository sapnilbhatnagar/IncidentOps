# RB014 — Caching and CDN Failures

**ID:** RB014  
**Category:** Caching / CDN  
**Applies to:** VC-API-Gateway, CDN layer (Cloudflare / Fastly)  
**Last reviewed:** 2026-03-18

---

## Symptoms

- Customers receiving stale data after an update (cache not invalidated)
- Cache-related headers (`Cache-Control`, `ETag`, `Vary`) behaving unexpectedly
- Sudden spike in origin traffic suggesting CDN is bypassing cache
- Customers in different regions seeing different data for the same resource
- API responses with `Age` header showing unexpectedly high values

---

## Triage

1. Check `Age` header on the failing response — is it being served from cache?
2. Check `Cache-Control` response headers — are they correct?
3. Is this one region or all regions?
4. Did a cache flush or configuration change recently occur?

---

## Common Causes

| Cause | Signal |
|---|---|
| Cache invalidation not triggered after write | Stale response; `Age` > 0 after the resource was updated |
| Cache key includes varying headers, causing misses | High miss rate; `Vary` header too broad |
| CDN config change bypassing cache | 100% miss rate starting at a specific time |
| Cache poisoning via host header injection | Customers seeing other tenants' cached data (rare; requires immediate escalation) |
| Short TTL causing excessive origin load | Origin CPU elevated; cache hit rate < 30% |
| Cache stampede after TTL expiry | Latency spike for ~10s; resolves as cache repopulates |

---

## Investigation Steps

1. Test the resource directly: check `Age`, `Cache-Control`, `X-Cache` headers
2. Check CDN cache hit rate in `VC-Observability`: `metric:cdn_cache_hit_rate`
3. Confirm cache invalidation was triggered on the relevant write operation
4. Check CDN configuration changelog for recent changes
5. Check `Vary` header — if it includes `Cookie` or `Authorization`, caching is effectively disabled

---

## Remediation

**Stale cache (invalidation not triggered):**
- Trigger manual cache purge for the affected resource/path (Platform Engineering)
- Investigate why invalidation did not fire — is the write path wired to cache eviction?

**Cache bypassed due to config change:**
- Roll back CDN configuration change
- Platform Engineering to review and re-apply with correct settings

**Cache poisoning (highest severity):**
- Immediately purge all caches
- Rotate any session tokens that may have been exposed
- Escalate to Security + Platform Engineering — P0

**Short TTL / stampede:**
- Increase TTL for stable resources
- Implement stale-while-revalidate to smooth stampedes

---

## Escalation

- Cross-tenant cache poisoning suspected → P0, Security + Platform Engineering immediately
- CDN outage (all regions) → P0, CDN vendor support + Platform Engineering
