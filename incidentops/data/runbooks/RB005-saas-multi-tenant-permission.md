---
id: RB005
title: Multi-Tenant Permission and ACL Issues (Cross-Tenant, Role, Downgrade, Consent)
last_updated: 2026-03-15
owner: identity-platform
severity_levels: [P3, P2, P1]
related_runbooks: [RB001]
related_codes: [ACL-CROSS-TENANT, ACL-ROLE-MISMATCH, ACL-DOWNGRADE, ACL-MISSING-CONSENT]
---

## When to use

Use this runbook when one or more of the following is observed:

- Customer reports a user can see something they should not.
- Customer reports a user cannot see something they should.
- VC-Identity emits elevated ACL-* events for a tenant.
- Internal Audit raises a cross-tenant access concern.

## Symptoms

- Customer ticket: "user X has wrong permissions", "we are seeing data from another company", "the consent prompt keeps appearing".
- VC-Observability alert: `ACL-DENY-RATE` or `ACL-CROSS-TENANT-EVENT`.

## Severity

- **P1**: confirmed cross-tenant data exposure. Engage Privacy and InfoSec immediately. Reportable to DPO.
- **P2**: role mismatch broken a critical integration.
- **P3**: expected permission downgrade or consent prompt.

## Initial triage (5 minutes)

1. Identify whether issue is access denied (lost permission) or access granted in error (escalated permission).
2. Pull VC-Identity audit log for the principal in question.
3. Confirm whether customer admin recently changed roles, scopes, or tenant membership.
4. For any suspected cross-tenant exposure, **stop normal triage and escalate immediately**. This is a P1 by default until proven otherwise.

## Investigation by code

### ACL-CROSS-TENANT

Request from one tenant attempted to access another tenant's resource.

- VC-API-Gateway denies these by default. Confirm denial in audit log.
- If denial confirmed: P3, no platform action, customer comms only.
- If access succeeded: **P1**, page Privacy and InfoSec, freeze the principal's session, full audit.
- Most common false positive: customer admin assigned a service account to multiple tenants and the access was legitimate but unfamiliar to the reporting customer.

### ACL-ROLE-MISMATCH

User's role grants smaller scope than the resource requires.

- Confirm role assignment with customer admin.
- Confirm scope hierarchy is current.
- Most common cause: scope hierarchy changed by VertexCloud product team and customer admin role definitions out of date.

### ACL-DOWNGRADE

User had permission at session start, lost it mid-session.

- Expected behaviour. Customer admin removed the role.
- No platform action. Customer comms only: explain the session-cache TTL.

### ACL-MISSING-CONSENT

Action requires consent not on file.

- Surface the consent requirement to customer admin.
- Block until consent recorded.
- Common after GDPR or regional regulation update; the consent type is new.

## Common causes (ranked by frequency)

1. Customer admin role change without informing affected users.
2. VertexCloud-side scope hierarchy update that customer admin role definitions did not catch up to.
3. Service account configured across multiple tenants legitimately, looks suspicious to one of those tenants.
4. New consent requirement post-regulation update.
5. Genuine cross-tenant exposure (rare, P1).

## Remediation

- For role mismatch: provide diff and remediation to customer admin.
- For downgrade: customer comms only.
- For missing consent: surface consent flow.
- For confirmed cross-tenant exposure: incident bridge, freeze, audit, customer comms drafted by Privacy.
- Never modify a customer's role assignments. Never grant or revoke permissions. Never bypass tenant isolation.

## Escalation

- P1 (suspected cross-tenant exposure): page Privacy and InfoSec on-call, open incident bridge, notify DPO. **Do not communicate to customer until Privacy approves wording.**
- P2: assign to Identity Platform queue, target 4h.
- P3: standard support response.

## Post-resolution checklist

- Customer confirms permissions match expectation.
- For any cross-tenant suspicion: full audit logged with DPO.
- If pattern repeats, surface to engineering for product fix.
- Update permission documentation if scope hierarchy changed.
