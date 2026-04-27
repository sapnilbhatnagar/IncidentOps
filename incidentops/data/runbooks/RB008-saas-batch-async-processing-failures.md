# RB008 — Batch Job and Async Processing Failures

**ID:** RB008  
**Category:** Async / Batch  
**Applies to:** VC-DataPlatform, VC-Webhooks, VC-Sync  
**Last reviewed:** 2026-03-10

---

## Symptoms

- Customer reports bulk import/export job stuck in `PENDING` or `PROCESSING` for > 30 min
- Batch API calls return `202 Accepted` but no completion webhook fires
- Job status endpoint returns `FAILED` with no `error_detail`
- Incremental sync jobs completing but data not appearing in customer's destination
- Customer reports duplicate records after a batch job retry

---

## Triage

1. Confirm the job ID and tenant ID from the customer report
2. Check job status: `GET /v2/jobs/{job_id}` — what state is it in?
3. Check `VC-DataPlatform` job worker logs for the job_id
4. Check if the job's completion webhook endpoint is reachable

---

## Common Causes

| Cause | Signal |
|---|---|
| Job worker crashed mid-processing | Job in `PROCESSING` state > timeout; worker logs show OOM or panic |
| Completion webhook unreachable | Job succeeded internally but `FAILED` on delivery; look for webhook delivery logs |
| Payload too large for single job | Job fails at `PARSING` stage with `PayloadTooLargeError` |
| Idempotency key collision on retry | Duplicate records; check `idempotency_key` on the original request |
| Downstream service unavailable during write phase | Job `FAILED` at `WRITING` stage; check VC-DataPlatform dependencies |
| Job queue backed up | Job stuck in `PENDING`; check queue depth metric |

---

## Investigation Steps

1. `GET /v2/jobs/{job_id}` — inspect `state`, `started_at`, `completed_at`, `error_detail`
2. Check worker logs: `service:vc-dataplatform job_id:<id>`
3. Check webhook delivery log for the job's `callback_url`
4. Check queue depth: `service:vc-dataplatform queue_depth` — is it elevated?
5. For duplicates: compare `idempotency_key` on original vs retry requests

---

## Remediation

**Stuck job (worker crash):**
- Trigger manual re-queue via internal tooling (Tier 3 only)
- If job is idempotent, ask customer to resubmit with same idempotency key
- Investigate worker OOM — may require Platform Engineering if systemic

**Completion webhook not firing:**
- Verify webhook endpoint reachability from VertexCloud egress IPs
- Check RB003 (webhook delivery failures) for webhook-specific investigation

**Payload too large:**
- Direct customer to split payload — max job payload is 50MB
- Batch API supports chunked job submission via `parent_job_id`

**Duplicate records on retry:**
- Confirm customer is passing a stable `idempotency_key` on retries
- If duplicates already in system: customer must reconcile; provide query to identify dupes

---

## Escalation

- Worker crash confirmed systemic → Platform Engineering (P1 if multi-tenant)
- Queue depth > 10k jobs → Platform Engineering (capacity)
- Data corruption confirmed → P0 — escalate immediately
