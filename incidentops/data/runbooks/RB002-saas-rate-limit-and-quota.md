---
id: RB002
title: Rate Limit and Quota Issues (429, Burst, Daily Quota)
last_updated: 2026-03-08
owner: api-platform
severity_levels: [P3, P2]
related_runbooks: [RB001]
related_codes: [RATE-429-USER, RATE-429-TENANT, RATE-QUOTA-DAILY, RATE-BURST]
---

## When to use

Use this runbook when one or more of the following is observed:

- Customer reports a sudden surge in 429 responses.
- VC-API-Gateway emits `RATE-LIMIT-HIT` for a tenant at elevated rate.
- An integration owner reports their batch job started failing this morning.

## Symptoms

- Customer ticket: "we are being rate limited", "all our requests are 429", "our nightly sync broke".
- VC-Observability alert: `TENANT-429-RATE` over 5% of requests.

## Severity

- **P2**: tenant-wide blocking that breaks a customer's production integration.
- **P3**: single user, expected burst limit, customer-side retry storm.

## Initial triage (5 minutes)

1. Identify whether the limit hit is per-user, per-tenant, or per-API-key.
2. Pull last 60 minutes of request volume for the tenant from VC-Observability.
3. Check whether tenant tier matches the limit they are hitting (Pro tier vs Enterprise tier have different limits).
4. Confirm whether the customer recently changed integration code, deployed a new client, or onboarded new end-users.

## Investigation by code

### RATE-429-USER

Single user exceeded per-user limit.

- Almost always customer-side retry storm or runaway loop.
- No platform action. Recommend client-side exponential backoff.

### RATE-429-TENANT

Tenant exceeded contracted per-tenant rate.

- Confirm contracted limit (check VC-Billing tier).
- If new high-volume use case, route to Customer Success for tier conversation.
- For genuine emergencies, temporary uplift can be authorised by VP Customer Support, time-boxed to 24h, logged.

### RATE-QUOTA-DAILY

Daily quota exhausted.

- Confirm reset time (typically UTC midnight).
- Educate customer on quota windows.
- Most often a sign that customer is using interactive APIs for batch workloads. Recommend bulk endpoints.

### RATE-BURST

Short-window burst limit exceeded.

- Recommend exponential backoff with jitter.
- Look for retry storm patterns: many requests with identical bodies in <1s windows.

## Common causes (ranked by frequency)

1. Customer-side retry storm after a transient error.
2. Customer using single-record APIs for what should be a bulk job.
3. Customer onboarded a new high-volume team without telling Customer Success.
4. Customer client SDK out of date and not respecting `Retry-After` headers.
5. Genuine usage growth that justifies tier conversation.

## Remediation

- For customer-side retry storm: provide retry pattern guidance, recommend SDK upgrade.
- For tier mismatch: hand off to Customer Success.
- For emergency uplift: time-boxed, logged, requires VP Customer Support sign-off.
- Never silently raise a customer's limit. Never disable rate limiting. Never bypass the gateway.

## Escalation

- P2: assign to API Platform queue, target 2h response if production-blocking.
- P3: standard support response.

## Post-resolution checklist

- Customer confirms requests succeeding.
- Root cause documented in ticket (retry storm, tier mismatch, etc.).
- If pattern repeats, surface to Customer Success for tier conversation.
