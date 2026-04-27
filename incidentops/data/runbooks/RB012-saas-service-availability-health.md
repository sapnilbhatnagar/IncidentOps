# RB012 — Service Availability and Health Check Failures

**ID:** RB012  
**Category:** Availability  
**Applies to:** VC-API-Gateway, all VC services  
**Last reviewed:** 2026-03-12

---

## Symptoms

- Customer reports complete inability to reach the API (`Connection refused` or `503 Service Unavailable`)
- Health check endpoint (`/health`) returning non-200
- Load balancer health checks failing, removing pods from rotation
- Intermittent 503s with rapid recovery (< 30s) suggesting flapping

---

## Triage

1. Check status page — is there an active incident?
2. Check which services are unhealthy: `VC-Observability` → service health dashboard
3. Is this one region or multi-region?
4. Is it all tenants or a subset?

---

## Common Causes

| Cause | Signal |
|---|---|
| Pod OOMKilled and not yet restarted | Kubernetes events show `OOMKilled`; pod restart count elevated |
| Liveness probe misconfigured after deploy | Health check failures start at deploy time |
| Dependency service unhealthy (e.g. VC-Identity down) | Cascading failure; VC-Identity health check also failing |
| Node failure removing pods from cluster | Multiple pods failing simultaneously; node NotReady in cluster events |
| Deployment rollout with zero-downtime misconfigured | 503s during rollout window; `maxUnavailable` set incorrectly |

---

## Investigation Steps

1. Check `GET /health` — is it returning 200? What body?
2. Check pod logs for crash reason: look for OOM, panic, or unhandled exception
3. Check Kubernetes events for the affected namespace
4. Check whether the health check failing is a dependency (readiness probe checking downstream)
5. Check recent deploys — did this start at a rollout?

---

## Remediation

**OOMKilled pods:**
- Increase memory limit for the affected service (Platform Engineering)
- Short-term: cordon the affected node if node-level; reschedule pods

**Misconfigured liveness probe:**
- Adjust probe timeout/threshold — Platform Engineering
- Roll back deploy if liveness probe kills healthy pods

**Cascading dependency failure:**
- Identify the root dependency using the service health chain
- Apply circuit breaker if not already active
- Follow the unhealthy dependency's own runbook

**Zero-downtime rollout misconfiguration:**
- Pause rollout: `kubectl rollout pause`
- Fix `maxUnavailable` / `maxSurge` — Platform Engineering

---

## Escalation

- Availability < 99% for > 5 minutes on any tenant → Platform Engineering + on-call
- Multi-region outage → P0 — escalate to VP Engineering
