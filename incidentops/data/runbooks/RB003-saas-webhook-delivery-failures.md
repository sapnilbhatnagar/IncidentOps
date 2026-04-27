---
id: RB003
title: Webhook Delivery Failures (Timeout, Signature, Retry Exhausted, Endpoint Down)
last_updated: 2026-01-22
owner: integration-platform
severity_levels: [P3, P2, P1]
related_runbooks: [RB004]
related_codes: [WHK-DELIVERY-TIMEOUT, WHK-SIG-MISMATCH, WHK-RETRY-EXHAUSTED, WHK-ENDPOINT-DOWN, WHK-PAYLOAD-OVERSIZE]
---

## When to use

Use this runbook when one or more of the following is observed:

- Customer reports their webhook endpoint stopped receiving events.
- VC-Webhooks emits elevated `delivery.failed` rate for a tenant.
- Customer reports duplicate or out-of-order webhook events.

## Symptoms

- Customer ticket: "we stopped receiving webhooks", "signature does not validate", "duplicate events".
- VC-Observability alert: `WHK-DELIVERY-FAILURE-RATE` over threshold.

## Severity

- **P1**: cross-tenant webhook delivery degradation (platform-side issue).
- **P2**: single tenant losing events on a critical integration.
- **P3**: single endpoint timing out.

## Initial triage (5 minutes)

1. Pull last 60 minutes of delivery attempts for the tenant from VC-Webhooks.
2. Check whether failures are concentrated on one endpoint or across all of the tenant's endpoints.
3. Check VC-Webhooks status for any platform-wide degradation.
4. Confirm whether the customer recently changed their endpoint (new URL, new TLS cert, new signing secret).

## Investigation by code

### WHK-DELIVERY-TIMEOUT

Endpoint did not respond within 10s.

- Customer's endpoint is doing too much work synchronously.
- Recommend customer accept the webhook to a queue and process asynchronously.
- Check whether endpoint latency is gradually rising (capacity issue) or sudden cliff (deploy regression).

### WHK-SIG-MISMATCH

HMAC signature does not validate on receiver.

- Confirm shared secret has not been rotated without customer being informed.
- Verify signing algorithm (default HMAC-SHA256).
- Check for canonicalisation issues: trailing whitespace, charset, header ordering.
- A common pitfall: customer's framework strips or modifies the body before validating.

### WHK-RETRY-EXHAUSTED

Webhook retried up to maximum (default 8 attempts over 24h) and remains undelivered.

- Surface dead-letter queue contents to customer.
- Confirm endpoint health.
- Recommend customer enable replay-by-time once endpoint recovered.

### WHK-ENDPOINT-DOWN

Endpoint reachable but returning 5xx.

- Customer-side issue.
- Provide VC-Webhooks logs (status codes, response bodies) to customer for their debug.
- Do not retry beyond default budget.

### WHK-PAYLOAD-OVERSIZE

Payload exceeds 1 MB.

- Confirm payload contents.
- Recommend customer subscribe to summary events with detail-fetch pattern.

## Common causes (ranked by frequency)

1. Customer's endpoint capacity insufficient for event volume.
2. Customer rotated signing secret without updating both ends.
3. Customer deployed a regression that broke their handler.
4. Customer's TLS certificate expired.
5. Platform-side delivery worker degradation (rare, P1).

## Remediation

- Provide customer with delivery logs and dead-letter contents.
- Recommend retry, replay, or DLQ processing as appropriate.
- For platform-side degradation, engage Integration Platform on-call.
- Never replay webhooks on the customer's behalf. Never modify webhook payloads. Never share signing secrets in support tickets.

## Escalation

- P1: page Integration Platform on-call, open incident bridge, status page update.
- P2: assign to Integration Platform queue, target 4h.
- P3: standard support response.

## Post-resolution checklist

- Customer confirms events flowing.
- Dead-letter queue cleared if customer requested replay.
- Root cause documented.
- If pattern repeats, surface to engineering for delivery-mechanism review.
