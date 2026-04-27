# RB010 — Database Connection Pool Exhaustion

**ID:** RB010  
**Category:** Platform Reliability  
**Applies to:** VC-DataPlatform, VC-API-Gateway  
**Last reviewed:** 2026-03-05

---

## Symptoms

- API responses slowing to > 5s then timing out
- Error: `connection pool exhausted` or `too many connections` in logs
- Read and write operations both degraded equally
- Dashboard shows DB connection count at ceiling
- Symptoms appear gradually then collapse sharply

---

## Triage

1. Check current DB connection count vs pool ceiling
2. Check which services hold the most connections
3. Check for long-running queries blocking connection release
4. Check if a recent deploy changed connection pool configuration

---

## Common Causes

| Cause | Signal |
|---|---|
| Long-running queries holding connections | Active connection count high; `pg_stat_activity` shows old queries |
| Pool ceiling too low for current traffic | Connection count at exactly the ceiling; traffic is normal |
| Connection leak in application code | Connections held with no associated query; count grows over time |
| Thundering herd after an outage | All services reconnecting simultaneously after brief DB unavailability |
| Deploy without graceful connection drain | Spike at deploy time; old connections not released before new ones open |

---

## Investigation Steps

1. Check connection count: `service:vc-dataplatform metric:db_connections_active`
2. Check for long-running queries in `VC-DataPlatform` logs: `query_duration_ms:>30000`
3. Confirm pool ceiling configuration — compare to current peak connections
4. Check recent deploys for connection pool configuration changes
5. Check for thundering herd pattern: connection spike correlated with prior brief outage

---

## Remediation

**Long-running queries blocking connections:**
- Identify and terminate offending queries (Tier 3 / Platform Engineering only)
- Investigate query origin — likely a customer bulk operation or missing index

**Pool ceiling too low:**
- Adjust pool ceiling — Platform Engineering action
- Short-term: shed non-critical read traffic to read replica

**Connection leak:**
- Identify service with leak from connection attribution metrics
- Platform Engineering to deploy fix + restart affected service pods

**Thundering herd:**
- Stagger reconnect with exponential backoff (usually self-resolving in 2-5 min)
- If not resolving: shed traffic via rate limiter to allow orderly reconnect

---

## Escalation

- Pool exhaustion causing customer-facing errors → Platform Engineering (P1)
- Long-running query identified but not terminable without data risk → DBA on-call
