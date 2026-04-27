# RB015 — Cross-Region Replication and Failover

**ID:** RB015  
**Category:** Disaster Recovery / Multi-Region  
**Applies to:** VC-DataPlatform, VC-API-Gateway  
**Last reviewed:** 2026-03-20

---

## Symptoms

- Customer reports data written in one region not visible in another region
- Failover event occurred but customers are still hitting the old primary
- Replication lag alert firing — replica is behind primary by > 30s
- After failover, some writes from the pre-failover window are missing
- DNS failover completed but customers seeing `ECONNREFUSED` in the new region

---

## Triage

1. Confirm whether this is replication lag (primary up, replica behind) or failover (primary failed)
2. Check current replication lag: `service:vc-dataplatform metric:replication_lag_seconds`
3. If failover occurred — check when DNS TTL expired and confirm propagation
4. Check customer's region — are they in the affected region?

---

## Common Causes

| Cause | Signal |
|---|---|
| Replication lag under heavy write load | Lag growing steadily; write throughput elevated on primary |
| Network partition between regions | Lag spike correlating with cross-region network event |
| Failover not completing cleanly | New primary accepting writes but DNS not updated |
| Customer DNS cache not expired post-failover | Customer still hitting old primary; their TTL not expired |
| Split-brain: two primaries accepting writes | Conflicting writes; data divergence (critical — escalate immediately) |
| Data written during failover window not replicated | Missing records with timestamps in the failover window |

---

## Investigation Steps

1. Check replication lag metric: is it growing, steady, or recovering?
2. Confirm primary/replica topology: which node is current primary?
3. Check DNS resolution for the affected endpoint — is it pointing to the new primary?
4. Check for any writes in the failover window that may not have been replicated
5. Check for split-brain: are both the old and new primary accepting writes?

---

## Remediation

**Replication lag (primary healthy):**
- Usually self-resolving as write load decreases
- If persistent: throttle writes temporarily to allow replica to catch up (Platform Engineering)

**DNS not propagated post-failover:**
- Verify DNS TTL was short (should be 60s in our runbooks)
- Confirm Route 53 / DNS records updated to new primary
- Customers with long local DNS caches may need to flush: provide instructions

**Missing writes from failover window:**
- These writes may be irrecoverable if they were in-flight during failover
- Identify affected tenants and affected write window
- Customer communication required: TAM + VP Customer Success

**Split-brain detected:**
- P0 — escalate immediately to Platform Engineering + DBA on-call
- Do not attempt self-remediation — risk of data corruption

---

## Escalation

- Replication lag > 60s → Platform Engineering alert threshold (auto-paged)
- Failover triggered → Platform Engineering + on-call mandatory
- Split-brain confirmed → P0 — CEO bridge if customer-data risk
