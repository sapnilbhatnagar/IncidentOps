# RB013 — Event Streaming and Message Queue Failures

**ID:** RB013  
**Category:** Messaging / Events  
**Applies to:** VC-Webhooks, VC-DataPlatform, VC-Sync  
**Last reviewed:** 2026-03-15

---

## Symptoms

- Customer reports real-time events not arriving (Kafka / queue-backed event stream)
- Consumer lag growing — events produced but not consumed
- Event ordering guarantees violated — customer seeing out-of-order events
- Dead-letter queue depth growing with no corresponding alerts
- Customers on event subscription reporting `subscription paused` errors

---

## Triage

1. Check consumer group lag on the affected topic
2. Check dead-letter queue depth — are messages failing to process?
3. Check consumer pod health — are consumers running?
4. Check if producer is still writing (or has it also stalled?)

---

## Common Causes

| Cause | Signal |
|---|---|
| Consumer pod crashed / not running | Consumer group lag growing; no consumer heartbeats |
| Poison message causing repeated consumer crash | Consumer restarts in loop; same offset not advancing; DLQ filling |
| Consumer too slow for producer throughput | Lag growing gradually; consumer is alive but overwhelmed |
| Broker partition leadership rebalance | Temporary lag spike; resolves in < 2 min without intervention |
| Schema registry mismatch | Consumer fails to deserialise messages; deserialization errors in logs |
| Subscription quota exceeded | `subscription_paused` error; tenant has exceeded event subscription limit |

---

## Investigation Steps

1. Check consumer lag: `service:vc-dataplatform metric:consumer_lag topic:<topic>`
2. Check DLQ depth: `service:vc-dataplatform metric:dlq_depth topic:<topic>`
3. Check consumer pod status and restart count
4. Inspect DLQ messages for common error pattern
5. Check schema registry for version mismatch on the topic

---

## Remediation

**Consumer crashed:**
- Restart consumer pod (Platform Engineering)
- Investigate crash cause in pod logs

**Poison message:**
- Skip the poison message via offset manipulation (Platform Engineering, Tier 3)
- The skipped message is moved to DLQ automatically
- Investigate the message shape — is it a producer bug or a schema violation?

**Consumer overwhelmed:**
- Scale consumer replicas (Platform Engineering)
- Check if topic partitions allow parallelism (partition count vs consumer count)

**Schema registry mismatch:**
- Roll back producer to previous schema version until consumers are updated
- Schema evolution should be backward-compatible — flag to Platform Engineering

**Subscription quota exceeded:**
- Review customer's subscription tier
- Temporary quota increase requires TAM approval

---

## Escalation

- DLQ depth > 10k messages → Platform Engineering (data loss risk)
- Ordering violation confirmed → Platform Engineering (P1)
