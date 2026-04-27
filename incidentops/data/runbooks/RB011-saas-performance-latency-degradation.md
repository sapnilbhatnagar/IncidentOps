# RB011 — Performance Degradation and Latency Spikes

**ID:** RB011  
**Category:** Performance  
**Applies to:** VC-API-Gateway, VC-DataPlatform, VC-Observability  
**Last reviewed:** 2026-03-08

---

## Symptoms

- Customer reports API p95 latency > 3s (baseline < 300ms)
- Requests completing but slowly — not timing out
- Latency affects a subset of endpoints or all endpoints equally
- Symptoms appear at a specific time of day (load pattern) or after a deploy

---

## Triage

1. Is this one tenant or multi-tenant? Check `VC-Observability` latency by tenant
2. Is this one endpoint or all? Narrow the blast radius
3. Is it correlated with a deploy, a traffic spike, or a platform event?
4. Check downstream service latency — is the API gateway fast but a backend slow?

---

## Common Causes

| Cause | Signal |
|---|---|
| Noisy neighbour tenant using disproportionate compute | One tenant's traffic correlates with degradation for others |
| Missing database index on new query pattern | Latency on specific endpoints only; slow query log shows full table scans |
| Upstream dependency slowdown (third-party IdP, payment processor) | Latency on auth or payment endpoints specifically |
| Inefficient N+1 query introduced in recent deploy | Latency spike starting at deploy time; trace shows many small DB calls |
| Cache miss storm after cache flush | Spike immediately after cache clear; returns to baseline within minutes |
| Memory pressure causing GC pauses | Latency spikes every ~30s; GC log shows long pauses |

---

## Investigation Steps

1. Pull p50/p95/p99 latency by endpoint and tenant for the affected window
2. Check trace for a slow request — which span is the bottleneck?
3. Check slow query log: `service:vc-dataplatform query_duration_ms:>1000`
4. Check GC metrics if latency is periodic (every 20-60s)
5. Check noisy neighbour: per-tenant CPU and request rate during the window

---

## Remediation

**Noisy neighbour:**
- Apply stricter rate limits to the offending tenant (RB002)
- If legitimate traffic spike: notify tenant + discuss quota upgrade

**Missing index:**
- Platform Engineering to add index — typically zero-downtime in Postgres with `CREATE INDEX CONCURRENTLY`
- Monitor slow query log for improvement

**N+1 query from deploy:**
- Roll back the deploy if latency is severe (> 5s p95)
- Fix in code, re-deploy with query batching

**Cache miss storm:**
- Usually self-resolving — cache repopulates within minutes
- If persistent: check cache TTL configuration

---

## Escalation

- Latency > 5s p95 across all tenants → Platform Engineering (P1)
- Identified as upstream third-party dependency → TAM to notify affected customers
